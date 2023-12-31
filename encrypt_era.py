import PySimpleGUI as sg
from openai_connector import query_chatgpt
from settings import PROMPTS


sg.theme('SystemDefaultForReal')
layout = [ [sg.Text('Source File'),
            sg.In(size=(53, 1),  key='file', enable_events=True, disabled=True),
            sg.FileBrowse(initial_folder='.', key='browse_in', target='file', file_types=(('Text files', '*.txt'), ('Markup documents', '.md'), ))
           ],
           [sg.Frame('Operations', [[
            sg.Frame('Anonymise Options', [[
                sg.Radio('Masked', group_id='options', key='mask', default=True),
                sg.Radio('Pseudo-names', group_id='options', key='psudo-name'),
            ]]),
            sg.Radio('Information Extraction', group_id='options', key='ie'),
           ]])
           ],
           [sg.Frame('Source Text', [[sg.Multiline(size=(100, 45), key='source')]]),
            sg.Frame('Converted Text', [[sg.Multiline(size=(100, 45), key='output')]])
           ],
           [sg.Push(),
            sg.Text('Secured File'),
            sg.In(size=(51, 1), key='output_file', enable_events=True, disabled=True),
            sg.FileSaveAs(initial_folder='.', key='browse_out', target='output_file', default_extension='.txt', file_types=(('Text files', '*.txt'), ('Markup documents', '.md'), ))
           ],
           [sg.Push(),
            sg.Button('Execute', size=(10, 1)),
            sg.Button('Clear', size=(10, 1)),
            sg.Button('Exit', size=(10, 1))
           ]
         ]

# Create the window
window = sg.Window('EncryptEra Information Protector - DEMO', layout)

# Create an event loop
while True:
    event, values = window.read()
    if event in ('Exit', sg.WIN_CLOSED):
        break
    elif event == 'file':
        try:
            with open(values['file'], 'r', encoding='UTF-8') as f:
                file = f.read()
                f.close() 
            window['source'].update(file)
        except Exception as e:
            sg.popup_ok(e, title='File Read Error')
    elif event == 'Execute':
        if values['source'].strip() == '':
            sg.popup_ok('No text is loaded to process!', title='No Text')
            continue
        if values['mask']:
            prompt = PROMPTS[0] + '\n' + values['source']
        elif values['psudo-name']:
            prompt = PROMPTS[1] + '\n' + values['source']
        elif values['ie']:
            prompt = PROMPTS[2] + '\n' + values['source']

        sg.popup_auto_close('Please wait...', non_blocking=True, no_titlebar=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)
        try:
            response_text = query_chatgpt(prompt)
            window['output'].update(response_text)
        except Exception as e:
            sg.popup_ok(e, title='Proxy Error')
    elif event == 'Clear':
        window['file'].update('')
        window['source'].update('')
        window['output'].update('')
        window['output_file'].update('')
    elif event == 'output_file':
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
