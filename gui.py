import sys   
import PySimpleGUI as sg  
from WatchHue import WatchHue

w = WatchHue()

# GUI
layout = [[sg.Button('Load'),sg.Button('Save'),sg.Button('Hue Auth'), sg.Button('Token'), sg.Button('Bridge Auth')],
          [ sg.Text('Code:'),sg.Input(do_not_clear=True, key='_IN_'), sg.Button('Get Token')],
          [sg.Button('Sensors'), sg.Text('', key='_INFO_')],
          [sg.Text('Your typed chars appear here:'), sg.Text('', key='_OUTPUT_') ],  
          [sg.Input(do_not_clear=True, key='_IN_')],  
          [sg.Button('Show'), sg.Button('Exit')],[sg.Output(size=(80,10))]] 

window = sg.Window('Window Title').Layout(layout)  

# Initialisation


while True:                 # Event Loop  
    event, values = window.Read()  
    print(event, values)
    if event is None or event == 'Exit':  
        break  
    if event == 'Show':  
        # change the "output" element to be the value of "input" element  
        window.FindElement('_OUTPUT_').Update(values['_IN_'])
    if event =='Load':
        w.loadConfig()
    if event =='Save':
        w.saveConfig()
    if event =='Hue Auth':
        sg.PopupQuickMessage('Authorising!')
        text = sg.PopupGetText('Code', 'xxxxxxxx')  
    if event =='Get Token':
        sg.PopupQuickMessage('Code is '+window.FindElement('_IN_').Get())


window.Close()