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

api_headers={
        'Authorization': 'Bearer ' + API_TOKEN,
        'Content-Type': 'application/json; charset=utf-8'
}

def sendWithAPI(text,to,name='',icon=''):
    url='https://slack.com/api/chat.postMessage'
    requests.post(url, data = json.dumps({
        'text': text,
        'username': name,
        'icon_emoji': icon,
        'channel' : to,
    }),headers = api_headers)

def getChannelId(name):
    url='https://slack.com/api/channels.list'
    resp=requests.post(url,headers = api_headers)
    channellist=(resp.json())['channels']
    for i in range(len(channellist)):
        if channellist[i]['name']==name:
            return channellist[i]['id']

def getUserList(channel):
    url='https://slack.com/api/channels.info'
    resp=requests.get(url,params={
        'token': API_TOKEN,
        'channel': getChannelId(channel)
    })
    return resp.json()['channel']['members']

def getUserRealName(userid):
    url='https://slack.com/api/users.info'
    resp=requests.get(url,params={
        'token': API_TOKEN,
        'user': userid
    })
    return (resp.json())['user']['profile']['real_name']
