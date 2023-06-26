import threading
import PySimpleGUI as sg
from openai_connector import query_chatgpt
from settings import PROMPTS


sg.theme('SystemDefaultForReal')
layout = [ [sg.Text('Source File'),
            sg.In(size=(53, 1), enable_events=True, key='file'),
            sg.FileBrowse(initial_folder='.', file_types=(('Text files', '*.txt'), ('Markup documents', '.md'), ))
           ],
           [sg.Frame('Protection Options', [[
            sg.Radio('Pseudo-names', group_id='options', key='psudo-name', default=True),
            sg.Radio('Masked', group_id='options', key='mask')]])
           ],
           [sg.Frame('Source Text', [[sg.Multiline(size=(70, 25), key='source')]]),
            sg.Frame('Secured Text', [[sg.Multiline(size=(70, 25), key='output')]])
           ],
           [sg.Text(' ', expand_x=True, key='meh1', justification='center'),
            sg.Text('Secured File'),
            sg.In(size=(51, 1), enable_events=True, key='output_file'),
            sg.FileSaveAs(initial_folder='.', file_types=(('Text files', '*.txt'), ('Markup documents', '.md'), ))
           ],
           [sg.Text(' ', expand_x=True, key='meh2', justification='center'),
            sg.Button('De-identify'),
            sg.Button('    Save    '),
            sg.Button('    Clear   '),
            sg.Button('    Exit    ')
           ]
         ]

# Create the window
window = sg.Window('EncryptEra Information Protector - DEMO', layout)

# Create an event loop
while True:
    event, values = window.read()
    if event == '    Exit    ' or event == sg.WIN_CLOSED:
        break
    elif event == 'file':
        try:
            with open(values['file'], 'r', encoding='UTF-8') as f:
                file = f.read()
                f.close() 
            window['source'].update(file)
        except Exception as e:
            sg.popup_ok(e, title='File Read Error')
    elif event == 'De-identify':
        if values['source'].strip() == '':
            sg.popup_ok('No text is loaded to de-identify!', title='No Text')
            continue
        if values['psudo-name']:
            prompt = PROMPTS[0] + '\n' + values['source']
        elif values['mask']:
            prompt = PROMPTS[1] + '\n' + values['source']

        sg.popup_auto_close('Please wait...', non_blocking=True, no_titlebar=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)
        try:
            response_text = query_chatgpt(prompt)
            window['output'].update(response_text)
        except Exception as e:
            sg.popup_ok(e, title='Proxy Error')
    elif event == '    Clear   ':
        window['file'].update('')
        window['source'].update('')
        window['output'].update('')
        window['output_file'].update('')
    elif event == '    Save    ':
        if values['output'].strip() == '':
            sg.popup_ok('Nothing to save!', title='Content Error')
            continue
        if values['output_file'].strip() == '':
            sg.popup_ok('No filename is provided!', title='Filename Error')
            continue
        try:
            with open(values['output_file'], 'w+', encoding='UTF-8') as f:
                f.write(values['output'])
                f.close() 
        except Exception as e:
            sg.popup_ok(e, title='File Write Error')

window.close()
