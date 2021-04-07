from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    volumes = [round(x * 0.2, 1) for x in range(1, 40)]
    return render_template('index.html', len=len(volumes), volumes=volumes)


if __name__ == '__main__':
    app.run(debug=True)
