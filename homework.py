import time
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
import logging
load_dotenv()

logging.basicConfig(level=logging.INFO)

ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
NUMBER_TO = os.getenv('NUMBER_TO')
NUMBER_FROM = os.getenv('NUMBER_FROM')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
URL_API_VK = "https://api.vk.com/method/"
TWILIO_CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'access_token': ACCESS_TOKEN,
        'fields': 'online',
        'v': 5.92
    }
    method = 'users.get'
    url = URL_API_VK + method
    try:
        status = requests.post(url, params=params)
        try:
            user_info = status.json()['response']
            return user_info[0]['online']
        except Exception as err:
            logging.error(err, exc_info=True)
    except Exception as err:
        logging.error(err, exc_info=True)


def sms_sender(sms_text):
    message = TWILIO_CLIENT.messages.create(
        to=NUMBER_TO, 
        from_=NUMBER_FROM,
        body=sms_text)
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        else:
            logging.info(f'{vk_id} сейчас оффлайн!')
        time.sleep(5)