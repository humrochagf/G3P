# -*- coding: utf-8 -*-
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from src.core.models import (
    Produto, Pedido, Pagamento, Desconto, RelacaoPedidoProduto, Parceiro, User
)
from src.core.forms import DescontoInlinePedidoForm, ProdutoInlinePedidoForm, UserCreationForm


class StaffAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name')}
        ),
    )
    add_form = UserCreationForm

    def queryset(self, request):
        return super(StaffAdmin, self).queryset(request)\
                .filter(is_superuser=True)

    def save_model(self, request, obj, form, change):
        obj.is_superuser = True
        obj.is_staff = True
        obj.save()



class CustomerAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name')}
        ),
    )
    add_form = UserCreationForm

    def queryset(self, request):
        return super(CustomerAdmin, self).queryset(request)\
                .filter(is_superuser=False)

    def save_model(self, request, obj, form, change):
        obj.is_superuser = False
        obj.is_staff = True

        # TODO garantir permissões

        obj.save()


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'preco')
    search_fields = ('titulo', 'preco')
    list_filter = ('tipo',)

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
    form = ProdutoInlinePedidoForm


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

admin.site.unregister(User)
admin.site.register(User, StaffAdmin)
admin.site.register(Parceiro, CustomerAdmin)
