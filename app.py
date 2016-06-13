from flask import Flask, render_template, request
import os, requests

app = Flask(__name__, static_url_path='')

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



piserver = "https://192.168.0.2:8000/"                #BACKEND | PISERVER URL HERE
#socket.create_connection(('182.64.172.241', 8000), timeout=2)

@app.route('/')
#@requires_auth
def home():
    #url = piserver + "temp/"
    #send = requests.get(url, verify = False)
    return render_template('index.html')

@app.route('/<string:all_device>/')
#@requires_auth
def master(all_device):
    url = piserver + all_device + '/'
    send = requests.get(url, verify = False)
    return url

@app.route('/<string:device>/<string:device_id>/<string:status>/')
#@requires_auth
def contact_pi(device,device_id,status):
    url = piserver + device +'/' + device_id +'/' + status +'/'

    send = requests.get(url, verify = False)
    return url



if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 5000)))
