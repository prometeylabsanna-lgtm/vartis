import re

from django import forms

from .models import Lead


PHONE_RE = re.compile(r'^[\d\s+\-()]{7,20}$')


class LeadForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'tabindex': '-1',
        'autocomplete': 'off',
        'aria-hidden': 'true',
        'class': 'lead-form__honeypot',
    }))

    class Meta:
        model = Lead
        fields = ('name', 'phone', 'email', 'message', 'consent')
        error_messages = {
            'name': {'required': "Вкажіть ім'я"},
            'phone': {'required': 'Вкажіть телефон'},
            'email': {'required': 'Вкажіть email', 'invalid': 'Вкажіть коректний email'},
            'consent': {'required': 'Потрібна згода на обробку даних'},
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'name',
                'class': 'lead-form__input',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'autocomplete': 'tel',
                'placeholder': '+380',
                'class': 'lead-form__input',
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'email',
                'class': 'lead-form__input',
            }),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'class': 'lead-form__textarea',
            }),
            'consent': forms.CheckboxInput(attrs={
                'class': 'lead-form__checkbox',
            }),
        }

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Вкажіть ім'я")
        return name

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if not PHONE_RE.match(phone):
            raise forms.ValidationError('Вкажіть коректний телефон')
        return phone

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise forms.ValidationError('Потрібна згода на обробку даних')
        return consent

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise forms.ValidationError('Spam detected')
        return ''
