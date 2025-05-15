from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Use the user's primary key, timestamp, and email verification status
        # to create a unique token
        return (
            str(user.pk) + str(timestamp) + str(user.profile.email_verified)
        )

email_verification_token = EmailVerificationTokenGenerator()

def send_verification_email(user, request):
    """
    Send an email verification link to the user
    """
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Save the token to the user's profile
    user.profile.email_token = token
    user.profile.save()

    # Build the verification URL with HTTPS
    verification_path = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    # Force HTTPS for verification URL
    verification_url = request.build_absolute_uri(verification_path)
    # Ensure the URL uses HTTPS
    if verification_url.startswith('http://'):
        verification_url = verification_url.replace('http://', 'https://', 1)

    # Email content
    subject = 'Verify your email address'

    # Prepare context for the email template
    context = {
        'user': user,
        'verification_url': verification_url,
    }

    # Render HTML email
    html_message = render_to_string('registration/emails/email_verification.html', context)
    # Create plain text version of the email
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=html_message,
    )
