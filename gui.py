import sys  
if sys.version_info[0] >= 3:  
    import PySimpleGUI as sg  
else:  
    import PySimpleGUI27 as sg  

layout = [[sg.Button('Authorise'), sg.Text('Code:'),sg.Input(do_not_clear=True, key='_IN_'), sg.Button('Get Token')],
          [sg.Button('Sensors'), sg.Text('', key='_INFO_')],
          [sg.Text('Your typed chars appear here:'), sg.Text('', key='_OUTPUT_') ],  
          [sg.Input(do_not_clear=True, key='_IN_')],  
          [sg.Button('Show'), sg.Button('Exit')]]  

window = sg.Window('Window Title').Layout(layout)  

while True:                 # Event Loop  
  event, values = window.Read()  
  print(event, values)
  if event is None or event == 'Exit':  
      break  
  if event == 'Show':  
      # change the "output" element to be the value of "input" element  
      window.FindElement('_OUTPUT_').Update(values['_IN_'])
  if event =='Authorise':
      sg.PopupQuickMessage('Authorising!')
  if event =='Get Token':
      sg.PopupQuickMessage('Code is '+window.FindElement('_IN_').Get())


window.Close()