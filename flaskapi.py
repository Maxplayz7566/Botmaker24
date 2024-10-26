import json
import os
from io import BytesIO

from flask import Flask, send_file, render_template, abort, send_from_directory, request, jsonify, redirect
from webview import Window
from webview.window import FixPoint
from discord.ext import commands
import requests

BASE_DIR = "ui"

def createRoutes(app: Flask, window: Window, bot: commands.Bot):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/<path:filename>', methods=['GET'])
    def serve_file(filename):
        if os.path.isfile(os.path.join(BASE_DIR, filename)):
            return send_from_directory(BASE_DIR, filename)
        else:
            abort(404)

    @app.route('/favicon.ico')
    def favicon(): # not that it matters
        return send_file('res/icon.ico')

    @app.route('/api/title', methods=['POST'])
    def setTitle():
        title = request.args.get('title')

        if title:
            window.set_title(title)
            return {'status': 'success!'}
        else:
            return abort(404)

    @app.route('/api/setbottoken', methods=['POST'])
    def setToken():
        token = request.form.get('token')
        guild = request.form.get('guild')

        if token and guild:
            try:
                data = json.load(open('data.json', 'r'))

                data['completedSetup'] = True
                data['botInfo']['token'] = token
                data['botInfo']['guild'] = int(guild)

                json.dump(data, open('data.json', 'w'), indent=4)
                return "<script>window.location.href = '/home.html'</script>", 200
            except Exception as e:
                return "<script>window.location.href = '/home.html'</script>", 500
        else:
            return "<script>window.location.href = '/setup.html'</script>", 400

    @app.route('/api/screenSize', methods=['POST', 'GET'])
    def setScreenSize():
        width = request.args.get('width')
        height = request.args.get('height')

        if not width and not height:
            data = {
                'width': window.width,
                'height': window.height
            }

            return data, 200
        else:
            window.resize(int(width), int(height), FixPoint.SOUTH)
            data = {
                'width': window.width,
                'height': window.height
            }
            return data, 200

    @app.route('/api/completedsetup')
    def setupsate():
        return [json.load(open('data.json', 'r'))['completedSetup']]

    @app.route('/bot/avatar')
    def avatar():
        if bot.user.avatar is not None:
            open('cache.png', 'wb').write(requests.get(bot.user.avatar).content)
        else:
            open('cache.png', 'wb').write(requests.get('https://discord.com/assets/a0180771ce23344c2a95.png').content)
        return send_file('cache.png')

    @app.route('/bot/name')
    def name():
        return bot.user.name
