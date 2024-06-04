import requests


def send_sms(mobile:str, text:str):
    sender = "50004001896361"
    data = {'from': sender, 'to': mobile, 'text': text}
    response = requests.post('https://console.melipayamak.com/api/send/simple/8265f04cef6145c3be077c6f34e656c1', json=data)
    return response.json()

def send_token(mobile:str):
    data = {'to': mobile}
    response = requests.post('https://console.melipayamak.com/api/send/otp/8265f04cef6145c3be077c6f34e656c1', json=data)
    return response.json()