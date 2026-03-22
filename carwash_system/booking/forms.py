from django import forms
from datetime import date, timedelta
from .models import Booking


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
    class Meta:
        model = Booking
        fields = [
            "name",
            "phone",
            "email",
            "car_number",
            "date",
            "time_slot",
            "wash_type",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "optional"}),
            "car_number": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.Select(attrs={"class": "form-select"}),
            "time_slot": forms.Select(attrs={"class": "form-select"}),
            "wash_type": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_date(self):
        selected = self.cleaned_data["date"]
        today = date.today()
        tomorrow = today + timedelta(days=1)

        if selected not in [today, tomorrow]:
            raise forms.ValidationError("Booking allowed only for today or tomorrow.")

        return selected
