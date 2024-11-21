from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from .utils.sms import send_sms
import os
from django.conf import settings

# Used BASE_DIR to get the correct path to token.json
TOKEN_PATH = os.path.join(settings.BASE_DIR, 'api', 'token.json')

class SendNotificationsView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        message = request.data.get("message")
        recipients_sms = request.data.get("recipients_sms", [])  # List of phone numbers
        recipients_email = request.data.get("recipients_email", [])  # List of email addresses
        
        if not message:
            return Response({"error": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # SMS Sending
        sms_response = {"status": "No recipients for SMS"}
        if recipients_sms:
            sms_response = send_sms(message, recipients_sms)

        # Email Sending
        email_response = {"status": "No recipients for email"}
        if recipients_email:
            try:
                # Load the token.json file for Gmail API credentials
                creds = Credentials.from_authorized_user_file(TOKEN_PATH)
                
                # Refresh the token if it has expired
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                
                # Build the Gmail API service
                service = build('gmail', 'v1', credentials=creds)
                
                # Send emails to all recipients
                for email in recipients_email:
                    send_email(service, email, "Notification", message)
                
                email_response = {"status": "Emails sent successfully"}
            except Exception as e:
                email_response = {"error": str(e)}

        return Response({
            "success": {
                "sms_recipients": recipients_sms,
                "email_recipients": recipients_email,
            },
            "sms_response": sms_response,
            "email_response": email_response,
        }, status=status.HTTP_200_OK)

def send_email(service, to_email, subject, message_text):
    from email.mime.text import MIMEText
    import base64

    # Create an email message
    message = MIMEText(message_text)
    message['to'] = to_email
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email
    service.users().messages().send(userId="me", body={"raw": raw}).execute()

def home(request):
    return render(request, 'home.html')