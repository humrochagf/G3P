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
    tipo = models.SmallPositiverIntegerField(choices=TIPO_CHOICES)
    preco = DinheiroField(u"Preço")
    titulo = models.CharField(u"Titulo", max_digits=255)
    estoque = models.PositiveIntegerField(u"Estoque", null=True)

    composicao = models.ManyToManyField('self')


class Cor(models.Model):
    cor = models.CharField(max_length=255)

    def __unicode__(self):
        return self.cor


class Tema(models.Model):
    tema = models.CharField(max_length=255)

    def __unicode__(self):
        return self.tema


class Pedido(models.Model):
    data_solicitacao = models.DateTimeField(u"Data de solicitação", auto_now_add=True)
    data_saida = models.DateTimeField(u"Data de envio")
    data_retorno = models.DateTimeField(u"Data de retorno", null=True)
    anotacoes = models.TextField(u"Anotações")

    produtos = models.ManyToManyField(Produto, related_name='pedidos')


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
    titular_conta = models.CharField(u"Titular da conta")
    data_deposito = models.DateTimeField(u"Data do depósito")


class PagamentoCheque(Pagamento):
    banco = models.CharField(max_length=255)
    numero = models.CharField(u"Número do cheque", max_length=255)
    titular_conta = models.CharField(u"Titular da conta")


# TODO modelar o parceiro e dar um jeito de permitir que ele possa
# autenticar-se no sistema.
