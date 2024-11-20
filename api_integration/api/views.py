from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils.sms import send_sms

class SendSMSView(APIView):
    def post(self, request, *args, **kwargs):
        # Get message and recipient(s) from the request data
        message = request.data.get("message")
        recipients = request.data.get("recipients")  # Expecting a list of phone numbers

        if not message or not recipients:
            return Response({"error": "Message and recipients are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # If recipients is a single phone number, convert it to a list
        if isinstance(recipients, str):
            recipients = [recipients]

        # Send the SMS
        response = send_sms(message, recipients)
        
        # Handle the API response
        if "error" in response:
            return Response({"error": response["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"success": {"message": "Message sent successfully", "recipients": recipients}}, status=status.HTTP_200_OK)
    
def home(request):
    return render(request, 'home.html')