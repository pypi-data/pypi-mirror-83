import subprocess
from flask import Flask
from flask_restful import Api, Resource, reqparse


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


try:
    from snub import Snub
except ImportError:
    print("Trying to Install required module: requests")
    install_and_import('../setup.py')


from snub import Snub

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return "Flask API"

@app.route('/snub/search/<string:value>')
def search(value):
    snubbed = Snub().check(value, text_list=True, dns_list=True, static_list=True)
    return "{}".format(snubbed)

@app.route('/snub/blackhole/<string:value>')
def search_text_lists(value):
    snubbed = Snub().check(value, text_list=True)
    return "{}".format(snubbed)

@app.route('/snub/dns/<string:value>')
def search_dns_blacklist(value):
    snubbed = Snub().check(value, dns_list=True)
    return "{}".format(snubbed)

@app.route('/snub/static/<string:value>')
def search_static_blacklist(value):
    snubbed = Snub().check(value, static_list=True)
    return "{}".format(snubbed)

app.run(debug=True, host='0.0.0.0')