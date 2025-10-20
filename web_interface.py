import uasyncio
from lib.microdot import Microdot, redirect, send_file
import ujson
from constants import SETTINGS_FILE  # Your settings file path

USERNAME = 'admin'
PASSWORD = 'thsensor'

app = Microdot()

# Auth check (simple for demo)
def requires_auth(func):
    async def wrapper(request, *args, **kwargs):
        if request.headers.get('Authorization') != 'Basic YWRtaW46dGhzZW5zb3I=':  # Base64 of admin:thsensor
            return 'Unauthorized', 401
        return await func(request, *args, **kwargs)
    return wrapper

# Static CSS
@app.route('/static/<path:path>')
async def static(request, path):
    return send_file('/static/' + path)

# / : Info page (no login)
@app.route('/')
async def index(request):
    return """
    <html><head><link rel="stylesheet" href="/static/pico.min.css"></head>
    <body><h1>Device Info</h1><p>Welcome. Links: <a href="/diagnostics">Diagnostics</a> | <a href="/sysinfo">Sysinfo</a> | <a href="/setup">Setup</a></p></body></html>
    """

# /diagnostics : Show sensor data, test LED (no login)
@app.route('/diagnostics')
async def diagnostics(request):
    # Fake data; replace with real sensor/led
    temp = 25.0
    hum = 50.0
    return f"""
    <html><head><link rel="stylesheet" href="/static/pico.min.css"></head>
    <body><h1>Diagnostics</h1><p>Temp: {temp}°C | Hum: {hum}%</p>
    <form method="post"><button name="led" value="on">LED On</button><button name="led" value="off">LED Off</button></form></body></html>
    """

@app.route('/diagnostics', methods=['POST'])
async def diagnostics_post(request):
    # Handle LED; add your code
    print("LED action:", request.form.get('led'))
    return redirect('/diagnostics')

# /sysinfo : System info (login required)
@app.route('/sysinfo')
@requires_auth
async def sysinfo(request):
    return """
    <html><head><link rel="stylesheet" href="/static/pico.min.css"></head>
    <body><h1>System Info</h1><p>Uptime: N/A | Restart reason: N/A</p></body></html>
    """

# /setup : Change settings (login required)
@app.route('/setup')
@requires_auth
async def setup(request):
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = ujson.load(f)
    except:
        settings = {}
    return f"""
    <html><head><link rel="stylesheet" href="/static/pico.min.css"></head>
    <body><h1>Setup</h1>
    <form method="post">
        WiFi SSID: <input name="wifi_ssid" value="{settings.get('wifi_ssid', '')}"><br>
        WiFi Password: <input name="wifi_password" value="{settings.get('wifi_password', '')}"><br>
        NTP Host: <input name="ntp_host" value="{settings.get('ntp_host', 'pool.ntp.org')}"><br>
        <button>Save</button>
    </form></body></html>
    """

@app.route('/setup', methods=['POST'])
@requires_auth
async def setup_post(request):
    new_settings = {
        'wifi_ssid': request.form['wifi_ssid'],
        'wifi_password': request.form['wifi_password'],
        'ntp_host': request.form['ntp_host']
    }
    with open(SETTINGS_FILE, 'w') as f:
        ujson.dump(new_settings, f)
    # Go to ConnectionCheck (add your state change)
    return 'Saved! Restarting...'

# Run in Configuration state
async def run_server():
    await app.start_server(host='0.0.0.0', port=80)