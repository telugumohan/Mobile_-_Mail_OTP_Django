from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import RegistrationForm, OTPForm, LoginForm
from .models import TempUser, User
import random
import requests
import smtplib
from .utils import send_otp_via_sms

def generate_otp():
    return str(random.randint(100000, 999999))  # Generate a 6-digit OTP as a string


def send_otp_to_email(email, otp):
    try:
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'your-email@gmail.com',  # Sender email
            [email],  # Recipient email
            fail_silently=False,
        )
    except smtplib.SMTPException as e:
        print(f'SMTP error occurred: {e}')
    except Exception as e:
        print(f'Error sending email: {e}')
        return False
    return True



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            otp = generate_otp()
            email_otp = otp[:3].zfill(3)  # Ensures it's always 3 digits
            phone_otp = otp[3:].zfill(3)  # Ensures it's always 3 digits

            # Check if the email or phone already exists
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'form': form, 'error': 'Email is already taken'})

            success = True
            if phone:
                try:
                    send_otp_via_sms(phone, phone_otp)  # Send the last 3 digits to mobile
                except Exception as e:
                    print(f'Error sending SMS: {e}')
                    success = False

            if email:
                success &= send_otp_to_email(email, email_otp)  # Send the first 3 digits to email

            if success:
                # Store the complete OTP in session
                TempUser.objects.create(email=email, phone=phone, password=password, email_otp=email_otp,
                                        phone_otp=phone_otp)
                return redirect('validate_otp')  # Redirect to the OTP verification page
            else:
                return JsonResponse({"status": "error", "message": "Failed to send OTP"})

    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def validate_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            combined_otp = form.cleaned_data['combined_otp']
            temp_user = TempUser.objects.latest('created_at')
            expected_otp = str(temp_user.email_otp) + str(temp_user.phone_otp)
            if combined_otp == expected_otp:
                User.objects.create(email=temp_user.email, phone=temp_user.phone, password=temp_user.password)
                # Send success message to email and phone
                send_mail('Registration Successful', 'You have successfully registered!', 'from@example.com', [temp_user.email])
                print(f'Sending registration success message to {temp_user.phone}')
                return redirect('registration_success')
            else:
                return render(request, 'validate_otp.html', {'form': form, 'error': 'Invalid OTP'})
    else:
        form = OTPForm()
    return render(request, 'validate_otp.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=identifier).first() or User.objects.filter(phone=identifier).first()
            if user and user.password == password:
                return redirect('login_success')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Wrong password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')

def login_success(request):
    return render(request, 'login_success.html')
