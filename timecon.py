from flask import Flask, render_template, request
import numpy as np
from datetime import datetime, timedelta
import calendar

app = Flask(__name__,static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

def is_last_sunday(date):
    last_day_of_month = calendar.monthrange(date.year, date.month)[1]
    for day in range(last_day_of_month, 0, -1):
        if calendar.weekday(date.year, date.month, day) == 6:  #is the day sunday
            return day
    return None 

@app.route('/convert', methods=['POST'])
def convert():
    timezones = {
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
    cur_date = request.form.get('cur_date')
    cur_datetimeobj = datetime.strptime(cur_date, '%Y-%m-%d')
    last_sunday_of_month = is_last_sunday(cur_datetimeobj)

    #DST Logic
    if 3<=cur_datetimeobj.month<=10: #within dst months
        DST=True
        if cur_datetimeobj.month==3 and cur_datetimeobj.day < last_sunday_of_month:
            DST=False
        elif cur_datetimeobj.month==10 and cur_datetimeobj.day > last_sunday_of_month:
            DST=False
        else:
            DST=True

    dec_date = cur_datetimeobj - timedelta(days=1)

    tz = request.form['timezone'] #converting to
    h = int(request.form['hours'])
    m = int(request.form['minutes'])
    ap = request.form['am_pm']
    dst_ap=request.form['am_pm']

    if tz == "IST": #converting to ist
        tzn = request.form['convert_from']
        hrs = -timezones[tzn][0]
        dst_hrs=-(timezones[tzn][0]+1)
        mns = -timezones[tzn][1]
        dst_mns=-timezones[tzn][1]
        if(hrs<0):
            day=0
        else:
            day=1
      
        if(dst_hrs<0):
            dst_day=0
        else:
            dst_day=1

    else:
        tzn="IST"
        hrs = timezones[tz][0]
        dst_hrs=timezones[tz][0]+1
        mns = timezones[tz][1]
        dst_mns=timezones[tz][1]
        if(hrs<0):
            day=0
        else:
            day=1
        if(dst_hrs<0):
            dst_day=0
        else:
            dst_day=1

    hours = h + hrs
    if hours < 0:
        hours = 12 - np.abs(hours)
        if ap == "am":
            ap = "pm"
        else:
            ap = "am"
    elif hours > 12:
        hours = np.abs(hours) - 12
        if ap == "am":
            ap = "pm"
        else:
            ap = "am"

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
    
    dst_hours = h + dst_hrs
    if dst_hours < 0:
        dst_hours = 12 - np.abs(dst_hours)
        if dst_ap == "am":
            dst_ap = "pm"
        else:
            dst_ap = "am"
    elif dst_hours > 12:
        dst_hours = np.abs(dst_hours) - 12
        if dst_ap == "am":
            dst_ap = "pm"
        else:
            dst_ap = "am"

    dst_mins = m + dst_mns
    if dst_mins < 0:
        dst_hours = dst_hours - 1
        dst_mins = np.abs(dst_mins)
    elif dst_mins == 60:
        dst_hours=dst_hours+1
        dst_mins=0
    if dst_mins / 10 < 1:
        dst_mins = str(dst_mins)
        dst_mins = "0" + dst_mins

    result_time = f"{hours}:{mins} {ap}"
    dst_time = f"{dst_hours}:{dst_mins} {dst_ap}"

    if(day==0):diff=dec_date.date()
    else:diff=cur_datetimeobj.date()

    if(dst_day==0):dst_diff=dec_date.date()
    else:dst_diff=cur_datetimeobj.date()
    
    if(DST==True):dst="may apply"
    else:dst="does not apply" 

    return render_template('results.html', result_time=result_time,diff=diff,dst_diff=dst_diff, tz=tz,dst=dst,dst_time=dst_time)
if __name__ == '__main__':
    app.run(debug=True)
