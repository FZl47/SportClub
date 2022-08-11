from flask import (
    Flask,
    jsonify,
    request,
    render_template
)
import config

app = Flask(__name__)


@app.route('/')
def index():
    print(request)
    context = {
        'static_url':config.STATIC_URL,
        "name":"Fazel"
    }
    return render_template('index.html',**context)



if __name__ == '__main__':
    app.run(debug=True)
