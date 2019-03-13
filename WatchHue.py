import requests
import webbrowser
import hashlib
import configparser


# f
class WatchHue:

    def __init__(self):
        self.s = requests.Session()
        self.cfg = configparser.ConfigParser()
        self.access_token = ''
        self.refresh_token = ''
        self.ids = {'clientid': 'F8cAL8xkecuwTQOXHgADY1Zzr9WaskCc',
                    'clientsecret': 'xUlllnef19nMy8I4',
                    'appid': 'watchhue',
                    'deviceid': '9e7ba1a8-38d9-4944-b03d-db0f62689352',
                    'devicename': 'watchhue',
                    'state': '2ab21ac2',
                    'nonce': '',
                    'username': ''}
        self.code = ''
        self.tokReq = {}

    def loadConfig(self):
        self.cfg.read('watchhue.ini')
        # Load proxy settings
        if self.cfg.has_option('Network', 'proxy.http'):
            self.s.proxies['http'] = self.cfg.get('Network', 'proxy.http')
        if self.cfg.has_option('Network', 'proxy.https'):
            self.s.proxies['https'] = self.cfg.get('Network', 'proxy.https')
        # Disable SSL verification (for USZ proxy)
        if self.cfg.has_option('Network', 'verify'):
            self.s.verify = self.cfg.getboolean('Network', 'verify')
        # If access token
        if self.cfg.has_option('Auth', 'access_token'):
            self.access_token = self.cfg.get('Auth', 'access_token')
        # If refresh token
        if self.cfg.has_option('Auth', 'refresh_token'):
            self.access_token = self.cfg.get('Auth', 'refresh_token')

    def startAuth(self):
        call = 'https://api.meethue.com/oauth2/auth?clientid=' + self.ids['clientid'] \
               + '&appid=' + self.ids['appid'] + '&deviceid=' + self.ids['deviceid'] \
               + '&devicename=' + self.ids['devicename'] + '&state=' + self.ids['state'] \
               + '&response_type=code'
        returncall = self.s.get(call)
        webbrowser.open(returncall.url)

    def setCode(self, code):
        assert isinstance(code, str)
        self.code = code

    def requestTokens(self):
        req = self.s.post('https://api.meethue.com/oauth2/token',
                          data={'code': self.code, 'grant_type': 'authorization_code'})

        self.ids['nonce'] = req.headers['WWW-Authenticate'].split('"')[3]

        hash1 = hashlib.md5((self.ids['clientid'] + ':' + 'oauth2_client@api.meethue.com:'
                             + self.ids['clientsecret']).encode('utf-8')).hexdigest()

        hash2 = hashlib.md5('POST:/oauth2/token'.encode('utf-8')).hexdigest()

        response = hashlib.md5((hash1 + ':' + self.ids['nonce'] + ':' + hash2).encode('utf-8')).hexdigest()

        # now we can get the token!
        authString = 'Digest username="' + self.ids['clientid'] \
                     + '", realm="oauth2_client@api.meethue.com", nonce="' + self.ids['nonce'] \
                     + '", uri="/oauth2/token", response="' + response + '"'
        headers = {'Authorization': authString}

        tokenReq = self.s.post('https://api.meethue.com/oauth2/token',
                               data={'code': self.code, 'grant_type': 'authorization_code'},
                               headers=headers)

        self.access_token = tokenReq.json()['access_token']
        self.refresh_token = tokenReq.json()['refresh_token']

    def refreshTokens(self):

        req = self.s.post('https://api.meethue.com/oauth2/refresh',
                          data={'grant_type': 'refresh_token'})

        nonce = req.headers['WWW-Authenticate'].split('"')[3]

        hash1 = hashlib.md5((self.ids['clientid'] + ':' + 'oauth2_client@api.meethue.com:'
                             + self.ids['clientsecret']).encode('utf-8')).hexdigest()

        hash2 = hashlib.md5('POST:/oauth2/refresh'.encode('utf-8')).hexdigest()

        response = hashlib.md5((hash1 + ':' + nonce + ':' + hash2).encode('utf-8')).hexdigest()

        # now we can get the token!
        authString = 'Digest username="' + self.ids['clientid'] \
                     + '", realm="oauth2_client@api.meethue.com", nonce="' + nonce \
                     + '", uri="/oauth2/refresh", response="' + response + '"'

        tokenReq = self.s.post('https://api.meethue.com/oauth2/refresh',
                               data={'refresh_token': self.refresh_token},
                               params={'grant_type': 'refresh_token'},
                               headers={'Authorization': authString,
                                        'content-type': 'application/x-www-form-urlencoded'})
        self.tokReq = tokenReq

        self.access_token = tokenReq.json()['access_token']
        self.refresh_token = tokenReq.json()['refresh_token']



    def authWatchHue(self):
        self.s.put('https://api.meethue.com/bridge/0/config',
                   json={"linkbutton":True},
                   headers={'content-type':'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)}
                   )

        req_whitelist = self.s.post('https://api.meethue.com/bridge/',
                    headers={'content-type':'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
                    json={"devicetype": "watchhue"})

        self.ids['username'] = req_whitelist.json()[0]['success']['username']