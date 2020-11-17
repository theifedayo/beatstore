from django.shortcuts import render, get_object_or_404
from .forms import (SignUpForm, BeatForm, AgreementForm, PaymentForm, 
                CheckoutForm, PaymentOptionForm, PaystackForm,
                OTPForm, RateForm, PhoneForm, ContactForm, WithdrawForm,
                ContactProfForm, ProfileForm)
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Profile, Beat, Order, OrderBeat, Address, UserProfile, Rating, MassRate, Withdraw, Cash, ContactProf, OrderContactProf, ContactCash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from pydub import AudioSegment
import os
from django.conf import settings
import time
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import stripe
import requests
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import yagmail





stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.


def logout_request(request):
    logout(request)
    return redirect("/")

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid



###############################
def home_again(request):
    beat = Beat.objects.filter(verified=True)
    items = Beat.objects.filter(verified=True).order_by('-timestamp')
    relaxed = Beat.objects.filter(Q(verified=True) & Q(mood1='R'))
    users = items
    # try:
    #     contact = ContactProf.objects.get(user=request.user)
    #     template_name = 'core/home_again.html'
    #     context = {'beat': beat, 'users': users, 'relaxed': relaxed, 'contact': contact}
    #     return render(request, template_name, context)
	    
    # except ContactProf.DoesNotExist:

	   #  relaxed = Beat.objects.filter(Q(verified=True) & Q(mood1='R'))
	   #  print(relaxed,'-----------------------------------')
    page = request.GET.get('page', 1)
    paginator = Paginator(items, 15)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    template_name = 'core/home_again.html'
    context = {'beat': beat, 'users': users, 'relaxed': relaxed}
    return render(request, template_name, context)



def base(request):
    try:
        contact = ContactProf.objects.get(user=request.user)
        template_name = 'core/base.html'
        context = {'contact': contact}
        return render(request, template_name, context)
	    
    except ContactProf.DoesNotExist:
    	template_name = 'core/base.html'
    	context = {}
    	return render(request, template_name, context)


def pop(request):
    beat = Beat.objects.filter(Q(verified=True) & Q(genre1='P')).order_by('-timestamp')
    template_name = 'core/pop.html'
    context = {'beat': beat}
    return render(request, template_name, context)

def reggaeton(request):
    beat = Beat.objects.filter(Q(verified=True) & Q(genre1='RG')).order_by('-timestamp')
    template_name = 'core/reggaeton.html'
    context = {'beat': beat}
    return render(request, template_name, context)

def afropop(request):
    beat = Beat.objects.filter(Q(verified=True) & Q(genre1='AP')).order_by('-timestamp')
    template_name = 'core/gangsta.html'
    context = {'beat': beat}
    return render(request, template_name, context)


def afroblues(request):
    beat = Beat.objects.filter(Q(verified=True) & Q(genre1='AB')).order_by('-timestamp')
    template_name = 'core/afroblues.html'
    context = {'beat': beat}
    return render(request, template_name, context)

def randb(request):
    beat = Beat.objects.filter(Q(verified=True) & Q(genre1='R&B')).order_by('-timestamp')
    template_name = 'core/club.html'
    context = {'beat': beat}
    return render(request, template_name, context)

def bangare(request):
    beat = Beat.objects.filter(Q(verified=True) & Q(genre1='B')).order_by('-timestamp')
    template_name = 'core/urban.html'
    context = {'beat': beat}
    return render(request, template_name, context)




def rate_beat(request, pk):
    beat = get_object_or_404(Rating, pk=pk)
    beat_again = Rating.objects.filter(pk=beat.pk)
    for a in beat_again:
        the_beat = a.beat
        
    mass_rate = MassRate.objects.filter(beat=the_beat)
    users_list = []
    for a in mass_rate:
        present_user = a.user
        users_list.append(present_user)
    if request.user in users_list:
        return redirect('/')
    present_rate = beat.rate
    total = 0
    for a in mass_rate:
        total += a.rate
    form = RateForm(request.POST)
    if form.is_valid():
        no_of_rates = mass_rate.count()+1
        print(no_of_rates)
        obj = form.save(commit=False)
        obj.beat = the_beat
        obj.user = request.user
        obj.rate = int(form.cleaned_data['rate'])
        if obj.rate > 5:
            template_name = 'core/rate_form.html'
            form = RateForm()
            context = {'form': form, 'message': "Sorry, rating can't be more than 5"}
            return render(request, template_name, context)
        if obj.rate < 0:
            template_name = 'core/rate_form.html'
            form = RateForm()
            context = {'form': form, 'message': "Sorry, rating can't be less than 0"}
            return render(request, template_name, context)
        obj.save()

        avg_rate = int(int(obj.rate+total)/no_of_rates)
        beat_again.update(rate=avg_rate)
        return redirect('/')
    template_name = 'core/rate_form.html'
    form = RateForm()
    context = {'form': form,}
    return render(request, template_name, context)
###############################
###############################

def home(request):
    beats = Beat.objects.filter(verified=True).order_by('-timestamp')
    lis = []
    k=[]
    for a in beats:
        lis.append(a)

    for i in range(len(lis)):
        print(lis[i])
        rating =Rating.objects.filter(Q(beat=lis[i]))
        
    template_name = 'core/home_again.html'
    context = {'beats': beats, 'rating': rating}
    return render(request, template_name, context)





def results(request):
    template_name = 'core/results.html'
    query = request.GET.get('q')
    beats = Beat.objects.filter(Q(beat_name__icontains=query) & Q(verified=True)).order_by('-timestamp')
    context = {
        "beats":beats,
        "query": query
    }
    return render(request, template_name, context)


def results_prof(request):
    template_name = 'core/results_prof.html'
    query = request.GET.get('q')
    profile = Profile.objects.filter(Q(skill__icontains=query))
    context = {
        "profile":profile,
        "query": query
    }
    return render(request, template_name, context)


@login_required
def beat_form_view(request):
    i = Beat.objects.all()
    a = i.count() + 1#THIS SHOULD BE THE ITEM ID
    # beat_again_form = BeatAgainForm(request.POST or None,  request.FILES or None)
    if request.method == "POST":
        beat_form = BeatForm(request.POST or None,  request.FILES or None)
        if beat_form.is_valid():
            obj = beat_form.save(commit=False)
            csrf_slug = request.POST.get('csrfmiddlewaretoken')
            obj.slug = csrf_slug[:20:-2]
            obj.beat_id = a
            obj.user = request.user
            naira = beat_form.save()
            naira.refresh_from_db()
            # time.sleep(4)

            file_name = str(request.FILES.get('sound'))
            beat_name2 = request.POST.get('beat_name')



            # file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            naira.save()
            rating = Rating()
            rating.beat = obj
            rating.rate = 0
            rating.save()

            return redirect('core:beat-detail-view', slug=obj.slug)
        else:
            beat_form = BeatForm()
            return render( request, 'core/beat_form.html', {'beat_form':beat_form})

    else:
        beat_form = BeatForm()
        return render( request, 'core/beat_form.html', {'beat_form':beat_form})


#Signup view
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None,  request.FILES or None)
        if form.is_valid():
            u_email = str(request.POST.get('email'))
            print(u_email)
            if '@' not in u_email:
                email_error = 'Email is not valid'
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'email_error': email_error})

            user = form.save()
            user.refresh_from_db()
            user.profile.profile_pic = request.FILES.get('profile_pic')

            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.skill = form.cleaned_data.get('skill')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            yag = yagmail.SMTP("afrobeat1236@gmail.com", "afrobeat2020")

            html_msg = """

            <p><h4>You have successfuly created your AfroBeat Account
                Thank you for signing up on Afro Beat.</h4></p>
            """

            yag.send(request.user.email, "Welcome to AfroBeat NG", html_msg)
            return redirect('/')
        else:
            #Error messages for username
            u_name_list = []
            u_name = request.POST.get('username')
            u_name_obj = User.objects.filter(Q(username=u_name))
            if u_name_obj.exists():
                name_exists = 'Username already exists'
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'name_exists': name_exists})

            #Error messages for email
            u_email = str(request.POST.get('email'))
            print(u_email)
            
            if '@' not in u_email:
                print('baller')
            else:
                print('wrong')
            #Error messages for password
            if len(request.POST.get('password1')) < 8:
                too_short_password = "Password characters shouldn't be less than 8"
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'too_short':too_short_password}) 
            if request.POST.get('password1') != request.POST.get('password2'):
                not_the_same_password = 'Passwords not the same'
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form':form,'not_the_same_password': not_the_same_password}) 

    else:
        form = SignUpForm()
        return render(request, 'core/signup.html', {'form':form}) 













def contact_list(request):
    users = ContactProf.objects.all().order_by('-timestamp')
    template_name = 'core/contacts_list.html'
    context = { 'users': users }
    return render(request, template_name, context)

def contactprof_view(request):
    form = ContactProfForm(request.POST)
    if form.is_valid():
        try:
            cash = ContactProf.objects.get(user=request.user)
            message = "Contact Already created"
            form = ContactProfForm()
            return render( request, 'core/contactprof.html', {'form':form, "message": message})
        except ContactProf.DoesNotExist:
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('/profile')
    else:
        form = ContactProfForm()
        return render( request, 'core/contactprof.html', {'form':form})

def contactprof_delete(request):
    cont = ContactProf.objects.get(user=request.user)
    if request.method == 'GET':
        cont.delete()
        return redirect('/profile')


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    try:
        cash = ContactProf.objects.get(user=request.user)
        template_name = 'core/profile.html'
        context = { 'profile': profile,'cash': cash}
        return render(request, template_name, context)
    except ContactProf.DoesNotExist:
        template_name = 'core/profile.html'
        context = { 'profile': profile }
        return render(request, template_name, context)

@login_required
def edit_profile(request):
    
    prof = Profile.objects.get(user=request.user)
    if prof.user != request.user:
        return redirect('/profile')
    form = ProfileForm(request.POST or None,request.FILES or None, instance=prof)
    instance=prof
    if form.is_valid():
        form.save()
        return redirect('/profile')

    template_name = "core/edit_profile.html"
    context = {"form": form, "instance": instance}
    return render(request, template_name, context)


@staff_member_required
def admin_beat_list(request):
    beats = Beat.objects.all().order_by('-timestamp')
    template_name = "core/admin_list.html"
    context = {
        "beats": beats
    }
    return render(request, template_name, context)


@staff_member_required
def admin_beat_detail(request, slug):
    beat= get_object_or_404(Beat, slug=slug)
    template_name = 'core/admin_detail.html'
    context = {
        'beat': beat
    }
    return render(request, template_name, context)

@staff_member_required
def admin_delete(request, slug):
    beat = get_object_or_404(Beat, slug=slug)
    if request.method == 'GET':
        beat.delete()
        return redirect('/admin-list')

@staff_member_required
def admin_verify(request, slug):
    beat = get_object_or_404(Beat, slug=slug)
    up_beat = Beat.objects.filter(slug=slug)
    if request.method == 'GET':
        up_beat.update(verified=True)
        return redirect('/admin-list')

@staff_member_required
def admin_unverify(request, slug):
    beat = get_object_or_404(Beat, slug=slug)
    up_beat = Beat.objects.filter(slug=slug)
    if request.method == 'GET':
        up_beat.update(verified=False)
        return redirect('/admin-list')



@login_required
def my_orders(request):
    beat = Beat.objects.filter(user=request.user).order_by('-timestamp')
    li = []
    k=[]
    for a in beat:
        li.append(a)
        for i in range(len(li)):
            # print(li[i])
            order_beat = OrderBeat.objects.filter(Q(beat=li[i]) & Q(ordered=True)).order_by('-timestamp')
        ds = order_beat
        print(ds)

        for r in ds:
            # print(r)
            k.append(r)
        uni = list(set(k))
        
        if uni:
            dp = k
            total = 0
            for a in dp:
                beat_price = int(a.beat.price - (0.3*a.beat.price))
                total += beat_price

            try:
                cash = Cash.objects.get(user=request.user)
                cash_for_me = Cash.objects.filter(user=request.user) 
                for a in cash_for_me:
                    mine = a.cash  
                context = {'order_beat': uni, 'total': mine}
                return render(request, 'core/orders.html', context)

            except Cash.DoesNotExist:
                obj_ref = Cash(user=request.user)
                obj_ref = Cash.objects.create(user=request.user, cash=total)
            
            
            context = {'order_beat': uni}
            return render(request, 'core/orders.html', context)
    non = "No order at the moment"
    context = {
        'non': non
    }
    return render(request, 'core/orders.html', context)
        

################


def beat_store(request):
    beats = Beat.objects.all().order_by('-timestamp')
    template_name = 'core/beat_store.html'
    context = {'beats': beats}
    return render(request, template_name, context)

@login_required
def beat_list_view(request):
    beats = Beat.objects.filter(user=request.user)
    template_name = 'core/beat_list.html'
    context = {'beats': beats}
    return render(request, template_name, context)


@login_required
def beat_detail_view(request, slug):
    beat= get_object_or_404(Beat, slug=slug)
    beats = Beat.objects.filter(slug=slug)
    for a in beats:
        file_name = str(a.sound)###########
    file_path = "media/" 
    #start time and endtime for sound two
    startMin = 0
    startSec = 00

    endMin = 0
    endSec = 15

    # Time to miliseconds
    startTime = startMin*60*1000+startSec*1000
    endTime = endMin*60*1000+endSec*1000

    # Opening file and extracting segment
    song = AudioSegment.from_mp3(file_path + file_name)
    extract = song[startTime:endTime]
    fil = Beat.objects.filter(slug=slug)

    extract.export(file_path+file_name[1:], format="mp3")

    fil.update(sound_two = file_name[1:])

    template_name = 'core/beat_detail.html'
    context = {
        'beat': beat
    }
    return render(request, template_name, context)

@login_required
def beat_update_view(request, slug):
    beat= get_object_or_404(Beat, slug=slug)
    if beat.user != request.user:
        return redirect('/')
        #response = HttpResponse("You can't Update this. This isn't your journal notes")
        #response.status.code = 403
        #return response
    form = BeatForm(request.POST or None,request.FILES or None, instance=beat)
    instance=beat
    if form.is_valid():
        form.save()
        return redirect('/my-beats')

    template_name = "core/beat_update.html"
    context = {"form": form, "instance": instance}
    return render(request, template_name, context)






@login_required
def beat_delete_view(request, slug):
    template_name = 'core/item_delete.html'
    beat = get_object_or_404(Beat, slug=slug)
    if beat.user != request.user:
        return redirect('/')
        #response = HttpResponse("You can't delete this. This isn't your journal notes")
        #response.status.code = 403
        #return response
    if request.method == 'GET':
        beat.delete()
        return redirect('/my-beats')


def contact_view(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.user = request.user
        obj.save()
        return redirect('/')
    else:
        form = ContactForm()
        return render( request, 'core/contact.html', {'form':form})




@login_required
def license_view(request, slug):
    license = get_object_or_404(Beat, slug=slug)
    form = AgreementForm(request.POST or None,  request.FILES or None)
    if form.is_valid():
        agreement_choices = form.cleaned_data.get('agreement_choices')

        if agreement_choices == 'N':
            return redirect('/', agreement_choices="No, I don't")
        elif agreement_choices == 'Y':
            return redirect("core:add-to-cart", slug=slug)#, agreement_choices='I agree')
    else:  
        template_name = 'core/license.html'
        form = AgreementForm()
        context = {
            'license': license,
            'form': form
        }
        return render(request, template_name, context)


@login_required
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order_beat = OrderBeat.objects.filter(user=request.user, ordered=False)
        context = {
            'object': order,
            'order_beat': order_beat
        }
        print(order.get_total())
        return render(request, 'core/order_summary.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("/")




@login_required
def payment_options(request):
    form = PaymentOptionForm(request.POST or None,  request.FILES or None)
    if form.is_valid():
        payment_choices = form.cleaned_data.get('payment_choices')

        if payment_choices == 'PS':
            return redirect('/payment/paystack', payment_choices="Paystack")
        elif payment_choices == 'S':
            return redirect('/payment/stripe', payment_choices="Stripe")
        elif payment_choices == 'P':
            return redirect('/process', payment_choices='Paypal')
    else:  
        template_name = 'core/payment_options.html'
        form = PaymentOptionForm()
        context = {
            'form': form
        }
        return render(request, template_name, context)

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Beat, slug=slug)
    order_item, created = OrderBeat.objects.get_or_create(
        beat=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.beat.filter(beat__slug=item.slug).exists():
            # order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item is already in cart.")
            return redirect("core:order-summary")
        else:
            order.beat.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.beat.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Beat, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.beat.filter(beat__slug=item.slug).exists():
            order_item = OrderBeat.objects.filter(
                beat=item,
                user=request.user,
                ordered=False
            )[0]
            order.beat.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:license-view", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Beat, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


class CheckoutView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                # 'couponform': CouponForm(),
                'order': order,
                'fee': order.get_total()
                # 'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "core/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")
                return redirect('/payment-options')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


@csrf_exempt
def payment_done(request):
    order = Order.objects.filter(user=request.user, ordered=False).update(ordered=True)
    order_beat = OrderBeat.objects.filter(user=request.user).update(ordered=True)
    return render(request, 'core/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'core/canceled.html')


@login_required
def payment_process(request):
    items = Beat.objects.all()
    ors = Order.objects.filter(user=request.user)
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.2f' % order.get_total(),#.quantize(Decimal('.01')),
            'item_name': 'Order {}'.format(order.id),
            'invoice': str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('core:done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('core:canceled')),
        }

    


        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'core/process.html', {'order': order, 'form':form})
    except ObjectDoesNotExist:
        return redirect('/')


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        # if order.billing_address:
        context = {
            'order': order,
            'fee': order.get_total(),
            # 'DISPLAY_COUPON_FORM': False,
            'STRIPE_PUBLIC_KEY' : settings.STRIPE_SECRET_KEY
        }
        #     userprofile = self.request.user.userprofile
        #     if userprofile.one_click_purchasing:
        #         # fetch the users card list
        #         cards = stripe.Customer.list_sources(
        #             userprofile.stripe_customer_id,
        #             limit=3,
        #             object='card'
        #         )
        #         card_list = cards['data']
        #         if len(card_list) > 0:
        #             # update the context with the default card
        #             context.update({
        #                 'card': card_list[0]
        #             })
        return render(self.request, "core/payment.html", context)
        # else:
        #     messages.warning(
        #         self.request, "You have not added a billing address")
        #     return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)

        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            # token = request.GET['stripeToken']
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')
            print(token,'##################################################')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()
                order = Order.objects.filter(user=request.user, ordered=False).update(ordered=True)
                order_beat = OrderBeat.objects.filter(user=request.user).update(ordered=True)

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/payment/stripe/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/payment/stripe/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/payment/stripe/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/payment/stripe/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/payment/stripe/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/payment/stripe/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/payment/stripe/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


@login_required
def paystack_payment(request):
    form = PaystackForm(request.POST)
   # If token was already acquired, redirect to home page
   # if request.session.get('api_token', False):
   #      return HttpResponseRedirect(reverse('index'))
   
   # Get username and password from posted data, authenticate and
   # if successful save api token to session
    order = Order.objects.get(user=request.user, ordered=False)
    fee = order.get_total()
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            code = request.POST.get('code')
            account_number = request.POST.get('account_number')
            birthday = request.POST.get('birthday')
            data = {'email': email, 
                    'amount': str(order.get_total()*1000),
                    'bank': {
                        "code": code,
                        "account_number": account_number
                    },
                    'birthday': birthday}
            headers = {"Authorization" : "Bearer sk_test_49bbe885dc33ee12e07e887c9cf818e69c0ca690",
                            "Content-type": "application/json" }
            r = requests.post('https://api.paystack.co/charge',
                headers = headers, 
                data= json.dumps(data))
            r_text = r.text
            ref = r_text[83:98]
            print(r.text)
            print(data)
            if r.status_code == 200:

                context = {
                    'ref': ref,
                }
                return render(request, 'core/paystack_reference.html', context)

            else:
                print(r,'code....................')
                messages.error(request, 'Authentication failed')
                return redirect('/')
    else:
        form = PaystackForm()
        context = { 'form': form, 'fee': fee}
        return render(request, 'core/paystack.html', context)


@login_required
def otp_page(request):
    form = OTPForm(request.POST)
    if form.is_valid():
        otp = request.POST.get('otp')
        reference = request.POST.get('ref')
        data = {
            "otp": otp,
            "reference": reference
        }
        headers = {"Authorization" : "Bearer sk_test_49bbe885dc33ee12e07e887c9cf818e69c0ca690",
                "Content-type": "application/json" }
        s = requests.post('https://api.paystack.co/charge/submit_otp',
            headers = headers, 
            data= json.dumps(data))
        print(data)
        print(s.text)
        return redirect('/payment/paystack/phone')
    context = {
        'form': form
    }
    return render(request, 'core/otp_page.html', context)

@login_required
def phone_page(request):
    form = PhoneForm(request.POST)
    if form.is_valid():
        phone = request.POST.get('phone_number')
        reference = request.POST.get('ref')
        data = {
            "phone": phone,
            "reference": reference
        }
        headers = {"Authorization" : "Bearer sk_test_49bbe885dc33ee12e07e887c9cf818e69c0ca690",
                "Content-type": "application/json" }
        s = requests.post('https://api.paystack.co/charge/submit_phone',
            headers = headers, 
            data= json.dumps(data))
        print(data)
        print(s.text)
        if s.status_code == 200:
            order = Order.objects.filter(user=request.user, ordered=False).update(ordered=True)
            order_beat = OrderBeat.objects.filter(user=request.user).update(ordered=True)
            
            # for s in order:
            #     s.update(ordered=True)
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'core/phone_page.html', context)





@login_required
def purchased(request):
    order_beat = OrderBeat.objects.filter(user=request.user, ordered=True)
    order_contact = OrderContactProf.objects.filter(user=request.user, ordered=True)
    template_name = 'core/purchased.html'
    context = {'order_beat': order_beat, 'order_contact': order_contact}
    return render(request, template_name, context)

@login_required
def withdraw(request):
    cash = Cash.objects.get(user=request.user) 
    my_cash = Cash.objects.filter(user=request.user) 
    for a in my_cash:
        total = a.cash
    form = WithdrawForm(request.POST or None)
    if form.is_valid():
        amount = int(request.POST.get('amount'))
        if amount > total:
            message = 'Amount entered is more than what you have'
            template_name = "core/withdraw.html"
            context = {"form": form, 'message': message}
            return render(request, template_name, context)

        amount_left = total - amount
        cash_for_me = Cash.objects.filter(Q(user=request.user))

        amount_fee = cash_for_me.update(cash=amount_left)
        form.save()
        return redirect('/profile')

    template_name = "core/withdraw.html"
    context = {"form": form}
    return render(request, template_name, context)

def beatstore(request):
    beat = Beat.objects.all().order_by('-timestamp')
    template_name = 'core/beatstore.html'
    context = {'beat': beat}
    return render(request, template_name, context)

@login_required
def paystack_payment_prof(request, pk):
    form = PaystackForm(request.POST)
    contact = get_object_or_404(ContactProf, pk=pk)
    order = OrderContactProf.objects.get_or_create(user=request.user, contact=contact, ordered=False)
 
    m = contact.user.profile.phone
    fee = contact.price

    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get('email')
            code = request.POST.get('code')
            account_number = request.POST.get('account_number')
            birthday = request.POST.get('birthday')
            data = {'email': email, 
                    'amount': str(fee*1000),
                    'bank': {
                        "code": code,
                        "account_number": account_number
                    },
                    'birthday': birthday}
            headers = {"Authorization" : "Bearer sk_test_49bbe885dc33ee12e07e887c9cf818e69c0ca690",
                            "Content-type": "application/json" }
            r = requests.post('https://api.paystack.co/charge',
                headers = headers, 
                data= json.dumps(data))
            r_text = r.text
            ref = r_text[83:98]
            print(r.text)
            print(data)
            if r.status_code == 200:

                context = {
                    'ref': ref,
                }
                return render(request, 'core/paystack_reference_prof.html', context)

            else:
                print(r,'code....................')
                messages.error(request, 'Authentication failed')
                return redirect('/')
    else:
        form = PaystackForm()
        context = { 'form': form, 'fee': fee}
        return render(request, 'core/paystack2.html', context)


@login_required
def otp_page_prof(request):
    form = OTPForm(request.POST)
    if form.is_valid():
        otp = request.POST.get('otp')
        reference = request.POST.get('ref')
        data = {
            "otp": otp,
            "reference": reference
        }
        headers = {"Authorization" : "Bearer sk_test_49bbe885dc33ee12e07e887c9cf818e69c0ca690",
                "Content-type": "application/json" }
        s = requests.post('https://api.paystack.co/charge/submit_otp',
            headers = headers, 
            data= json.dumps(data))
        print(data)
        print(s.text)
        return redirect('/paystack/connect/phone')
    context = {
        'form': form
    }
    return render(request, 'core/otp_page_prof.html', context)

@login_required
def phone_page_prof(request):
    form = PhoneForm(request.POST)
    if form.is_valid():
        phone = request.POST.get('phone_number')
        reference = request.POST.get('ref')
        data = {
            "phone": phone,
            "reference": reference
        }
        headers = {"Authorization" : "Bearer sk_test_49bbe885dc33ee12e07e887c9cf818e69c0ca690",
                "Content-type": "application/json" }
        s = requests.post('https://api.paystack.co/charge/submit_phone',
            headers = headers, 
            data= json.dumps(data))
        print(data)
        print(s.text)
        if s.status_code == 200:
            order = OrderContactProf.objects.filter(user=request.user, ordered=False).update(ordered=True)
            
            
            # for s in order:
            #     s.update(ordered=True)
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'core/phone_page.html', context)


@login_required
def contact_orders(request):
	try:
	
	    contact = ContactProf.objects.get(user=request.user)
	    con = ContactProf.objects.filter(user=request.user)
	    for a in con:
	        cont = a
	        print(cont,'-------------')
	    contact = OrderContactProf.objects.filter(Q(ordered=True) & Q(contact=cont))
	    total = 0
	    for a in contact:
	        total += a.contact.price
	    print(total)
	    try:
	        contactcash = ContactCash.objects.get(user=request.user)
	        cash_for_me = ContactCash.objects.filter(user=request.user) 
	        for a in cash_for_me:
	            mine = a.cash  
	        context = {'contact': contact, 'total': mine}
	        return render(request, 'core/contact_orders.html', context)

	    except ContactCash.DoesNotExist:
	        obj_ref = ContactCash(user=request.user)
	        obj_ref = ContactCash.objects.create(user=request.user, cash=total)
	        context = {'contact': contact}
	        return render(request, 'core/contact_orders.html', context)
	except ContactProf.DoesNotExist:
		message = "Your contact is not for sale, go to profile to set it if interested"
		context = {'message': message}
		return render(request, 'core/contact_orders.html', context)

@login_required
def withdraw_contact(request):
    cash = ContactCash.objects.get(user=request.user) 
    my_cash = ContactCash.objects.filter(user=request.user) 
    for a in my_cash:
        total = a.cash
    total = int(total-(0.3*total))
    form = WithdrawForm(request.POST or None)
    if form.is_valid():
        amount = int(request.POST.get('amount'))
        if amount > total:
            message = 'Amount entered is more than what you have'
            template_name = "core/withdraw.html"
            context = {"form": form, 'message': message}
            return render(request, template_name, context)

        amount_left = total - amount
        cash_for_me = ContactCash.objects.filter(Q(user=request.user))

        amount_fee = cash_for_me.update(cash=amount_left)
        form.save()
        return redirect('/profile')

    template_name = "core/withdraw_contact.html"
    context = {"form": form}
    return render(request, template_name, context)
