
import requests
import webbrowser
import hashlib


my_ip =  '192.168.0.45'
my_username = 'pPhwa5anSiPhiJ05YU4fNUENz-RTrcCoZututZwz'

clientid = 'F8cAL8xkecuwTQOXHgADY1Zzr9WaskCc'
clientsecret = 'xUlllnef19nMy8I4'
appid = 'watchhue'
deviceid  = '9e7ba1a8-38d9-4944-b03d-db0f62689352'
devicename = 'watchhue'
state = '2ab21ac2-9ca5-4b51-802c-fbbfd06a0c48'
call = 'https://api.meethue.com/oauth2/auth?clientid='+clientid+'&appid='+appid+'&deviceid='+deviceid+'&devicename='+devicename+'&state='+state+'&response_type=code'

returncall = requests.get(call)

webbrowser.open(returncall.url)


# opens the Hue webpage -> allow app -> redirect to page with code
code='yoRxXybi'
req = requests.post('https://api.meethue.com/oauth2/token',data={'code':code,'grant_type':'authorization_code'})

nonce = req.headers['WWW-Authenticate'].split('"')[3]

hash1 = hashlib.md5((clientid+':'+'oauth2_client@api.meethue.com:'+clientsecret).encode('utf-8')).hexdigest()

hash2 = hashlib.md5('POST:/oauth2/token'.encode('utf-8')).hexdigest()

response = hashlib.md5((hash1 + ':'+ nonce + ':'+hash2).encode('utf-8')).hexdigest()

#now we can get the token!
Auth_string = 'Digest username="'+clientid+'", realm="oauth2_client@api.meethue.com", nonce="'+nonce+'", uri="/oauth2/token", response="'+response+'"'
headers = {'Authorization':Auth_string}

token_req = requests.post('https://api.meethue.com/oauth2/token', data={'code':code,'grant_type':'authorization_code'}, headers = headers)

#now we should have the tokens!
access_token = token_req.json()['access_token']
token_req.json()['refresh_token']

bearer_token = 'Bearer '+ access_token

requests.put('https://api.meethue.com/bridge/0/config', json={"linkbutton":True},headers={'Authorization': bearer_token, 'Content-Type':'application/json'})


requests.put('https://api.meethue.com/bridge/0/config',
      json={'linkbutton':'true'},
      headers={'content-type':'application/json',
               'Authorization': 'Bearer {}'.format(access_token)})



a = requests.post('https://api.meethue.com/bridge/',
headers={'Content-Type':'application/json',
               'Authorization': 'Bearer o7w1p1CPcd5xiDvDmxtdscu9I8qI'},
               json={"devicetype":"watchhue"})
a.headers
username = a.json()[0]['success']['username']

def get_pres_sensor_state_https(my_username, pres_ids):
    pres_states = []
    for id in pres_ids:
        r = requests.get('https://api.meethue.com/bridge/'+my_username+'/sensors/'+id,
        headers={'Authorization': bearer_token}) 
        pres_states.append(r.json()["state"])
    return pres_states

get_pres_sensor_state_https(username, ['33'])
