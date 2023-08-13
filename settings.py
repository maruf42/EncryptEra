OPENAI_API_KEY = '70d773eddedf4b16830fd49b3d610a5f'
OPENAI_HOST = 'ao-wl-eus-anzx.openai.azure.com'
OPENAI_PATH = '/openai/deployments/CTOTest/chat/completions'
OPENAI_URL = 'https://' + OPENAI_HOST + OPENAI_PATH
OPENAI_API_VERSION = '2023-03-15-preview'
OPENAI_MODEL = 'gpt-35-turbo'
PROXY_URL = 'http://127.0.0.1:9000/'

PROMPTS = [
    'Alter all the sensitive information form the below text by replacing them with XXX. Use the same number of X as the length of the original text. Replace all names, address, email, phone/fax numbers, identifiers, dates, times, dollar amounts:',
    'Alter all the sensitive information form the below text using real sounding psudo-names. Replace all names, address, email, phone/fax numbers, identifiers, dates, times, dollar amounts:',
    'Extract all the sensitive information from the below text and associate them with the type of information:'
]
