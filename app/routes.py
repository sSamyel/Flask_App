from datetime import datetime
import requests
import random
from itertools import groupby
from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, SettingForm, FileForm, TranslateForm, NasaForm, NasaPlanetForm, WeatherForm
from app.models import User
from requests import post, get



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/mainPage', methods=['GET','POST'])
def index():
    a = render_template('mainPage.html', username = username, commentary = commentary, login = tname)
    return a

@app.route('/main')
def main():
    return redirect('/mainPage')

@app.route('/login', methods=['GET','POST'])
def login():
    global username,commentary, tname, tmail
    form = LoginForm()
    #users = User.query.all()
    #for u in users:
        #db.session.delete(u)
    #db.session.commit()
    if form.validate_on_submit():
        usname = form.username.data
        password = form.password.data
        users = User.query.all()
        for u in users:
            if usname == u.username and password == u.password_hash:
                login_user(u)
                username = usname
                commentary = u.commentary
                tname = u.login
                tmail = u.email
                return redirect('/main')
    logout_user()
    return render_template("login.html", form=form)

username = ""
origin = ""
tmail=""
tname = ""
commentary = "Добро пожаловать!"

@app.route('/registration', methods=['GET','POST'])
def registration():
    global NUM_USER
    global username
    global login, tname, tmail
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        login = form.login.data
        fullname = form.fullname.data
        email = form.email.data
        picture = "avatar.png"
        commentary = "Добро пожаловать!"
        user = User(username=username, password_hash=password, login=login, fullname=fullname, email=email, picture=picture, commentary=commentary)
        username = ""
        tname = ""
        tmail = ""
        db.session.add(user)
        db.session.commit()
        NUM_USER += 1
        return redirect('/mainPage')
    else:
        logout_user()
    return render_template("registration.html", form=form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    global username
    users = User.query.all()
    for u in users:
        if u.username == username:
            name = u.username
            fullname = u.fullname
            login = u.login
            email = u.email
            form = FileForm()
            fname = u.picture
            if form.validate_on_submit():
                f = form.file_object.data
                fname = f.filename
                u.picture = f.filename
                db.session.commit()
            return render_template("profile.html", name=name, fullname=fullname, login=login, email=email, fname=fname, form=form )
    return redirect('/login')


@app.route("/logout")
@login_required
def logout():
    global commentary, tname, username
    logout_user()
    username = ""
    tname = ""
    commentary = "Добро пожаловать!"
    return redirect('/login')

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    global tmail, username, commentary, origin, tname
    origin = username
    users = User.query.all()
    for u in users:
        if u.username == username:
            form = SettingForm(current_user.username, current_user.email)
            if form.validate_on_submit():
                usernam = form.username.data
                password = form.password.data
                login = form.login.data
                fullname = form.fullname.data
                email = form.email.data
                picture = form.file_object.data
                commentar = form.commentary.data
                if commentar != "":
                   u.commentary = commentar
                   commentary = commentar
                if picture != None:
                   picture.save(app.root_path + '/static/' + picture.filename)
                   u.picture = picture.filename
                if email != "":
                   tmail = email
                   u.email = email
                if fullname != "":
                   u.fullname = fullname
                if login != "":
                   u.login = login
                   tname = login
                if usernam != "":
                   u.username = usernam
                   username = usernam
                if password != "":
                   u.password_hash = password
                db.session.commit()
                return redirect('/profile')
            return render_template('setting.html', form=form)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    form = TranslateForm()
    if form.validate_on_submit():
        text = form.text.data
        lang = form.lang.data
        return render_template('translatePage.html',username=username, commentary=getTranslate(text,lang) ,form=form)
    return render_template('translatePage.html', username=username, commentary="", form=form)

max = 1000
dataOt = ""
dataDo = ""
@app.route('/nasaPhotos', methods=['GET', 'POST'])
def nasaPhotos():
    global max, dataOt, dataDo
    NASA_API_KEY = 'D5hqJAy7JV9dmAnkPrXHFmc1Hcu5cLWULtzxgbKH'
    ROVER_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos'
    params = {
        'sol': 1722,
        'api_key': NASA_API_KEY}
    response = get(ROVER_URL, params=params)
    r_json = response.json()
    max = r_json['photos'][0]['rover']['max_sol']
    ROVER_URL = 'https://epic.gsfc.nasa.gov/api/natural/all'
    response = get(ROVER_URL)
    r_json = response.json()
    dataOt = r_json[len(r_json) - 1]['date']
    dataDo = r_json[0]['date']
    return render_template('nasa_photos.html')

@app.route('/nasaPhotos1', methods=['GET', 'POST'])
def nasaPhotos1():
    form = NasaForm()
    rover = form.rover.data
    data_arr = getPhotoMars(rover)
    if form.validate_on_submit():
        rover = form.rover.data
        data_arr = getPhotoMars(rover)
        return render_template('nasa_photos1.html', photo=data_arr[0], data=data_arr[1], camera=data_arr[2], roverZ=data_arr[3], roverP=data_arr[4], roverPhoto=data_arr[5], roverCameras=data_arr[6],form=form)
    return render_template('nasa_photos1.html',  photo=data_arr[0], data=data_arr[1], camera=data_arr[2], roverZ=data_arr[3], roverP=data_arr[4], roverPhoto=data_arr[5], roverCameras=data_arr[6], form=form)

@app.route('/nasaPhotos2', methods=['GET', 'POST'])
def nasaPhotos2():
    form = NasaPlanetForm()
    date_arr = getPhotoEath()
    return render_template('nasa_photos2.html', photo=date_arr[4], dataYY=date_arr[0], dataMM=date_arr[1], dataDD=date_arr[2], dataTime=date_arr[3], form=form)

@app.route('/Weather', methods=['GET', 'POST'])
def Weather():
    global error
    mounth = ['января', 'февраля', 'марта', 'апреля', 'майя', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    form = WeatherForm()
    if form.validate_on_submit():
        city = form.sity.data
        if city != '':
            date_arr = getWeather(city)
            if date_arr == 'false':
                return render_template('weatherTitle.html', error=error,form=form)
            packet = getWeatherForecast(city)
            data = packet[1]
            time = packet[0]
            count = len(data[0])
            num = []
            for i in time:
                if i==time[0]:
                    num.append('Сегодня')
                else:
                    t = i.split('-')
                    if t[1][0]=='0':
                        t[1] = t[1][1]
                    str = t[2] + ' ' + mounth[int(t[1])-1]
                    num.append(str)
            return render_template('weather.html', conditions=date_arr[0], temp=date_arr[1], temp_min=date_arr[2], temp_max=date_arr[3], data=data, time=time, num=num,  count=count, form=form)
        else:
            error = 'empty'
            return render_template('weatherTitle.html', error=error, form=form)
    return render_template('weatherTitle.html', error=error, form=form)

def getLanguage(text):
    URL = "https://translate.yandex.net/api/v1.5/tr.json/detect"
    KEY = "trnsl.1.1.20200410T163517Z.e887712552657b36.702fa280b24bb6199b4940e4d6022607538153f6"
    Text = text
    params = {
        "key": KEY,
        "text": Text
    }
    response = get(URL, params=params)
    r_json = response.json()
    x = r_json['lang']
    return x

def getTranslate(text, lang):
    URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    KEY = "trnsl.1.1.20200410T163517Z.e887712552657b36.702fa280b24bb6199b4940e4d6022607538153f6"
    if text != '':
        Text = text
        Lang = lang
        params = {
            "key": KEY,
            "text": Text,
            "lang": Lang
        }

        response = get(URL, params=params)
        r_json = response.json()
        x = r_json['text']
        if x[0] == Text:
            return ''
        return x[0]
    return ''

def getPhotoMars(ROVER_URL):
    if ROVER_URL == "None":
       ROVER_URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
    NASA_API_KEY = 'D5hqJAy7JV9dmAnkPrXHFmc1Hcu5cLWULtzxgbKH'
    while True:
        sol = random.randint(0, max)
        params = {'sol': sol, 'api_key': NASA_API_KEY}
        response = get(ROVER_URL, params=params)
        r_json = response.json()
        if 'photos' not in r_json:
            raise Exception
        photos = r_json['photos']
        if not photos:
            continue
        number = random.choice(photos)
        image = number['img_src']
        data = number['earth_date']
        camera = number['camera']['full_name']
        roverZ = number['rover']['launch_date']
        roverP = number['rover']['landing_date']
        roverPhoto = number['rover']['total_photos']
        roverCameras = len(number['rover']['cameras'])
        data_arr = [image, data, camera, roverZ, roverP, roverPhoto, roverCameras]
        return data_arr

def getPhotosEath(YY, MM, DD):
    NASA_API_KEY = 'D5hqJAy7JV9dmAnkPrXHFmc1Hcu5cLWULtzxgbKH'
    ROVER_URL = 'https://epic.gsfc.nasa.gov/api/natural'
    date = YY + "-" + MM + "-" + DD
    if YY == "":
        YY = "2016"
        MM = "10"
        DD = "31"
    date = YY + "-" + MM + "-" + DD
    ROVER_URL = 'https://epic.gsfc.nasa.gov/api/enhanced/date/' + date
    response = get(ROVER_URL)
    r_json = response.json()
    img = r_json[0]['image']
    src = 'https://epic.gsfc.nasa.gov/archive/enhanced/' + YY + "/" + MM + "/" + DD + '/png/' + img + '.png'
    return src

def getPhotoEath():
    NASA_API_KEY = 'D5hqJAy7JV9dmAnkPrXHFmc1Hcu5cLWULtzxgbKH'
    ROVER_URL = 'https://epic.gsfc.nasa.gov/api/enhanced/date/'
    response = get(ROVER_URL)
    r_json = response.json()
    img = r_json[0]['image']
    date = r_json[0]['date']
    date = date.split(' ')
    dateD = date[0].split('-')
    src = 'https://epic.gsfc.nasa.gov/archive/enhanced/' + dateD[0] + "/" + dateD[1] + "/" + dateD[2] + '/png/' + img + '.png'
    date_arr = dateD
    date_arr.append(date[1])
    date_arr.append(src)
    return date_arr

error = 'true'
def getWeather(s_city):
    global error
    appid = "daffb209468d1cb6eb84d10090f2e5f8"
    try:
        params = {
            'q': s_city,
            'units': 'metric',
            'lang': 'ru',
            'APPID': appid
        }
        res = get("http://api.openweathermap.org/data/2.5/weather", params=params)
        data = res.json()
        conditions =  data['weather'][0]['description']
        temp = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        error = 'true'
    except Exception as e:
        error = 'false'
        return error
        print("Exception (weather):", e)
        pass
    data_arr = [conditions, temp, temp_min, temp_max]
    return data_arr

def getWeatherForecast(s_city):
    city_id = 0
    appid = "daffb209468d1cb6eb84d10090f2e5f8"
    params = {
        'q': s_city,
        'units': 'metric',
        'lang': 'ru',
        'APPID': appid
    }

    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params)
        data = res.json()
        data_arr = []
        date_arr = []
        for i in data['list']:
            one = i['dt_txt'].split(' ')
            str = one[1] + '{0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0]['description']
            data_arr.append(str)
            date_arr.append(one[0])
    except Exception as e:
        print("Exception (forecast):", e)
        pass
    array = [date_arr, data_arr]
    arr = [el for el, _ in groupby(date_arr)]
    packet = [arr, array]
    return packet

app.run(port=8080, host='127.0.0.1')