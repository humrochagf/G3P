from django.contrib import admin
from src.core.models import (
    Produto, Pedido, Pagamento, Desconto, RelacaoPedidoProduto
)
from src.core.forms import DescontoInlinePedidoForm

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'preco')
    search_fields = ('titulo', 'preco')
    list_filter = ('tipo',)
    filter_horizontal = ('composicao',)

    def save_model(self, request, obj, form, change):
        if change is True:
            return obj.versioned_save()
        else:
            return super(ProdutoAdmin, self).save_model(
                request, obj, form, change)

    def queryset(self, request):
        return super(ProdutoAdmin, self).queryset(request).active()


class ProdutoInlinePedido(admin.TabularInline):
    model = RelacaoPedidoProduto


class DescontoInlinePedido(admin.TabularInline):
    model = Desconto
    form = DescontoInlinePedidoForm


class PedidoAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_solicitacao'
    list_display = ('__unicode__', 'solicitante', 'data_solicitacao',
                    'data_saida', 'data_retorno')
    search_fields = ('id', 'solicitante__first_name',
                     'solicitante__last_name')
    list_filter = ('data_saida', 'data_retorno')

    inlines = (ProdutoInlinePedido, DescontoInlinePedido)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(PedidoAdmin, self).get_readonly_fields(
                                                            request, obj)
        if obj is not None:
            return readonly_fields + ('data_solicitacao',)
        else:
            return readonly_fields



admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Pagamento)
