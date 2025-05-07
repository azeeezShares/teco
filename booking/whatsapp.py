import requests
ACCESS_TOKEN ="EAATOF1eYUM8BO9EQGpJVKt00c6MMmFZBPN7puy3fD0DKLZAeAzvOnEPBcksGF6fwmvgEPgH5NdGw7Tahhp6zE1Lr3ZBo9PK9Rtdvo9NTXUjwoFnbbu80YRO8c14YBmCS4hAka0O9emI5USrwfx6jzO7lHNWqbrvfZC1O1QS710iqepOnliNoPHWG"
VERSION = "v22.0"
PHONE_NUMBER = "+998954271965"
PHONE_NUMBER_ID = "682771568245963"

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
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response