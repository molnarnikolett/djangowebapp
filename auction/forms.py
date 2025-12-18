from decimal import Decimal
from django import forms
from .models import Item


class BidForm(forms.Form):
    amount = forms.DecimalField(
        label="Ajánlott összeg (HUF)",
        max_digits=10,
        decimal_places=0,
        min_value=1,
    )

    def __init__(self, *args, **kwargs):
        self.current_price = kwargs.pop("current_price", None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if self.current_price is not None:
            # Elvárjuk, hogy a licit SZIGORÚAN nagyobb legyen
            if amount <= self.current_price:
                raise forms.ValidationError(
                    f"A licitnek nagyobbnak kell lennie a jelenlegi árnál ({self.current_price} HUF)."
                )

        return amount

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "name",
            "category",
            "starting_price",
            "auction_time",
            "image",
        ]