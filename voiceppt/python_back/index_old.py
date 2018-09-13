from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '11798235'
API_KEY = 'aL7V21ao41uZSNdwRzSfGYUi'
SECRET_KEY = 'OxN8NixEoRo3rWUj1zVY3EI8Nmlrw6xj'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


result = client.asr(get_file_content('22.wav'), 'wav', 16000, {
    'dev_pid': 1536,
})

print (result)