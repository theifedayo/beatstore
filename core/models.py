from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


# Create your models here.

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

GENRE_CHOICES = (
    ('Cl', 'Club'),

    ('P', 'Pop'),
    ('RG', 'Reggaeton'),
    ('U', 'Underground'),
    ('A', 'Afro'),
    ('AP', 'Afro Pop'),
    ('AR', 'Afro Reggae'),
    ('R&B', 'Afro R&B'),
    ('AB', 'Afro Blues'),
    ('B', 'Bangare')
)

MOOD_CHOICES = (
    ('A', 'Angry'),
    ('D', 'Dark'),
    ('E', 'Epic'),
    ('F', 'Frantic'),
    ('H', 'Happy'),
    ('I', 'Inspiring'),
    ('R', 'Relaxed'),
    ('S', 'Sad'),
    ('Si', 'Silly'),
    ('So', 'Soulful'),
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


class Profile(models.Model):
    profile_pic = models.FileField(upload_to='profile-pic')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    skill = models.CharField(choices=SKILL_CHOICES, max_length=4)
    

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class ContactProf(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.IntegerField()
    company_name = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
 

class OrderContactProf(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    ordered = models.BooleanField(default=False)
    contact = models.ForeignKey(ContactProf, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username




class Beat(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True, blank=False)
    producer_name = models.CharField(max_length=45)
    beat_name = models.CharField(max_length=40)
    beat_id = models.CharField(max_length=33, blank=False, null=False, unique=True)
    sound = models.FileField()
    sound_two = models.FileField()
    license = models.TextField()
    genre1 = models.CharField(choices=GENRE_CHOICES, max_length=3)
    mood1 = models.CharField(choices=MOOD_CHOICES, max_length=2)
    mood2 = models.CharField(choices=MOOD_CHOICES, max_length=2)
    price = models.FloatField()
    verified = models.BooleanField(default=False)
    thumbnail = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return f"{self.user.username}'s {self.beat_name}, verified-{ self.verified}"

class Rating(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.beat.beat_name

class MassRate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

class SellersPay(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    withdraw = models.FloatField()

    def __str__(self):
        return self.user.username




class OrderBeat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    #beat_owner = models.Foreign(User, default=1, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f"{self.user.username} order {self.beat.beat_name}"



    def get_total_item_price(self):
        return self.beat.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    beat = models.ManyToManyField(OrderBeat)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for order_item in self.beat.all():
            total += order_item.get_total_item_price()
        return total



    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

class Contact(models.Model):
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email

class Cash(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cash = models.IntegerField()


class ContactCash(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cash = models.IntegerField()

    def __str__(self):
        return self.user.username


class Withdraw(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    bank_name = models.CharField(max_length=20)
    amount = models.IntegerField()
    account_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
