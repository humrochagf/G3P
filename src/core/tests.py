# -*- coding: utf-8 -*-
from decimal import Decimal
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from src.core.models import (
    Produto,
    Pedido,
    RelacaoPedidoProduto,
    get_user_balance,
)


class VersionamentoProdutoTestCase(TestCase):
    def test_it_works(self):
        p1 = Produto.objects.create(titulo=u"Teste", preco=1, tipo=0)

        # alterar o título do produto não gera uma nova versão
        p1.titulo = u"Teste Alterado"
        p2 = p1.versioned_save()
        self.assertEqual((p1.codigo, p1.id), (p2.codigo, p2.id))

        # confirmar que o objeto foi atualizado no banco, e nenhuma nova versão
        # foi gerada
        p3 = Produto.objects.latest_version().get(codigo=p1.codigo)
        self.assertEqual((p1.codigo, p1.id), (p3.codigo, p3.id))

        # alterar o preço do produto gera uma nova versão
        p1.preco = 2
        p1v2 = p1.versioned_save()
        self.assertNotEqual((p1.codigo, p1.id), (p1v2.codigo, p1v2.id))

        # deve retornar uma lista contendo apenas as versões mais atuais
        # dos produtos, ou seja, apenas `p1v2`.
        active = Produto.objects.active()
        self.assertEqual(active.count(), 1)
        self.assertEqual(active[0].id, p1v2.id)


class BalanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('username', 'user@test.test', 'password')

    def test_order_value(self):
        p1 = Produto.objects.create(titulo=u"Teste", preco=10, tipo=0)
        p2 = Produto.objects.create(titulo=u"Teste 2", preco=20, tipo=1)

        o1 = Pedido.objects.create(solicitante=self.user, data_saida=datetime.now())
        RelacaoPedidoProduto.objects.create(pedido=o1, produto=p1, quantidade=3)
        RelacaoPedidoProduto.objects.create(pedido=o1, produto=p2, quantidade=2)

        self.assertIn(p1, o1.produtos.all())
        self.assertIn(p2, o1.produtos.all())

        self.assertEqual(o1.get_value(), 70)

        d1 = o1.descontos.create(valor=Decimal('3.34'), justificativa='so pra zoar')

        self.assertEqual(o1.get_value(), Decimal('66.66'))

        d2 = o1.descontos.create(valor=Decimal('-22.22'), justificativa='pq eu posso')

        self.assertEqual(o1.get_value(), Decimal('88.88'))

        self.assertEqual(get_user_balance(self.user), Decimal('88.88'))

        o2 = Pedido.objects.create(solicitante=self.user, data_saida=datetime.now())
        RelacaoPedidoProduto.objects.create(pedido=o2, produto=p2, quantidade=1)

        self.assertEqual(get_user_balance(self.user), Decimal('108.88'))

        # e por ultimo, testamos se o argumento de data funciona
        # corretamente
        yesterday = datetime.now() - timedelta(days=1)
        Pedido.objects.filter(pk=o1.pk).update(data_solicitacao=yesterday)
        self.assertEqual(get_user_balance(self.user, until=yesterday), Decimal('88.88'))
