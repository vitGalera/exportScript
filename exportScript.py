import json
import pycurl
from StringIO import StringIO
from zipfile import ZipFile

class InMemoryZipFile(object):
    def __init__(self, stringIO):
        self.inMemoryOutputFile = stringIO

    def write(self, inzipfilename, data):
        zip = ZipFile(self.inMemoryOutputFile, 'a')
        zip.writestr(inzipfilename, data)
        zip.close()

    def read(self):
        self.inMemoryOutputFile.seek(0)
        return self.inMemoryOutputFile.getvalue()

    def writetofile(self, filename):
        open(filename, 'wb').write(self.read())


CREDENTIALS_PATH = "../credentials.json"

def load_credentials(file_path=CREDENTIALS_PATH):
    with open(CREDENTIALS_PATH) as credentials:
        res = json.load(credentials)
    return res

def get_data(filename=None, start='20180521t00', end='20180521t23'):
    """
    Retrieves data from amplitude
    """
    if not filename:
        filename = start + ':' + end
    cred = load_credentials()
    API_KEY = cred['vitcord']['APIKey']
    SECRET_KEY = cred['vitcord']['secretKey']
    URL = 'https://amplitude.com/api/2/export?start={start}&end={end}'.format(start=start, end=end)
    stringIO = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, URL)
    c.setopt(pycurl.USERPWD, '{API}:{SECRET}'.format(API=API_KEY, SECRET=SECRET_KEY))
    c.setopt(c.WRITEDATA, stringIO)
    c.perform()
    c.close()
    in_memory_file = InMemoryZipFile(stringIO)
    in_memory_file.writetofile(filename)
    return True
