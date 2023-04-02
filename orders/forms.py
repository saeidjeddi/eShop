from django import forms


class CortAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, label="تعداد")
