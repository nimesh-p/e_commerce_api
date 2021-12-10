from celery import Task
from django.contrib.auth.forms import PasswordResetForm
from e_commerce.celery_config import celery_app
from commerce_api.models import User


class PasswordResetEmail(Task):
    """task for password rest email send with celery"""

    name = "send_password_reset_email"

    def run(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name,
    ):
        print(subject_template_name)
        print(email_template_name)
        print(context)
        print(from_email)
        print(to_email)
        print(html_email_template_name)

        try:
            context["user"] = User.objects.get(pk=context["user"])

            return PasswordResetForm.send_mail(
                None,
                subject_template_name,
                email_template_name,
                context,
                from_email,
                to_email,
                html_email_template_name,
            )

        except Exception as e:
            print(e)
            # logging.error(
            #     f"Error while calling executing PasswordResetEmail. error message: {str(e)}"
            # )
            # return "Failed"


send_password_reset_email = celery_app.register_task(PasswordResetEmail())
