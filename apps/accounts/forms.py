from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from core.constants import COUNTIES


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'Your first name',
    }))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'Your last name',
    }))
    id_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'e.g. 12345678',
    }))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'e.g. 0712 345 678',
    }))
    county = forms.ChoiceField(choices=[('', 'Select your county')] + list(COUNTIES), required=False, widget=forms.Select(attrs={
        'class': 'form-select w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'your@email.com',
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'Choose a username',
    }))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'Minimum 8 characters',
    }))
    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form-input w-full rounded-lg border border-[#dbe0e6] h-12 px-4',
        'placeholder': 'Re-enter your password',
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        if not id_number.isdigit() or len(id_number) < 6:
            raise forms.ValidationError('Enter a valid ID number (at least 6 digits).')
        return id_number

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get('password')
        cpw = cleaned.get('confirm_password')
        if pw and cpw and pw != cpw:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg '
                 'text-[#111418] focus:outline-0 focus:ring-0 border border-[#dbe0e6] bg-white '
                 'h-14 placeholder:text-[#60758a] p-[15px] text-base font-normal leading-normal',
        'placeholder': 'Your full name',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg '
                 'text-[#111418] focus:outline-0 focus:ring-0 border border-[#dbe0e6] bg-white '
                 'h-14 placeholder:text-[#60758a] p-[15px] text-base font-normal leading-normal',
        'placeholder': 'Your email address',
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg '
                 'text-[#111418] focus:outline-0 focus:ring-0 border border-[#dbe0e6] bg-white '
                 'h-14 placeholder:text-[#60758a] p-[15px] text-base font-normal leading-normal',
        'placeholder': 'Subject',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg '
                 'text-[#111418] focus:outline-0 focus:ring-0 border border-[#dbe0e6] bg-white '
                 'h-32 placeholder:text-[#60758a] p-[15px] text-base font-normal leading-normal',
        'placeholder': 'Your message...',
        'rows': 5,
    }))

    def save(self):
        from .models import AuditEntry
        AuditEntry.objects.create(
            action='contact_message',
            details=f"From: {self.cleaned_data['name']} <{self.cleaned_data['email']}>\n"
                    f"Subject: {self.cleaned_data['subject']}\n"
                    f"Message: {self.cleaned_data['message']}",
        )
