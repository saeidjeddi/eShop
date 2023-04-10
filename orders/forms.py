from django import forms


class CortAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, label="تعداد")


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput, label='کد تخفیف')
