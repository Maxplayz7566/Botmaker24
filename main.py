import json
import os.path
import time

import webview
import ctypes
import logging
import threading

from flask import Flask
from webview import Window

import flaskapi
import bot

window: Window = None
app = Flask(__name__, template_folder='ui/templates')
DEBUG = True

WM_SETICON = 0x0080
ICON_SMALL = 0
ICON_BIG = 1

appInfo = {
    "version": "0.1",
    "company": "tir5d.turtle",
    "product": "Botmaker24",
    "subproduct": "maker"
}

defaultData = {
    "completedSetup": False,
    "prefix": "!",
    "botInfo": {
        "token": ""
    }
}

def loadData():
    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:
            json.dump(defaultData, f, indent=4)

def getLogger():
    logger = logging.getLogger(str(__name__).replace("__", ""))
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def getRandomPort():
    logger.info("Grabbing random free port to bind to")
    import socket
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def codeOnRun():
    logger.info("Started Webview")
    loadData()
    botThread.start()
    flaskThread.start()

def run_flask():
    time.sleep(2)
    flaskapi.createRoutes(app, window, bot, logger)
    app.run('127.0.0.1', serverPort)

def run_bot():
    bot.bot.run(json.load(open('data.json', 'r'))['botInfo']['token'])

if __name__ == '__main__':
    logger = getLogger()
    if not DEBUG:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
    serverPort = 59267 if DEBUG else getRandomPort()

    flaskThread = threading.Thread(name='Flask', daemon=True, target=run_flask)
    botThread = threading.Thread(name='Flask', daemon=True, target=run_bot)

    logger.info("Creating window")
    window = webview.create_window(f'',
                                   url=f"http://localhost:{serverPort}/setup.html",
                                   resizable=False,
                                   width=320,
                                   height=600
                                   )

    logger.info("Creating app user model id")
    myappid = f'{appInfo["company"]}.{appInfo["product"]}.{appInfo["subproduct"]}.{appInfo["version"]}'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    webview.start(icon='res/icon.ico', func=codeOnRun, debug=DEBUG, http_server=False)
