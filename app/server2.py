#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import static_file, route, run, get
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

import os
import json
from bot import Bot
import re

clients = set()
my_bot = Bot()

@route('/')
def index():
    return static_file('index.html', root='./app')


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./app')


@get('/websocket', apply=[websocket])
def chat(ws):
    clients.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in clients:
                u.send(json.dumps({'data': msg}))
            bot_res = my_bot.recv_message(msg)
            if bot_res != None:
                for u in clients:
                    u.send(json.dumps({'data': bot_res}))
        else: break
    clients.remove(ws)

run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), server=GeventWebSocketServer)
