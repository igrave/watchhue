import requests

my_ip =  '192.168.0.45'
my_username = 

sens = requests.get('http://'+my_ip+'/api/'+my_username+'/sensors') 
sj = sens.json()
sens.ids = sj.keys()
pres_ids = []

for key in sens.ids:
    if sj[key]['type'] == 'ZLLPresence':
        sj[key]['name']
        pres_ids.append(key)

print(pres_ids)

for id in pres_ids:
    r = requests.get('http://'+my_ip+'/api/'+my_username+'/sensors/'+id) 
    print(r.json()["state"])

