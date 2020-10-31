import time
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
number_to = os.getenv('NUMBER_TO')
number_from = os.getenv('NUMBER_FROM')
access_token = os.getenv('ACCESS_TOKEN')
client = Client(account_sid, auth_token)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'access_token': access_token,
        'fields': 'online',
        'v': 5.92
    }
    status = requests.post("https://api.vk.com/method/users.get", params=params)
    user_info = status.json()['response']
    return (user_info[0]['online'])


def sms_sender(sms_text):
    message = client.messages.create(
        to=number_to, 
        from_=number_from,
        body=sms_text)
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)