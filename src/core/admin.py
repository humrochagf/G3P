from django.contrib import admin
from src.core.models import *

admin.site.register(Pedido)
admin.site.register(Desconto)
admin.site.register(Pagamento)


class ProdutoAdmin(admin.ModelAdmin):
    search_fields = ['titulo']
    list_filter = ('tipo',)
    filter_horizontal = ('composicao',)

admin.site.register(Produto, ProdutoAdmin)
