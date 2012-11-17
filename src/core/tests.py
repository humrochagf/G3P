# -*- coding: utf-8 -*-
from django.test import TestCase
from src.core.models import Produto


class VersionamentoProdutoTestCase(TestCase):
    def test_it_works(self):
        p1 = Produto.objects.create(titulo=u"Teste", preco=1, tipo=0)

        # alterar o título do produto não gera uma nova versão
        p1.titulo = u"Teste Alterado"
        p2 = p1.versioned_save()

        self.assertEqual((p1.codigo, p1.id), (p2.codigo, p2.id))

        # alterar o preço do produto gera uma nova versão
        p1.preco = 2
        p1v2 = p1.versioned_save()
        self.assertNotEqual((p1.codigo, p1.id), (p1v2.codigo, p1v2.id))

        # deve retornar uma lista contendo apenas as versões mais atuais
        # dos produtos, ou seja, apenas `p1v2`.
        active = Produto.objects.active()
        self.assertEqual(active.count(), 1)
        self.assertEqual(active[0].id, p1v2.id)
