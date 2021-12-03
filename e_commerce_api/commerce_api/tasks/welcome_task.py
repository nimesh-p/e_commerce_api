from celery import Task
from commerce_api.services.success_welcome_service import SuccessEMail
from e_commerce.celery_config import celery_app


class SendWelcomeEmail(Task):
    """task for successfully registration welcome email send with celery"""

    name = "send_welcome_email"

    def run(self, user_first_name, to_email):

        try:
            return SuccessEMail.send_success_registration_email(
                user_first_name, to_email
            )

        except Exception as e:
            print(e)
            # logging.error(
            #     f"Error while calling executing SendWelcomeEmail. error message: {str(e)}"
            # )
            # return "Failed"


send_welcome_email = celery_app.register_task(SendWelcomeEmail())
