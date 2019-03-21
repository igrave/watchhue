

import PySimpleGUI as sg
from time import localtime, strftime
from json import dumps, loads
from WatchHue import WatchHue

w = WatchHue()

# GUI
layout = [[sg.Button('Load'), sg.Button('Save'), sg.Button('Hue Auth'), sg.Button('Refresh Token'), sg.Button('Bridge Auth'), sg.Button('Exit')],
          [sg.Text('URI:'), sg.Input(key='_URI_', do_not_clear=True, default_text='/lights/')],
          [sg.Text('Body:'), sg.Input(default_text='{"hue": 50000, "on": true,"bri": 200}', do_not_clear=True, key='_BODY_', size=(35, 3))],
          [sg.Button('Get'), sg.Button('Put'), sg.Button('Post')],
          [sg.Output(size=(80, 10))],
          [sg.Button('Find Sensors'), sg.Button('Check Sensors')]]

window = sg.Window('Window Title').Layout(layout)

# Initialisation


while True:                 # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break

    if event == 'Load':
        w.loadConfig()
        sg.EasyPrint('Access token: ' + w.access_token, do_not_reroute_stdout=True)
        sg.EasyPrint('Refresh token: ' + w.refresh_token)
        sg.EasyPrint('Refresh token expires: ' + strftime("%x %X", localtime(w.refresh_expires)))
        sg.EasyPrint('Bridge username:' + w.ids['username'])

    if event == 'Save':
        w.saveConfig()

    if event == 'Refresh Token':
        w.refreshTokens()
        sg.EasyPrint('New tokens:')
        sg.EasyPrint('Access token: ' + w.access_token)
        sg.EasyPrint('Refresh token: ' + w.refresh_token)
        sg.EasyPrint('Refresh token expires: ' + strftime("%x %X", localtime(w.refresh_expires)))

    if event == 'Hue Auth':
        w.startAuth()
        text = sg.PopupGetText('Code', 'xxxxxxxx')
        w.setCode(text)
        w.requestTokens()

    if event == 'Bridge Auth':
        w.authWatchHue()
        sg.EasyPrint(w.ids['username'])

    if event == 'Get':
        q = w.getHue(uri=window.FindElement('_URI_').Get())
        sg.EasyPrint("Get:")
        sg.EasyPrint(q.headers)
        print(dumps(q.json(), indent=2))
        window.Refresh()

    if event == 'Put':
        try:
            body = window.FindElement('_BODY_').Get()
            j = loads(body)
        except:
            print('Invalid json in body!')
            continue
        u = window.FindElement('_URI_').Get()
        q = w.putHue(uri=u, json=j)
        sg.EasyPrint("Post:")
        sg.EasyPrint(q.headers)
        print(dumps(q.json(), indent=2))
        window.Refresh()

    if event == 'Post':
        try:
            j = loads(window.FindElement('_BODY_').Get())
        except:
            print('Invalid json in body!')
            continue
        u = window.FindElement('_URI_').Get()
        q = w.postHue(uri=u, json=j)
        sg.EasyPrint("Post:")
        sg.EasyPrint(q.headers)
        print(dumps(q.json(), indent=2))
        window.Refresh()

    if event == 'Find Sensors':
        w.get_pres_sensors_https()

    if event == 'Check Sensors':
        w.get_pres_sensor_state_https()

window.Close()
