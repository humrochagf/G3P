# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


def get_user_balance(user, until=None):
    orders = user.pedidos.filter()
    if until is not None:
        orders = orders.filter(data_solicitacao__lte=until)
    return sum(pedido.get_value() for pedido in orders)


class Parceiro(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = u"Parceiro"
        verbose_name_plural = u"Parceiros"


class DinheiroField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 11)
        kwargs.setdefault('decimal_places', 2)
        return super(DinheiroField, self).__init__(*args, **kwargs)


class ProdutoQueryMixin(object):
    """
    Métodos comuns aos queryset e managers de produtos.
    """

    def _latest_version_ids(self):
        """
        Retorna um queryset contendo apenas os ids das últimas versões
        de cada produto.
        """
        return self.values('codigo')\
                .annotate(max_id=models.Max('id'))\
                .order_by('max_id')\
                .values_list('max_id', flat=True)

    def latest_version(self):
        """
        Filtra o queryset mantendo apenas as últimas versões dos
        produtos.
        """
        subquery = self._latest_version_ids()
        return self.filter(id__in=subquery)

    def active(self):
        """
        Retorna apenas os produtos em suas últimas versões que estão
        ativos.
        """
        return self.latest_version().filter(ativo=True)


class ProdutoQuerySet(models.query.QuerySet, ProdutoQueryMixin):
    pass


class ProdutoManager(models.Manager, ProdutoQueryMixin):
    use_for_related_managers = True

    def get_query_set(self):
        return ProdutoQuerySet(self.model, using=self._db)


class Produto(models.Model):
    TIPO_CHOICES = (
        (0, u"Venda"),
        (1, u"Aluguel"),
    )

    codigo = models.CharField(max_length=32, editable=False)

    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES)
    titulo = models.CharField(u"Titulo", max_length=255)
    preco = DinheiroField(u"Preço")

    # Verificar a validade do ativo pois a queryset ja garante pegar a
    # verção atual sem utiliza-lo, observe que ele em momento algum é setado
    # como False.
    ativo = models.BooleanField(default=True, editable=False)

    VERSIONED_FIELDS = ('tipo', 'preco')

    objects = ProdutoManager()

    class Meta:
        unique_together = (('codigo', 'id'),)

    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = uuid.uuid1().hex
        return super(Produto, self).save(*args, **kwargs)

    def versioned_save(self):
        fresh = self.__class__.objects.get(pk=self.pk)
        new_version = False
        for field_name in self.VERSIONED_FIELDS:
            if getattr(self, field_name) != getattr(fresh, field_name):
                new_version = True
                break

        if not new_version:
            self.save()
            return self
        else:
            return self._create_new_version()

    versioned_save.alters_data = True

    def _create_new_version(self):
        """
        Cria uma nova versão deste produto.
        """
        data = {field.name: getattr(self, field.name)
                for (field, model) in self._meta.get_fields_with_model()}
        del data['id']
        return self.__class__.objects.create(**data)


class Pedido(models.Model):
    APROVACAO_CHOICES = (
        (False, u"Não"),
        (True, u"Sim")
    )

    solicitante = models.ForeignKey('auth.User', related_name='pedidos',
                                    verbose_name=u"Solicitante", editable=False)
    aprovacao = models.BooleanField(u'Aprovado?', choices=APROVACAO_CHOICES,
                                    default=False)
    data_solicitacao = models.DateTimeField(u"Data de solicitação", auto_now_add=True)
    data_saida = models.DateTimeField(u"Data de envio")
    data_retorno = models.DateTimeField(u"Data de retorno", null=True, blank=True)
    anotacoes = models.TextField(u"Anotações", null=True, blank=True)

    produtos = models.ManyToManyField('Produto', through='RelacaoPedidoProduto', related_name='pedidos')

    def __unicode__(self):
        return u"Pedido %s" % self.id

    def get_value(self):
        values = self.relacaopedidoproduto_set.values_list(
                            'produto__preco', 'quantidade')
        values = (val * quant for (val, quant) in values)

        # considerar os descontos
        discounts = self.descontos.values_list('valor', flat=True)

        return sum(values) - sum(discounts)


class RelacaoPedidoProduto(models.Model):
    pedido = models.ForeignKey('Pedido')
    produto = models.ForeignKey('Produto')
    quantidade = models.PositiveIntegerField(u"Quantidade")

    class Meta:
        unique_together = ("pedido", "produto")
        verbose_name = u"Item de pedido"
        verbose_name_plural = u"Itens de pedido"


class Desconto(models.Model):
    pedido = models.ForeignKey('Pedido', related_name='descontos')
    valor = DinheiroField(u"Valor em R$")
    justificativa = models.TextField(u"Justificativa")


class InheritanceCastModel(models.Model):
    """
    Uma classe abstrata que possui uma FK para seu tipo de conteúdo.

    Muito útil para criar um esquema de herança em que se pode fazer
    casting dos objetos.

    Referência:
        http://stackoverflow.com/questions/929029/how-do-i-access-the-child-classes-of-an-object-in-django-without-knowing-the-nam/929982#929982
    """
    tipo = models.ForeignKey('contenttypes.ContentType', editable=False,
                             verbose_name=u"Tipo")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.content_type = self._get_content_type()
        return super(InheritanceCastModel, self).save(*args, **kwargs)

    def cast(self):
        return self.content_type.get_object_for_this_type(pk=self.pk)

    def _get_content_type(self):
        return ContentType.objects.get_for_model(type(self))


class Pagamento(InheritanceCastModel):
    usuario = models.ForeignKey('auth.User', verbose_name=u"Parceiro")
    data = models.DateTimeField(u"Data")
    valor = DinheiroField(u"Valor")
    anotacoes = models.TextField(u"Anotações")

    def __unicode__(self):
        return u"Pagamento %s" % (self.id,)


class PagamentoDebito(Pagamento):
    banco = models.CharField(max_length=255)
    numero = models.CharField(u"Número do cheque", max_length=255)
    titular_conta = models.CharField(u"Titular da conta", max_length=255)
    data_deposito = models.DateTimeField(u"Data do depósito")

    class Meta:
        verbose_name = u"Pagamento em débito"
        verbose_name_plural = u"Pagamentos em débito"


class PagamentoCheque(Pagamento):
    banco = models.CharField(max_length=255)
    numero = models.CharField(u"Número do cheque", max_length=255)
    titular_conta = models.CharField(u"Titular da conta", max_length=255)

    class Meta:
        verbose_name = u"Pagamento com cheque"
        verbose_name_plural = u"Pagamentos com cheque"


# TODO isolar o banco em outra tabela, usar aquele índice da febraban (3
# caracteres alfanuméricos [+ dígito opcional?])
