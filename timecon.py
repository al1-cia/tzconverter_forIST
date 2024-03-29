from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__,static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    timezones = {
        "AEST": [4,30],
        "BST": [-4, -30],
        "CST": [-10, -30],
        "PT": [-12, -30],
        "EST": [-9, -30],
        "GMT": [-5, -30],
        "UTC": [-5, -30],
        "CET": [-4, -30],
        "JST":[3,30],
        "IST": [0,0]
    }

    tz = request.form['timezone']
    h = int(request.form['hours'])
    m = int(request.form['minutes'])
    ap = request.form['am_pm']

    if tz == "IST":
        tzn = request.form['convert_from']
        hrs = -timezones[tzn][0]
        mns = -timezones[tzn][1]
        if(hrs<0):
            day=0
        else:
            day=1
        if ap == "am":
            ap = "pm"
        else:
            ap = "am"
    else:
        tzn="IST"
        hrs = timezones[tz][0]
        mns = timezones[tz][1]
        if(hrs<0):
            day=0
        else:
            day=1

    hours = h + hrs
    if hours < 0:
        hours = 12 - np.abs(hours)
        if ap == "am":
            ap = "pm"
        else:
            ap = "am"
    elif hours > 12:
        hours = np.abs(hours) - 12

    mins = m + mns
    if mins < 0:
        hours = hours - 1
        mins = np.abs(mins)
    elif mins == 60:
        hours=hours+1
        mins=0
    if mins / 10 < 1:
        mins = str(mins)
        mins = "0" + mins

    result_time = f"{hours}:{mins} {ap}"
    if(day==0):diff="Behind"
    else:diff="Ahead of"
    return render_template('results.html', result_time=result_time,diff=diff,tzn=tzn, tz=tz)
if __name__ == '__main__':
    app.run(debug=True)
