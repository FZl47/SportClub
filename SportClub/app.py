import tools
import sys
import config
import models
from flask import (
    Flask,
    jsonify,
    request,
    render_template
)


app = Flask(__name__)



@app.route('/')
def index():
    context = {
        'static_url':config.STATIC_URL,
        'days':models.Day.all()
    }
    return render_template('index.html',**context)


@app.post('/reserve-time')
def reserve_time():
    """
        Method allow : POST
    """
    status_code = 0
    data = request.form
    time_id = data.get('time_id') or None
    day_id = data.get('day_id') or None
    name = data.get('name')
    phone = data.get('phone')
    if time_id and day_id and time_id.isdigit() and day_id.isdigit() and name and phone:
        time_object = models.Time.get(time_id,day_id)
        if time_object:
            if time_object.available:
                # Payment ...
                time_object.reserve_time(name,phone,day_id)
                # Show Message Successfully Reserved
                return tools.Set_Cookie_Functionality('وقت شما با موفقیت رزرو شد','Success')
            else:
                # Show Message Time is Not Available
                return tools.Set_Cookie_Functionality('وقت مورد نظر شما موجود نمیباشد', 'Error')
        else:
            # Show Message Time Not Found
            return tools.Set_Cookie_Functionality('وقت مورد نظر شما یافت نشد', 'Error')
    else:
        # Show Message Please Enter fields correctly
        return tools.Set_Cookie_Functionality('لطفا فیلد هارا به درستی وارد نمایید', 'Error')


@app.post('/submit-message')
def submit_message():
    """
        Method allow : POST
    """
    data = request.form
    name = data.get('name')
    phone = data.get('phone')
    message = data.get('message')
    if name and phone and message:
        models.ContactUs.add(name,phone,message)
        return tools.Set_Cookie_Functionality('نظر شما با موفقیت ثبت شد','Success')
    return tools.Set_Cookie_Functionality('لطفا فیلد هارا به درستی پر نمایید','Error')

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




