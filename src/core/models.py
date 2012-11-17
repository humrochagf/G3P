# -*- coding: utf-8 -*-
from django.db import models


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
        (2, u"Composto"),
    )

    codigo = models.PositiveIntegerField(default=0, editable=False)

    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES)
    titulo = models.CharField(u"Titulo", max_length=255)
    preco = DinheiroField(u"Preço")

    # se for NULL, significa que o produto "não possui estoque", o que é
    # diferente de um produto que "não possui nenhum item em estoque", caso no
    # qual estoque seria igual a zero.
    estoque = models.PositiveIntegerField(u"Estoque", null=True, blank=True)

    ativo = models.BooleanField(default=True, editable=False)

    composicao = models.ManyToManyField('self', null=True, blank=True,
                                        limit_choices_to={'tipo': 1},
                                        related_name='compositor')

    VERSIONED_FIELDS = ('tipo', 'preco')

    objects = ProdutoManager()

    class Meta:
        unique_together = (('codigo', 'id'),)

    def __unicode__(self):
        return self.titulo

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
    solicitante = models.ForeignKey('auth.User', related_name='pedidos',
                                    verbose_name=u"Solicitante")
    data_solicitacao = models.DateTimeField(u"Data de solicitação", auto_now_add=True)
    data_saida = models.DateTimeField(u"Data de envio")
    data_retorno = models.DateTimeField(u"Data de retorno", null=True)
    anotacoes = models.TextField(u"Anotações", null=True, blank=True)

    produtos = models.ManyToManyField('Produto', through='RelacaoPedidoProduto', related_name='pedidos')

    def __unicode__(self):
        return u"Pedido %d" % self.id


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


class Pagamento(models.Model):
    tipo = models.ForeignKey('contenttypes.ContentType', editable=False)
    data = models.DateTimeField(u"Data")
    valor = DinheiroField(u"Valor")
    anotacoes = models.TextField(u"Anotações")


# TODO isolar o banco em outra tabela, usar aquele índice da febraban (3
# caracteres alfanuméricos [+ dígito opcional?])

class PagamentoDebito(Pagamento):
    banco = models.CharField(max_length=255)
    numero = models.CharField(u"Número do cheque", max_length=255)
    titular_conta = models.CharField(u"Titular da conta", max_length=255)
    data_deposito = models.DateTimeField(u"Data do depósito")


class PagamentoCheque(Pagamento):
    banco = models.CharField(max_length=255)
    numero = models.CharField(u"Número do cheque", max_length=255)
    titular_conta = models.CharField(u"Titular da conta", max_length=255)
