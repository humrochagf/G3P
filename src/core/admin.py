from django.contrib import admin
from src.core.models import (
    Produto, Pedido, Desconto, Pagamento,
)

admin.site.register(Pedido)
admin.site.register(Desconto)
admin.site.register(Pagamento)


class ProdutoAdmin(admin.ModelAdmin):
    search_fields = ['titulo']
    list_filter = ('tipo',)
    filter_horizontal = ('composicao',)

    def save_model(self, request, obj, form, change):
        if change is True:
            return obj.versioned_save()
        else:
            return super(ProdutoAdmin, self).save_model(
                request, obj, form, change)

admin.site.register(Produto, ProdutoAdmin)
