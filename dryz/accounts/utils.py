import pyotp
from datetime import datetime, timedelta
from django.db.models.signals import Signal
from django.dispatch import receiver
from django.core.mail import send_mail
import threading
from threading import local
from accounts.middleware import request_local

otp_generated = Signal()

@receiver(otp_generated)
def send_otp(sender, **kwargs):
    request = request_local.request
    email = kwargs.get('email')
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_date)

    subject = f"Hello, {email}!"
    message = "OTP verification"
    from_email = "dryzz.official@gmail.com"
    htmlgen = f"""
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
  <div style="margin:50px auto;width:70%;padding:20px 0">
    <div style="border-bottom:1px solid #eee">
      <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Dryz</a>
    </div>
    <p style="font-size:1.1em">Hi,</p>
    <p>Thank you for choosing Dryz. Use the following OTP to complete your Sign In procedures. OTP is valid for 1 minutes</p>
    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
    <p style="font-size:0.9em;">Regards,<br />Dryz</p>
    <hr style="border:none;border-top:1px solid #eee" />
    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
      <p>Dryz</p>
      <p>contact : 0000000000</p>
      <p>Email : Dryzz.official@gamil.com</p>
    </div>
  </div>
</div>
    """
    send_mail(subject, message, from_email, [email], fail_silently=False, html_message=htmlgen)
    print(f"your OTP is{otp}")
