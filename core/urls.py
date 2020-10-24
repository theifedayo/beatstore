from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve 
from django.conf.urls import url
from core import views
from django.contrib.auth.views import LoginView
from .views import (
    CheckoutView,
    PaymentView)



app_name = 'core'

urlpatterns = [
	path('home/', views.home, name='home'),
    path('', views.home_again, name='home-again'),
    path('logout/', views.logout_request, name='logout'),
    path('get-contacts/', views.contact_list, name='contact-list'),
    path('beat-store/', views.beat_store, name='beat-store'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('withdraw-contact/', views.withdraw_contact, name='withdraw-contact'),
    path('contact-us/', views.contact_view, name='contact'),
    path('bangare/', views.bangare, name="club"),
    path('randb/', views.randb, name="urban"),
    path('afroblues/', views.afroblues, name="dirtysouth"),
    path('afropop/', views.afropop, name="gangsta"),
    path('reggaeton/', views.reggaeton, name="reggaeton"),
    path('pop/', views.pop, name="pop"),
    path('rate/<int:pk>/', views.rate_beat, name='rate-beat'),
    path('purchased/', views.purchased, name="purchased"),
	path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile-contact/', views.contactprof_view, name='contact-prof-view'),
    path('contactprof-del/', views.contactprof_delete, name='contactprof_del'),
    path('search/', views.results, name='results'),
    path('order-summary/', views.order_summary, name='order-summary'),
    path('add-to-cart/<str:slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('my-orders/', views.my_orders, name="my-orders"),
    path('contact-orders/', views.contact_orders, name='conatct-orders'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('admin-list/', views.admin_beat_list, name='admin-beat-list'),
    path('admin-list/<str:slug>', views.admin_beat_detail, name='admin-beat-detail'),
    path('del/<str:slug>', views.admin_delete, name="admin-delete"),
    path('verify/<str:slug>', views.admin_verify, name="admin-verify"),
    path('unverify/<str:slug>', views.admin_unverify, name="admin-unverify"),
    path('<str:slug>/license/', views.license_view, name='license-view'),
    path('payment-options/', views.payment_options, name="payment-options"),
    path('upload-beat/', views.beat_form_view, name='beat-form-view'),
    path('my-beats', views.beat_list_view, name='beat-list-view'),
    path('my-beats/<str:slug>/', views.beat_detail_view, name='beat-detail-view'),
    path('<str:slug>/edit', views.beat_update_view, name='beat-update'),
    path('<str:slug>/delete', views.beat_delete_view, name='beat-delete'),
    path('process/', views.payment_process, name="process"),
    path('done/', views.payment_done, name="done"),
    path('canceled', views.payment_canceled, name='canceled'),
    path('payment/stripe/', PaymentView.as_view(), name='payment-stripe'),
    path('payment/paystack/', views.paystack_payment, name="payment-paystack"),
    path('paystack/connect/<int:pk>/', views.paystack_payment_prof, name="payment-paystack-prof"),
    path('payment/paystack/ref', views.otp_page, name="otp-page"),
    path('paystack/connect/ref', views.otp_page_prof, name="otp-page-prof"),
    path('payment/paystack/phone', views.phone_page, name="phone-page"),
    path('paystack/connect/phone', views.phone_page_prof, name="phone-page-prof"),
]

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG == True:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ]