import json, os, urllib.request, urllib.error
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '').strip()
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '').strip()
PORT = int(os.environ.get('PORT', '8080'))

def telegram_send(text):
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError('Telegram is not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env, then restart the server.')
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    body = json.dumps({'chat_id': CHAT_ID, 'text': text, 'disable_web_page_preview': True}).encode()
    req = urllib.request.Request(url, data=body, headers={'Content-Type':'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            data=json.loads(response.read().decode())
            if not data.get('ok'): raise RuntimeError(data.get('description','Telegram API rejected the message'))
    except urllib.error.HTTPError as e:
        detail=e.read().decode(errors='replace')[:300]
        raise RuntimeError(f'Telegram API error {e.code}: {detail}')

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT), **kwargs)
    def send_json(self, code, data):
        raw=json.dumps(data).encode(); self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        if urlparse(self.path).path not in ('/api/alert','/api/location'):
            return self.send_json(404, {'error':'Endpoint not found'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length > 12000: return self.send_json(413, {'error':'Request too large'})
            data=json.loads(self.rfile.read(length).decode('utf-8'))
            loc=data.get('location') or {}
            coords='Location unavailable'
            if isinstance(loc,dict) and 'latitude' in loc and 'longitude' in loc:
                coords=f"{loc['latitude']}, {loc['longitude']}"
            map_url=data.get('map_url') or (f'https://maps.google.com/?q={coords}' if coords != 'Location unavailable' else '')
            if self.path == '/api/alert':
                msg=(f"🚨 RAKSHANET SOS TEST ALERT\nProject lead: Vijaysimha\nType: {str(data.get('type','SOS'))[:80]}\nTime: {str(data.get('timestamp',''))[:80]}\nLocation: {coords}" + (f"\nMap: {map_url}" if map_url else '') + '\n\nThis is a project alert, not an emergency-services dispatch.')
                telegram_send(msg)
                return self.send_json(200, {'ok':True,'message':'Telegram alert sent to the configured chat.'})
            msg=(f"📍 RakshaNet location update\nProject lead: Vijaysimha\nTime: {str(data.get('timestamp',''))[:80]}\nLocation: {coords}" + (f"\nMap: https://maps.google.com/?q={coords}" if coords != 'Location unavailable' else ''))
            telegram_send(msg)
            return self.send_json(200, {'ok':True,'message':'Location update sent.'})
        except Exception as e:
            return self.send_json(400, {'error':str(e)[:500]})
    def log_message(self, fmt, *args): print('%s - %s' % (self.address_string(), fmt % args))

if __name__ == '__main__':
    os.chdir(ROOT)
    print(f'RakshaNet running at http://localhost:{PORT}')
    print('Telegram configured:', bool(BOT_TOKEN and CHAT_ID))
    ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
