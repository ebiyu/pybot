import mylogger
from logging import getLogger
logger=getLogger('slackLib')

import requests ,json
import key
WEB_HOOK_URL=key.WEB_HOOK_URL()
API_TOKEN=key.API_TOKEN()
BOT_TOKEN=key.BOT_TOKEN()

import datetime

def send(text,to,name='',icon=''):
    requests.post(WEB_HOOK_URL, data = json.dumps({
        'text': text,
        'username': name,
        'icon_emoji': icon,
        'channel' : to,
    }))

bot_headers={
        'Authorization': 'Bearer ' + BOT_TOKEN,
        'Content-Type': 'application/json; charset=utf-8'
}
def addReactionByBot(channel,ts,emoji):
    url='https://slack.com/api/reactions.add'
    resp=requests.post(url, data = json.dumps({
        'name': emoji,
        'channel': getChannelId(channel),
        'timestamp': ts,
    }),headers = bot_headers)
    if resp.json()['ok']==False:
        logger.error(resp.json()['error'])
    else:
        logger.info('add :'+emoji+': to #'+channel)

api_headers={
        'Authorization': 'Bearer ' + API_TOKEN,
        'Content-Type': 'application/json; charset=utf-8'
}

def sendWithAPI(text,to,name='',icon=''):
    url='https://slack.com/api/chat.postMessage'
    resp=requests.post(url, data = json.dumps({
        'text': text,
        'username': name,
        'icon_emoji': icon,
        'channel' : to,
    }),headers = api_headers)
    if resp.json()['ok']==False:
        logger.error(resp.json()['error'])
    else:
        logger.info('sent "'+text+'" to '+to)
        return resp.json()['ts']

def getChannelId(name):
    url='https://slack.com/api/channels.list'
    resp=requests.post(url,headers = api_headers)
    if resp.json()['ok']:
        logger.debug('successfully got id for #'+name)
        channellist=(resp.json())['channels']
        for i in range(len(channellist)):
            if channellist[i]['name']==name:
                return channellist[i]['id']
        logger.error('channel not found')
    else:
        logger.error(resp.json()['error'])

def getChannelList():
    url='https://slack.com/api/channels.list'
    resp=requests.post(url,headers = api_headers)
    if resp.json()['ok']:
        logger.debug('successfully got channel list')
        channellist=(resp.json())['channels']
        for i in range(len(channellist)):
            channellist[i]=channellist[i]['name']
        return channellist
    else:
        logger.error(resp.json()['error'])

def getUserList(channel):
    url='https://slack.com/api/channels.info'
    resp=requests.get(url,params={
        'token': API_TOKEN,
        'channel': getChannelId(channel)
    })
    if resp.json()['ok']:
        logger.debug('successfully got user list in #'+channel)
        return resp.json()['channel']['members']
    else:
        logger.error(resp.json()['error'])

def getUserRealName(userid):
    url='https://slack.com/api/users.info'
    resp=requests.get(url,params={
        'token': API_TOKEN,
        'user': userid
    })
    if resp.json()['ok']:
        logger.debug('successfully got user name of '+userid)
        return (resp.json())['user']['profile']['real_name']
    else:
        logger.error(resp.json()['error'])

def cleanChannel(channel,beforeHour):
    ts=(datetime.datetime.now()-datetime.timedelta(hours=beforeHour)).timestamp()
    chid=getChannelId(channel)
    geturl='https://slack.com/api/channels.history'
    resp=requests.get(geturl,params={
        'token': API_TOKEN,
        'channel': chid,
        'latest': ts
    })
    if resp.json()['ok']:
        l=resp.json()['messages']
        tslist=[]
        delurl='https://slack.com/api/chat.delete'
        for i in l:
            tslist.append(i['ts'])
            resp2=requests.post(delurl, data = json.dumps({
                'channel' : chid,
                'ts': i['ts']
            }),headers = api_headers)
            if resp.json()['ok']==False:
                logger.error(resp.json()['error'])
                break
        else:
            if len(l)!=0:
                logger.info('successfully cleared '+str(len(l))+' message(s) in #'+channel)
            else:
                logger.debug('no message to delete in #'+channel)
    else:
        logger.error(resp.json()['error'])
