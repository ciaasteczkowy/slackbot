# coding=utf-8
import os
import json
import requests
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory, Response, jsonify
from flask_slack import Slack
import cfg


# bot.py
import bot

bot = bot.Bot(cfg)

# Flask
app = Flask(__name__)
app.config.from_pyfile('cfg.py')

# To get rid of too curious peeps
@app.route('/', methods=['GET'])
def index():
    resp = 'Go away!'
    return resp

# Flask-Slack
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)

# /translate
@slack.command('translate', token=cfg.TOKEN_TRANSLATE,
               team_id=cfg.TEAM_ID, methods=['POST'])
def translate(text=None, **kwargs):
    text = text.encode('utf-8')
    # separate languages from text to translate
    tmp = text.split()

    auto = False

    # detect it user specified source language
    if '-' in tmp[0]:
        lnfrom = tmp[0].split('-')[0]
        lnto = tmp[0].split('-')[1]
    else:
        auto = True
        lnto = tmp[0]
    # escape spaces
    text = '+'.join(tmp[1::])

    # RUSKI YANDEX OLABOGA
    if not auto:
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key={key}&lang={2}-{1}&text={0}'.format(
            text, lnto, lnfrom, key=cfg.YANDEX_KEY)
    else:
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key={key}&lang={1}&text={0}'.format(
            text, lnto, key=cfg.YANDEX_KEY)
    r = requests.get(url)
    r = json.loads(r.text)

    # if specified target language doesn't exist, then return error from server
    if 'text' in r:
        resp = r['text']
    else:
        resp = r['message']

    return slack.response(resp)


# /remindgroup
@slack.command('remindgroup', token=cfg.TOKEN_REMINDGROUP,
               team_id=cfg.TEAM_ID, methods=['POST'])
def remindgroup(**kwargs):
    text = kwargs.get('text')

    # detect if user specified channel, if not then get it from request data
    if text.startswith('#'):
        channel = text.split()[0].replace('#','')
        text = ' '.join(text.split()[1::])
    else:
        channel = kwargs.get('channel_name')

    # command is for channels only
    if channel != 'directmessage':
        # bot.post(text, channel)
        bot.post(text, channel)
        return slack.response('ok')
    else:
        return slack.response(u'Użyj komendy na kanale, dla którego chcesz ustawić przypomnienie, '
                              u'lub wpisz kanał jako pierwszy argument np:\n'
                              u'/remindgroup #random in <time> to <message>')


if __name__ == '__main__':
    app.run()
