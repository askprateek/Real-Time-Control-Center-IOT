from flask import Flask, render_template, request
import os, requests, json, ssl
from flask.json import jsonify

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

app = Flask(__name__, static_url_path='')

# url_for('static', filename='style.css')

# piserver = "http://172.16.15.225:8000/"

piserver = "http://192.168.0.4:8000/"                #BACKEND | PISERVER URL HERE
#socket.create_connection(('182.64.172.241', 8000), timeout=2)

@app.route('/')
#@requires_auth
def home():
    url = piserver + "device/"

    r = requests.get(url)
    # d = json.dumps(str(r))
    # data = json.load(d)
    # x = json.loads(str(r), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    # return json.loads(r.text)
    api = json.loads(r.text)
    home = set()
    for device in api:
        home.add(device['room'])
    return render_template('test.html', devices = api ,home =home)
    #return json.dumps(data)



@app.route('/api/')
def device():
    url = piserver + "device/"
    return requests.get(url, verify =False).content

# @app.route('/<string:all_device>/')
# #@requires_auth'''
#
# # def master(all_device):
# #     url = piserver + all_device + '/'
# #     send = requests.get(url, verify = False)
# #     return url

@app.route('/<string:device>/<string:device_id>/<string:status>/')
#@requires_auth
def contact_pi(device,device_id,status):
    url = piserver + device +'/' + device_id +'/' + status +'/'

    send = requests.get(url, verify = False)
    return url



if __name__ == "__main__":
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 80)))
