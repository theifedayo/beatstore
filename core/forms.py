from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Beat, SellersPay, MassRate, Contact, Withdraw, ContactProf, OrderContactProf, Profile
from django_countries.fields import CountryField
from django.forms import widgets
from django_countries.widgets import CountrySelectWidget



A_CHOICES = (
    ('Y', 'I agree'),
    ('N', "No, I don't"),
)



PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('PS', 'PayStack'),
)


SKILL_CHOICES = (
    ('m', 'Musician'),
    ('p', 'Producer'),
    ('ma', 'Manager'),
    ('pro', 'PRO'),
    ('co', 'Compose'),
    ('sw', 'Songwriter'),
    ('lb', 'Label brand & Sponsor'),
    ('di', 'Director'),
    ('mo', 'Model'),
    ('pa', 'Painter'),
    ('st', 'Stylist'),
    ('ac', 'Actor'),
    ('me', 'Media'),
    ('de', 'Designer'),
    ('pg', 'Photographer'),
    ('pt', 'Poet'),
    ('bd', 'Band'),
    ('tc', 'Teacher'),
    ('dc', 'Dancer'),
    ('cm', 'Comedian'),
    ('so', 'Show Organizers'),
)



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'message']

class OTPForm(forms.Form):
    otp = forms.IntegerField()
    ref = forms.CharField(max_length=50)

class PhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=20)
    ref = forms.CharField(max_length=50)

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ['name', 'email', 'bank_name', 'amount', 'account_number']

class ContactProfForm(forms.ModelForm):
    class Meta:
        model = ContactProf
        fields = ['company_name', 'price']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'full_name','email','address','city','state','country','phone','skill']

class SignUpForm(UserCreationForm):
    profile_pic = forms.FileField()
    full_name = forms.CharField(max_length=100, help_text='Full Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    address = forms.CharField(max_length=300)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    skill = forms.ChoiceField(
        widget=forms.RadioSelect, choices=SKILL_CHOICES)


    class Meta:
        model = User
        fields = ('username',
		'email', 'password1', 'password2',)

class RateForm(forms.ModelForm):
    class Meta:
        model = MassRate
        fields = ['rate']


class BeatForm(forms.ModelForm):
    class Meta:
        model = Beat
        fields = ['beat_name','sound', 'license', 'genre1', 'mood1', 'mood2', 'price', 'thumbnail']

class PaystackForm(forms.Form):
    email = forms.EmailField()
    # amount = forms.FloatField()
    code = forms.CharField(required=True)
    account_number = forms.CharField()
    birthday = forms.DateTimeField()

class AgreementForm(forms.Form):
    agreement_choices = forms.ChoiceField(
        widget=forms.RadioSelect, choices=A_CHOICES)


class PaymentOptionForm(forms.Form):
    payment_choices = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)