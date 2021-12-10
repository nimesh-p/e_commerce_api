from django.contrib.sites.models import Site

current_site = Site.objects.get_current()

SITE_URL = current_site.domain


EMAIL_VERIFY_MESSAGE = {
    "subject": "Please confirm your email",
    "title": "Hello, FirstName,",
    "body": f"\nWe need to confirm that it's you,\n{SITE_URL}/activate/UID/TOKEN/ \nIf you did not register an account with us, please ignore or delete this email",
    "footer": "\nThank you",
}

SUCCESS_REGISTRATION_MESSAGE = {
    "subject": "Welcome to E-commerce",
    "title": "Hello, FirstName,",
    "body": f"\nWelcome to E-commerce Website,\n{SITE_URL}/login/ \nThank you",
}
CLASS_RESPONSE = {"success": True, "message": ""}
ORGANIZATION_RESPONCE = "Get all cart data successfully"

PASSWORD_RESET_EMAIL_MESSAGE = {
    "header": "Hello, ",
    "body": "We need to confirm that it's you,",
    "footer1": "If you did not request to reset your password, please ignore or delete this email",
    "footer": "Thank you",
}
