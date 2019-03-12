import requests

my_ip =  '192.168.0.45'
my_username = 'pPhwa5anSiPhiJ05YU4fNUENz-RTrcCoZututZwz'

def get_sensor_state(my_ip, my_username, pres_ids):
    pres_states = []
    for id in pres_ids:
        r = requests.get('http://'+my_ip+'/api/'+my_username+'/sensors/'+id) 
        pres_states.append(r.json()["state"])
    
    return pres_states

def get_pres_sensor_states(my_ip, my_username):
    sens = requests.get('http://'+my_ip+'/api/'+my_username+'/sensors') 
    sj = sens.json()
    sens_ids = sj.keys()
    pres_ids = []
    for key in sens_ids:
        if sj[key]['type'] == 'ZLLPresence':
            sj[key]['name']
            pres_ids.append(key)
    return pres_ids


    