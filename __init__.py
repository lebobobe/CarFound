from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    volumes = [round(x * 0.2, 1) for x in range(1, 40)]
    return render_template('index.html', len=len(volumes), volumes=volumes, brand='Toyota',
        model='Celica', price='630000', city='Москва', year='1995', mileage='221337',
        volume='3.0', hp='228', fuel_type='Бензин', transmission='Механическая',
        WD='Задний', wheel_drive='Правый', body='Купе', color='Черный',
        condition='Не битая', owners='3+',
        pic_url='https://sun9-39.userapi.com/impg/6NGwMBoUnUhcniGvoBiEJ-yX8SRcQUj020XO-A/NvL8YGVCk0I.jpg?size=2048x1536&quality=96&sign=2028ee00be27a2cd9eac1126b34548ab&type=album',
        listing_url='https://auto.ru/cars/used/sale/toyota/celica/1103113371-a2d4da4c/')


@app.route('/authentication')
def authentication():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
