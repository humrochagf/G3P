# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User
from src.core.models import Desconto


class UserCreationForm(BaseUserCreationForm):
    first_name = forms.CharField(label=u"Nome")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class DescontoInlinePedidoForm(forms.ModelForm):
    SINAL_CHOICES = (
        ('', u"----"),
        (1, u"Desconto"),
        (-1, u"Multa"),
    )
    sinal = forms.TypedChoiceField(label=u"Tipo", choices=SINAL_CHOICES, coerce=int)
    valor = forms.DecimalField(label=u"Valor")
    justificativa = forms.CharField(label=u"Justificativa")

    class Meta:
        model = Desconto
        fields = ('justificativa',)

    def __init__(self, *args, **kwargs):
        super(DescontoInlinePedidoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.valor:
            initial = {
                'sinal': -1 if self.instance.valor < 0 else 1,
                'valor': abs(self.instance.valor),
            }
            initial.update(self.initial)
            self.initial = initial

    def save(self, commit=True):
        obj = super(DescontoInlinePedidoForm, self).save(commit=False)
        obj.valor = (self.cleaned_data['valor'] * self.cleaned_data['sinal'])
        if commit:
            obj.save()
        return obj


class ProdutoInlinePedidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProdutoInlinePedidoForm, self).__init__(*args, **kwargs)
        self.fields['produto'].queryset = self.fields['produto'].queryset.active()
