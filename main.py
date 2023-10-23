from pywebio.platform.flask import webio_view
from flask import Flask, request, redirect
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from config import *
import tinydb

app = Flask(__name__)
links = tinydb.TinyDB('database.json')
Link = tinydb.Query()

@app.get("/<slg>")
def slug(slg):
    link = links.get(Link.text == slg)
    return redirect(link['url'])

def ui():
    put_text("Добро пожаловать в nlink")

    data = input_group("Создание ссылки", [
        input("Длинная ссылка", name="url"),
        input("Текст ссылки", name="text")
    ])

    link = links.get(Link.text == data['text'])
    if link is None:
        links.insert({"text": data['text'], "url": data['url']})
        put_html("Ссылка создана: " + f"<a href=\"{LINK_URL + '/' + data['text']}\">{LINK_URL + '/' + data['text']}</a>")
    else:
        put_error("Ссылка с таким текстом уже существует.")

def start_flask_server():
    app.add_url_rule('/', 'webio_view', webio_view(ui), methods=['GET', 'POST', 'OPTIONS'])
    app.run(host='0.0.0.0', port=8888, debug=True)


if __name__ == '__main__':
    start_flask_server()
