# page navigation purpose
import re

from django.shortcuts import render, redirect


# authentication purpose
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib import messages


# otp generation  purpose
from .models import CustomUser
from .utils import send_otp, otp_generated
from datetime import datetime
import pyotp

# validation purpose
from django.core.exceptions import ValidationError


# <------------------------------------Start Login------------------------------------------------------>

@never_cache
# User sign-in view
def UserSignin(request):
    # Check if the user is already authenticated
    if 'user-email' in request.session:
        # If authenticated, redirect to the home page
        return redirect('home')

    # Handle POST request (user submission of login form)
    if request.method == 'POST':
        # Get email and password from the form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email and password are provided and not empty
        if email is not None and password is not None and email.strip() == '' and password.strip() == '':
            # Display an error message and redirect back to the sign-in page if fields are blank
            messages.error(request, "Fields can't be blank")
            return redirect('user_signin')
        # Authenticate the user with provided email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active is True and user.is_superuser is False:
                try:
                    pass
                except:
                    pass
                login(request, user)
                request.session['user-email'] = email
                return redirect('home')
            else:
                return redirect('user_signin')
        else:
            try:
                user = CustomUser.objects.get(email=email)
                if user.is_active is False:
                    messages.error(request, 'User is Blocked..!')
                else:
                    messages.error(request, 'Email or password is incorrect')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Email or password is incorrect')
            return redirect('user_signin')

    # Render the user login page for GET requests
    return render(request, 'user/user_login.html')


# <------------------------------------End Login------------------------------------------------------>


def signin_email_otp(request):
    if 'user-email' in request.session:
        # If authenticated, redirect to the home page
        return redirect('home')

    # Handle POST request (user submission of login form)
    if request.method == 'POST':
        # Get email and password from the form data
        email = request.POST.get('email')
        # Check if email and password are provided and not empty
        if email is not None and email.strip() == '':
            # Display an error message and redirect back to the sign-in page if fields are blank
            messages.error(request, "Fields can't be blank")
            return redirect('user_signin')
        try:
            user = CustomUser.objects.get(email=email)

            if user is not None:
                if user.is_active is True and user.is_superuser is False:
                    # If authentication succeeds, send an OTP for further verification
                    # sent email otp using signal
                    otp_generated.send(sender=None, email=email)
                    # Store email and password in the session for later use
                    request.session['user_email'] = email
                    return redirect('signin_otp')
                else:
                    messages.error(request, 'you are blocked')
                # Redirect to the OTP verification page
                return redirect('signin_otp')
            else:
                # If authentication fails, display an error message and redirect back to the sign-in page
                messages.error(request, 'Email is incorrect')
                return redirect('user_signin')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email is incorrect')
    # Render the user login page for GET requests
    return render(request, 'user/user_login.html')


# <---------------------------------------OTP validation ---------------------------------------------->
def otp_signin(request):
    if 'user-email' in request.session:
        return redirect('home')
    if request.method == 'POST':
        otp = ''
        otp += request.POST.get('otp1')
        otp += request.POST.get('otp2')
        otp += request.POST.get('otp3')
        otp += request.POST.get('otp4')
        otp += request.POST.get('otp5')
        otp += request.POST.get('otp6')
        user_email = request.session['user_email']
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            validate_until = datetime.fromisoformat(otp_valid_date)
            if validate_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=120)
                if totp.verify(otp):
                    user = CustomUser.objects.get(email=user_email)
                    login(request, user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['user_email']
                    request.session['user-email'] = user_email
                    return redirect('home')
                else:
                    messages.error(request, 'Please enter proper OTP .')
            else:
                messages.error(request, 'OTP expired.')
        else:
            del request.session['otp_secret_key']
            del request.session['otp_valid_date']
            del request.session['email']
            return redirect('user_signin')

    return render(request, 'user/otp_signin.html')


# <--------------------------------------End -OTP validation ---------------------------------------------->


# <---------------------------------------Start Register form validation---------------------------------------->

# <-------------Email validation---------------->
def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


# <------------password validation-------------->
def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False


# <-----------------username validation----------->
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'

    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces'
    elif CustomUser.objects.filter(username=value).exists():
        return 'Username already exist'
    else:
        return False


# <---------------------------------------End register form validation---------------------------------------->


# <---------------------------------------Start Signup-------------------------------------------------------->
def UserSignup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Null values checking
        check = [username, email, password, cpassword, phone]
        for value in check:
            if not value:
                context = {
                    'pre_username': username,
                    'pre_phone': phone,
                    'pre_email': email,
                }
                messages.info(request, 'Some fields are empty')
                return render(request, 'user/user_register.html', context)

        # Validate name
        result = validate_name(username)
        if result is not False:
            context = {
                'pre_username': username,
                'pre_phone': phone,
                'pre_email': email,
            }
            messages.info(request, result)
            return render(request, 'user/user_register.html', context)

        # Validate email
        if not validateEmail(email):
            context = {
                'pre_username': username,
                'pre_phone': phone,
                'pre_email': email,
            }
            messages.info(request, 'Enter a valid email')
            return render(request, 'user/user_register.html', context)

        # Validate password
        if not ValidatePassword(cpassword):
            context = {
                'pre_username': username,
                'pre_phone': phone,
                'pre_email': email,
            }
            messages.warning(request, 'Enter a strong password')
            return render(request, 'user/user_register.html', context)

        # Check if the email already exists in the User model
        if CustomUser.objects.filter(email=email).exists():
            context = {
                'pre_username': username,
                'pre_phone': phone,
                'pre_email': email,
            }
            messages.error(request, 'Email already exists')
            return render(request, 'user/user_register.html', context)

        if CustomUser.objects.filter(phone=phone).exists():
            context = {
                'pre_username': username,
                'pre_phone': phone,
                'pre_email': email,
            }
            messages.error(request, 'Phone Number is already exists')
            return render(request, 'user/user_register.html', context)

        if password != cpassword:
            context = {
                'pre_username': username,
                'pre_phone': phone,
                'pre_email': email,
            }
            messages.error(request, 'Passwords do not match')
            return render(request, 'user/user_register.html', context)

        # sent email otp using signal

        otp_generated.send(sender=None, email=email)
        request.session['username'] = username
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['password'] = password

        return redirect('signup_otp')

    return render(request, 'user/user_register.html')


# <---------------------------------------End Signup-------------------------------------------------------->

def otp_signup(request):
    email = request.session['email']
    username = request.session['username']
    phone = request.session['phone']
    password = request.session['password']

    if request.method == 'POST':
        otp = ''
        otp += request.POST.get('otp1')
        otp += request.POST.get('otp2')
        otp += request.POST.get('otp3')
        otp += request.POST.get('otp4')
        otp += request.POST.get('otp5')
        otp += request.POST.get('otp6')

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']
        if otp_secret_key and otp_valid_date is not None:
            validate_until = datetime.fromisoformat(otp_valid_date)
            if validate_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=120)
                if totp.verify(otp):
                    # User Registration
                    my_user = CustomUser.objects.create_user(email, password=password, username=username, phone=phone)
                    my_user.save()
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['email']
                    del request.session['username']
                    del request.session['phone']
                    del request.session['password']
                    request.session['user-email'] = email
                    return redirect('home')
                else:
                    messages.error(request, 'Please enter proper OTP .')
            else:
                messages.error(request, 'OTP expired.')
        else:
            del request.session['otp_secret_key']
            del request.session['otp_valid_date']
            del request.session['email']
            return redirect('user_signin')

    return render(request, 'user/otp_signup.html')


# <---------------------------------------Start Logout-------------------------------------------------------->

@never_cache
def UserLogout(request):
    # session_key = request.session.session_key
    if 'user-email' in request.session:
        # if session_key:
        #     Session.objects.filter(session_key=session_key).delete()
        logout(request)

    return redirect('user_signin')


# <---------------------------------------End Signup-------------------------------------------------------->


def ForgotPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            try:
                is_valid_email = CustomUser.objects.get(email=email)
                if is_valid_email is not None:
                    request.session['email'] = email
                    send_otp(request, email)
                    return redirect('otp_forgot_password')
            except CustomUser.DoesNotExist:
                messages.error(request, 'No user is found')
                return redirect('forgot_password')
    except Exception as e:
        print(e)
    return render(request, "user/forgot_password.html")


# conform_password.html

def ConfirmPassword(request):
    try:
        if request.method == 'POST':
            password = request.POST.get('password')
            c_password = request.POST.get('c_password')
            if not ValidatePassword(c_password):
                messages.warning(request, 'Enter a strong password')
                return render(request, 'user/confirm_password.html')
            if password != c_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'user/user_register.html')
            email = request.session['email']
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(password)
                user.save()
                return redirect('user_signin')
            except CustomUser.DoesNotExist:
                return redirect('forgot_password')

    except Exception as e:
        print(e)

    return render(request, 'user/confirm_password.html')


def ForgotPasswordOtp(request):
    if request.method == 'POST':
        otp = ''
        otp += request.POST.get('otp1')
        otp += request.POST.get('otp2')
        otp += request.POST.get('otp3')
        otp += request.POST.get('otp4')
        otp += request.POST.get('otp5')
        otp += request.POST.get('otp6')

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']
        if otp_secret_key and otp_valid_date is not None:
            validate_until = datetime.fromisoformat(otp_valid_date)
            if validate_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=120)
                if totp.verify(otp):
                    return redirect('confirm_password')
                else:
                    messages.error(request, 'Please enter proper OTP .')
            else:
                messages.error(request, 'OTP expired.')
        else:
            del request.session['otp_secret_key']
            del request.session['otp_valid_date']
            del request.session['email']
            return redirect('user_signin')

    return render(request, 'user/otp_forgot_password.html')


def ResentOtp(request):
    try:
        if 'otp_secret_key' in request.session:
            del request.session['otp_secret_key']
        if 'otp_valid_date' in request.session:
            del request.session['otp_valid_date']

            email= request.session['user_email']
            send_otp(request,email)
        return redirect('signin_otp')
    except Exception as e:
        print(e)


def wallet(request):
    return render(request, 'user/user-profile/wallet.html')