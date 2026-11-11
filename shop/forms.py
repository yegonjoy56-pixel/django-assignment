
from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ("mpesa", "M-Pesa STK Push"),
        ("cash_on_delivery", "Cash on Delivery"),
        ("card", "Card Payment"),
    ]

    full_name = forms.CharField(
        max_length=150,
        label="Full Name"
    )

    phone_number = forms.CharField(
        max_length=20,
        label="Phone Number",
        help_text="Enter the phone number for delivery."
    )

    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Delivery Address"
    )

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        label="Payment Method",
        widget=forms.Select()
    )
