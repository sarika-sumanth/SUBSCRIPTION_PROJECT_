from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, LoginForm, SubscriptionForm
from .models import BillingPlan, CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('billing_plans')  # Redirect to the plans page after successful registration
        else:
            print(form.errors)  # Print form errors to identify the cause of validation failure
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            print("HAi")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                #print('User is authenticated:', user.is_authenticated)  # Debug statement
                return redirect('billing_plans')  # Redirect to the plans page after login
            else:
                # User credentials are not valid, show an error message
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def billing_plans(request):
   plans = [
        {
            'name': 'Plan A',
            'regular_yearly_price': 100,
            'regular_monthly_price': 10,
            'video_quality': 'HD',
            'resolution': '1080p',
            'devices': 2,
            'screens': 2,
        },
        # Add more plans here
    ]
   return render(request, 'billing_plans.html', {'plans': plans})

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            billing_plan = form.cleaned_data['billing_plan']
            billing_interval = form.cleaned_data['billing_interval']
            user = request.user
            user.billing_plan = billing_plan
            user.billing_interval = billing_interval
            user.save()
            return redirect('payment')  # Redirect to the payment page
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})

# Implement the payment view and template in Step 8
# Implement the subscription_details view and template in Step 10
# Implement the cancel_subscription view in Step 11
# subscriptions/views.py




def show_plans(request):
    plans = BillingPlan.objects.all()
    if request.method == 'POST':
        # Implement plan selection and subscription creation using Stripe here
        pass
    return render(request, 'BillingPlan.html', {'plans': plans})

def show_selected_plan(request):
    # Implement displaying the selected plan details here
    pass

def cancel_subscription(request):
    # Implement canceling the selected plan subscription here
    pass


# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = 'sk_test_51NbmUnSDi0uSGhnZVBD9AsabWQav3gH4h5Fea97c5mz52zhkVZCunbhuYo7ZHwsbV8aGQE32eauAwhbppMltnp9u00eJoGVGc5'  # Replace with your actual Stripe secret key

# views.py

from django.conf import settings
from django.shortcuts import render
import stripe

def payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        amount = 200  # Replace with the actual payment amount
        currency = 'usd'  # Replace with the actual currency
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )
        return render(request, 'payment.html', {
            'client_secret': payment_intent.client_secret,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        })
    return render(request, 'payment.html', {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY})

# views.py

from django.shortcuts import render, redirect
from django.conf import settings
import stripe

# views.py

from django.http import JsonResponse
import stripe
from django.conf import settings

def create_payment_intent(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        amount = 2000  # Replace with the actual payment amount
        currency = 'usd'  # Replace with the actual currency
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
        )
        return JsonResponse({'client_secret': payment_intent.client_secret})
    return JsonResponse({'error': 'Invalid request method'})

def payment_confirmation(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_method_id = request.POST['payment_method_id']
        amount = 2000  # Replace with the actual payment amount
        currency = 'usd'  # Replace with the actual currency
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method=payment_method_id,
            confirm=True,
        )
        # Save the payment details in the database
        payment = payment.objects.create(
            amount=amount,
            currency=currency,
            payment_intent_id=payment_intent.id,
        )
        return redirect('success')  # Redirect to a success page
    return redirect('cancel')  # Redirect to a cancel page
# views.py

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Initialize Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_view(request):
    if request.method == 'POST':
        try:
            # Create a payment intent with Stripe
            intent = stripe.PaymentIntent.create(
                amount=1000,  # Replace with the actual amount in cents (e.g., 1000 for $10)
                currency='usd',  # Replace with your preferred currency
            )
            client_secret = intent.client_secret
            return JsonResponse({'clientSecret': client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return render(request, 'payments/payment.html')
