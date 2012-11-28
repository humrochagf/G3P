# -*- coding: utf-8 -*-
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from src.core.models import (
    Produto,
    Pedido,
    Pagamento,
    Desconto,
    RelacaoPedidoProduto,
    Parceiro,
    User,
    get_user_balance
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
    list_filter = ('is_active',)
    list_display = ('first_name', 'username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name')}
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

        obj.user_permissions.add()

    #def balanco_mensal(self, obj):
    #    return - get_user_balance(obj)


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

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(ProdutoInlinePedido, self).get_readonly_fields(request, obj)
        if obj is not None:
            readonly_fields += ('preco_un', 'preco')
        return readonly_fields

    def preco_un(self, obj):
        return obj.produto.preco

    def preco(self, obj):
        return obj.produto.preco * obj.quantidade


class DescontoInlinePedido(admin.TabularInline):
    model = Desconto
    form = DescontoInlinePedidoForm


class PedidoAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_solicitacao'
    search_fields = ('id', 'solicitante__first_name')
    list_display = ['solicitante', 'data_solicitacao',
                    'data_saida', 'data_retorno', 'aprovacao']
    list_filter = ('aprovacao', 'data_saida')

    inlines = (ProdutoInlinePedido, DescontoInlinePedido)

    def queryset(self, request):
        qs = super(PedidoAdmin, self).queryset(request)
        if not request.user.is_superuser:
            return qs.filter(solicitante=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.solicitante = request.user
        return super(PedidoAdmin, self).save_model(
            request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude += ['data_retorno', 'aprovacao']
        return super(PedidoAdmin, self).get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(PedidoAdmin, self).get_readonly_fields(
                                                            request, obj)

        readonly_fields += ('solicitante',)

        if not request.user.is_superuser:
            readonly_fields += ('data_retorno', 'aprovado')

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
