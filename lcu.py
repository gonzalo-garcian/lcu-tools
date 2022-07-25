import requests, json

class LeagueClientUpdate():

    def __init__(self, user = None, password = None, port = None, host = None, ssl_certificate = None):

        if user != None:
            self.__CONST_USER = user
        else:
            self.__CONST_USER = 'riot'

        self.__CONST_PASSWORD = password

        self.__CONST_PORT = port

        if host != None:
            self.__CONST_HOST = host
        else:
            self.__CONST_HOST = '127.0.0.1'

        if ssl_certificate != None:
            self.__CONST_SSL_CERTIFICATE = ssl_certificate
        else:
            self.__CONST_SSL_CERTIFICATE = 'riotgames.pem'


    def get_user(self):

        return self.__CONST_USER


    def get_password(self):

        return self.__CONST_PASSWORD


    def get_port(self):

        return self.__CONST_PORT


    def load_lockfile(self, path = None):

        if path != None:
            self.__CONST_PATH = path
        else:
            self.__CONST_PATH = 'C:\Riot Games\League of Legends\lockfile'

        lockfile = open(self.__CONST_PATH, 'r').read().split(':')

        self.__CONST_PASSWORD = lockfile[3]

        self.__CONST_PORT = lockfile[2]


    def GET(self, endpoint, json_filename = None):
        
        open(f'{json_filename}.json', 'wb').write(requests.get( f'https://{self.__CONST_HOST}:{self.__CONST_PORT}{endpoint}',
                       auth = requests.auth.HTTPBasicAuth(self.__CONST_USER, self.__CONST_PASSWORD),
                       verify = self.__CONST_SSL_CERTIFICATE,
                       allow_redirects = True ).content )


    def PUT(self, endpoint, json_filename = None, put_json_path = None):
        
        open(f'{json_filename}.json', 'wb').write(requests.put( f'https://{self.__CONST_HOST}:{self.__CONST_PORT}{endpoint}',
                       auth = requests.auth.HTTPBasicAuth(self.__CONST_USER, self.__CONST_PASSWORD),
                       verify = self.__CONST_SSL_CERTIFICATE,
                       data = open(put_json_path, 'r').read(),
                       allow_redirects = True ).content )


    def POST(self, endpoint, json_filename = None, put_json_path = None):
        
        open(f'{json_filename}.json', 'wb').write(requests.post( f'https://{self.__CONST_HOST}:{self.__CONST_PORT}{endpoint}',
                       auth = requests.auth.HTTPBasicAuth(self.__CONST_USER, self.__CONST_PASSWORD),
                       verify = self.__CONST_SSL_CERTIFICATE,
                       data = open(put_json_path, 'r').read(),
                       allow_redirects = True ).content )