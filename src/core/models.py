# -*- coding: utf-8 -*-
from django.db import models


class DinheiroField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 11)
        kwargs.setdefault('decimal_places', 2)
        return super(DinheiroField, self).__init__(*args, **kwargs)


# TODO exclusão lógica de produtos; versionamento de produtos, para que seu
# preço possa ser alterado sem quebrar o histórico de pedidos;


class Produto(models.Model):
    TIPO_CHOICES = (
        (0, u"Venda"),
        (1, u"Aluguel"),
        (2, u"Composto"),
    )

    # se for NULL, significa que o produto "não possui estoque", o que é
    # diferente de um produto que "não possui nenhum item em estoque", caso no
    # qual estoque seria igual a zero.
    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES)
    titulo = models.CharField(u"Titulo", max_length=255)
    preco = DinheiroField(u"Preço")
    estoque = models.PositiveIntegerField(u"Estoque", null=True, blank=True)
    composicao = models.ManyToManyField('self',
                                        null=True,
                                        blank=True,
                                        limit_choices_to={'tipo': 1})

    def __unicode__(self):
        return self.titulo


class Desconto(models.Model):
    # Classe criada para lançamentos de descontos/multas
    # o desconto pode ser negativo ou positivo e relativo ou absoluto
    # sendo aplicado sobre o pedido
    # TODO checar se o modelo está correto
    TIPO_CHOICES = (
        (0, u"Debito %"),
        (1, u"Debito R$"),
        (2, u"Credito %"),
        (3, u"Credito R$"),
    )

    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES)
    valor_relativo = models.PositiveIntegerField(U"Valor %", null=True)
    valor_absoluto = DinheiroField(u"Valor R$", null=True)
    justificativa = models.TextField(u"Justificativa do desconto")


class Pedido(models.Model):
    data_solicitacao = models.DateTimeField(u"Data de solicitação", auto_now_add=True)
    data_saida = models.DateTimeField(u"Data de envio")
    data_retorno = models.DateTimeField(u"Data de retorno", null=True)
    produtos = models.ManyToManyField('Produto', through='RelacaoPedidoProduto', related_name='pedidos')
    # TODO checar referencia
    anotacoes = models.TextField(u"Anotações")
    descontos = models.ManyToManyField('Desconto', null=True)


class RelacaoPedidoProduto(models.Model):
    pedido = models.ForeignKey('Pedido')
    produto = models.ForeignKey('Produto')
    quantidade = models.PositiveIntegerField(u"Quantidade")

    class Meta:
        unique_together = ("pedido", "produto")


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


# TODO modelar o parceiro e dar um jeito de permitir que ele possa
# autenticar-se no sistema.
