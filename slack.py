import requests ,json
import key
WEB_HOOK_URL=key.WEB_HOOK_URL()
API_TOKEN=key.API_TOKEN()

def send(text,to,name='',icon=''):
    requests.post(WEB_HOOK_URL, data = json.dumps({
        'text': text,
        'username': name,
        'icon_emoji': icon,
        'channel' : to,
    }))

def sendWithAPI(text,to,name='',icon=''):
    url='https://slack.com/api/chat.postMessage'
    requests.post(url, data = json.dumps({
        'text': text,
        'username': name,
        'icon_emoji': icon,
        'channel' : to,
    }),headers = {
        'Authorization': 'Bearer ' + API_TOKEN,
        'Content-Type': 'application/json; charset=utf-8'
    })
