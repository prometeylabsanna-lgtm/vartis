import re

from django import forms

from .models import Lead


NAME_RE = re.compile(
    r"^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'ʼ’\-\s]{2,120}$",
)
EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')


def normalize_ua_phone(raw: str) -> str | None:
    """Повертає +380XXXXXXXXX або None, якщо формат не UA."""
    digits = re.sub(r'\D', '', (raw or '').strip())
    if digits.startswith('380') and len(digits) == 12:
        return f'+{digits}'
    if digits.startswith('0') and len(digits) == 10:
        return f'+380{digits[1:]}'
    return None


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
            'name': {'required': "Поле обов'язкове для заповнення"},
            'phone': {'required': "Поле обов'язкове для заповнення"},
            'email': {
                'required': "Поле обов'язкове для заповнення",
                'invalid': 'Введіть коректну електронну пошту',
            },
            'consent': {'required': 'Потрібна згода на обробку даних'},
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'name',
                'class': 'lead-form__input',
                'minlength': '2',
                'maxlength': '120',
                'data-validate': 'name',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'autocomplete': 'tel',
                'inputmode': 'tel',
                'placeholder': '+380 XX XXX XX XX',
                'class': 'lead-form__input',
                'data-validate': 'phone',
            }),
            'email': forms.EmailInput(attrs={
                'autocomplete': 'email',
                'inputmode': 'email',
                'placeholder': 'user@domain.com',
                'class': 'lead-form__input',
                'data-validate': 'email',
            }),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'class': 'lead-form__textarea',
            }),
            'consent': forms.CheckboxInput(attrs={
                'class': 'lead-form__checkbox',
                'data-validate': 'consent',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['consent'].required = True
        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    css = self.fields[name].widget.attrs.get('class', '')
                    if 'is-invalid' not in css.split():
                        self.fields[name].widget.attrs['class'] = f'{css} is-invalid'.strip()
                    self.fields[name].widget.attrs['aria-invalid'] = 'true'

    def clean_name(self):
        name = re.sub(r'\s+', ' ', (self.cleaned_data.get('name') or '').strip())
        if len(name) < 2:
            raise forms.ValidationError("Поле обов'язкове для заповнення")
        if not NAME_RE.match(name):
            raise forms.ValidationError(
                "Ім'я може містити лише літери, пробіл, дефіс або апостроф"
            )
        return name

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if not phone:
            raise forms.ValidationError("Поле обов'язкове для заповнення")
        normalized = normalize_ua_phone(phone)
        if not normalized:
            raise forms.ValidationError(
                'Введіть номер у форматі +380XXXXXXXXX або 0XXXXXXXXX'
            )
        return normalized

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if not email:
            raise forms.ValidationError("Поле обов'язкове для заповнення")
        if not EMAIL_RE.match(email):
            raise forms.ValidationError('Введіть коректну електронну пошту')
        return email.lower()

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise forms.ValidationError('Потрібна згода на обробку даних')
        return consent

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise forms.ValidationError('Spam detected')
        return ''
