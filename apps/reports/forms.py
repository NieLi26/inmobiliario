from typing import Any, Dict
from django import forms
from .models import OperationBuyHistory


class OperationBuyHistoryFirstForm(forms.ModelForm):
    # signature_purchase_sale_agreement = forms.DateField(widget=forms.DateInput())

    # publication = forms.CharField(widget=forms.HiddenInput())

    # message = forms.CharField(label="Mensaje", widget=forms.Textarea(attrs={
    #     'rows': '3'
    # }))

    # phone = forms.CharField(label='Télefono', widget=(forms.TextInput(attrs={
    #     'x-mask': '999999999',
    #     'placeholder': 'Ej. 965337823'
    # })))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if self.errors.get(field):
    #             self.fields[field].widget.attrs['class'] = 'focus:outline-none border border-red-500 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['signature_purchase_sale_agreement'].widget = forms.DateInput(attrs={"type": "date"})

    class Meta:
        model = OperationBuyHistory
        fields = ('total', 'purchase_sale_advance', 'signature_purchase_sale_agreement', 'purchase_sale_agreement')

    def clean_total(self):
        total = self.cleaned_data['total']
        if total != '' and total <= 0:
            msg = 'Total debe ser Mayora 0'
            raise forms.ValidationError(msg)
        return total

    def clean(self):
        cleaned_data = super().clean()
        purchase_sale_advance = cleaned_data.get('purchase_sale_advance')
        purchase_sale_agreement = cleaned_data.get('purchase_sale_agreement')
        signature_purchase_sale_agreement = cleaned_data.get('signature_purchase_sale_agreement')
        if purchase_sale_advance or purchase_sale_agreement or signature_purchase_sale_agreement:
            if not purchase_sale_advance:
                msg = 'El Valor del Anticipo debe ser Mayor a 0'
                self.add_error('purchase_sale_advance', msg)
            if not purchase_sale_agreement:
                msg = 'Debe subir Documento de Promesa de Compra/Venta'
                self.add_error('purchase_sale_agreement', msg)
            if not signature_purchase_sale_agreement:
                msg = 'Debe Indicar la Fecha de Firma de Promesa de Compra/Venta'
                self.add_error('signature_purchase_sale_agreement', msg)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.purchase_sale_advance and instance.purchase_sale_agreement and instance.signature_purchase_sale_agreement:
            instance.has_promise = True
        if commit:
            instance.save()
        return instance


class OperationBuyHistorySecondForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_list = ['sales_document', 'signature_sales_document']
        for field in required_list:
            self.fields[field].required = True

        self.fields['signature_sales_document'].widget = forms.DateInput(attrs={"type": "date"})

    class Meta:
        model = OperationBuyHistory
        fields = (
            'signature_sales_document',
            'sales_document'
        )

    # def clean_signature_sales_document(self):
    #     signature_sales_document = self.cleaned_data['signature_sales_document']
    #     if not signature_sales_document:
    #         msg = 'Fecha Firma Contrato de Compra/Venta es Obligatoria'
    #         raise forms.ValidationError(msg)
    #     return signature_sales_document

    # def clean_sales_document(self):
    #     sales_document = self.cleaned_data['sales_document']
    #     if not sales_document:
    #         msg = 'Contrato de Compra/Venta es Obligatoria'
    #         raise forms.ValidationError(msg)
    #     return sales_document

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_completed = True
        if commit:
            instance.save()
        return instance


class OperationBuyHistoryUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['publication'].widget = forms.HiddenInput()
        date_list = ['signature_purchase_sale_agreement', 'signature_sales_document']
        for field in date_list:
            self.fields[field].widget = forms.DateInput(attrs={"type": "date"}, format='%Y-%m-%d')

    class Meta:
        model = OperationBuyHistory
        fields = (
            'total',
            'purchase_sale_advance',
            'signature_purchase_sale_agreement',
            'purchase_sale_agreement',
            'signature_sales_document',
            'sales_document'
        )

    def clean_total(self):
        total = self.cleaned_data['total']
        if total != '' and total <= 0:
            msg = 'Total debe ser Mayora 0'
            raise forms.ValidationError(msg)
        return total

    def clean(self):
        cleaned_data = super().clean()
        purchase_sale_advance = cleaned_data.get('purchase_sale_advance')
        purchase_sale_agreement = cleaned_data.get('purchase_sale_agreement')
        signature_purchase_sale_agreement = cleaned_data.get('signature_purchase_sale_agreement')
        if purchase_sale_advance or purchase_sale_agreement or signature_purchase_sale_agreement:
            if not purchase_sale_advance:
                msg = 'El Valor del Anticipo debe ser Mayor a 0'
                self.add_error('purchase_sale_advance', msg)
            if not purchase_sale_agreement:
                msg = 'Debe subir Documento de Promesa de Compra/Venta'
                self.add_error('purchase_sale_agreement', msg)
            if not signature_purchase_sale_agreement:
                msg = 'Debe Indicar la Fecha de Firma de Promesa de Compra/Venta'
                self.add_error('signature_purchase_sale_agreement', msg)

        sales_document = cleaned_data.get('sales_document')
        signature_sales_document = cleaned_data.get('signature_sales_document')
        if sales_document or signature_sales_document:
            if not sales_document:
                msg = 'Debe subir Documento de Contrato de Compra/Venta'
                self.add_error('sales_document', msg)
            if not signature_sales_document:
                msg = 'Debe Indicar la Fecha de Firma de Contrato de Compra/Venta'
                self.add_error('signature_sales_document', msg)
        return cleaned_data

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if instance.purchase_sale_advance and instance.purchase_sale_agreement and instance.signature_purchase_sale_agreement:
    #         instance.has_promise = True
    #     if commit:
    #         instance.save()
    #     return instance
