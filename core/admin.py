from django.contrib import admin
from .models import Beat, Profile, Cash, OrderBeat, Order, Refund, Address, Payment, UserProfile, SellersPay, Rating, MassRate,ContactCash, Contact, Withdraw, ContactProf, OrderContactProf



def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


# Register your models here.
admin.site.register(Beat)
admin.site.register(UserProfile)
admin.site.register(SellersPay)
admin.site.register(Profile)
admin.site.register(OrderBeat)
admin.site.register(Order)
admin.site.register(Refund)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Rating)
admin.site.register(MassRate)
admin.site.register(Contact)
admin.site.register(Withdraw)
admin.site.register(Cash)
admin.site.register(ContactProf)
admin.site.register(OrderContactProf)
admin.site.register(ContactCash)
