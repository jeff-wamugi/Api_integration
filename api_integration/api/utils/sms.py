import africastalking
from django.conf import settings

# Initialize Africa's Talking
africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
sms = africastalking.SMS

def send_sms(message, recipients):
    """
    Sends an SMS using Africa's Talking.

    :param message: The message content
    :param recipients: A list of recipient phone numbers (e.g., ["+254745507549"])
    :return: The response from the Africa's Talking API
    """
    try:
        response = sms.send(message, recipients)
        return response
    except Exception as e:
        return {"error": str(e)}
