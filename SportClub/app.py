from flask import (
    Flask,
    jsonify,
    request,
    render_template
)
import sys
import config
import models

app = Flask(__name__)



@app.route('/')
def index():
    context = {
        'static_url':config.STATIC_URL,
        "name":"Fazel",
        'days':models.Day.all()
    }
    return render_template('index.html',**context)


if __name__ == '__main__':
    commands = {}
    _args_command = sys.argv
    _args_command = _args_command[1:]
    for cmnd in _args_command:
        cmnd = cmnd.split('=')
        key , val = cmnd[0],cmnd[1]
        commands[key] = val
    signal = commands.get('-s','run')
    if signal == 'run':
        app.run(debug=config.DEBUG)
    elif signal == 'migrate':
        models._migrate()




