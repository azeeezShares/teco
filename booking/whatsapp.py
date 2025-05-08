import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


ACCESS_TOKEN ="EAATOF1eYUM8BO9EQGpJVKt00c6MMmFZBPN7puy3fD0DKLZAeAzvOnEPBcksGF6fwmvgEPgH5NdGw7Tahhp6zE1Lr3ZBo9PK9Rtdvo9NTXUjwoFnbbu80YRO8c14YBmCS4hAka0O9emI5USrwfx6jzO7lHNWqbrvfZC1O1QS710iqepOnliNoPHWG"
VERSION = "v22.0"
PHONE_NUMBER_ID = "682771568245963"
VERIFY_TOKEN = "dsalfjdfjoieoijfdlskjdjfdslkfjdkjfd"  # Replace with your actual token
WEBHOOK_URL = "https://tecoshop.es/webhook/"  # Replace with your actual webhook URL

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        with open("whatsapp_response.txt", "a") as file:
            file.write(response.text)
        print("Response saved to whatsapp_response.txt")
        return response
    else:
        with open("whatsapp_error.txt", "a") as file:
            file.write(response.text)
        print(response.status_code)
        print(response.text)
        return response
    


@csrf_exempt  # Disable CSRF for this view as the requests are coming from an external source
def webhook(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)

            # # Check if the 'statuses' key exists in the payload
            # if 'statuses' in data:
            #     for status in data['statuses']:
            #         # Extract information about the message status
            #         message_id = status['id']
            #         recipient_id = status['recipient_id']
            #         status_type = status['status']

            #         # Log or process the message status
            #         # You could save it to the database, send an email, etc.
            #         print(f"Message {message_id} to {recipient_id} is {status_type}")
            #         with open("whatsapp_status_updates.txt", "a") as file:
            #             file.write(f"Message {message_id} to {recipient_id} is {status_type}\n")

            with open("whatsapp_status_updates.txt", "a") as file:
                file.write(request.body.decode('utf-8') + "\n")

            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    elif request.method == 'GET':
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        mode = request.GET.get('hub.mode')

        if mode and verify_token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse("Invalid verification token", status=403)