import requests


class backend(object):


    def __init__(self, cec, password):
        self.cec = cec
        self.password = password
        self.auth_URL = "https://scripts.cisco.com/api/v2/auth/login"


    def authenticate(self):
        self.s = requests.Session()
        self.s.trust_env = False
        self.auth = requests.auth.HTTPBasicAuth(self.cec, self.password)
        self.ret = self.s.get(self.auth_URL, auth=self.auth, verify=False)
        if self.ret.status_code == 200 or self.ret.status_code == 201:
            print("Successfully authenticated!")
            return 1
        elif self.ret.status_code == 401:
            print("Unauthorized, try typing your credentials again")
            return 0
        else:
            print("unexpected login reply (%s): %s",
                  self.ret.status_code, self.ret.text)