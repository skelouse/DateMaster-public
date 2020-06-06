import requests
import json
from os.path import join

class FireBase():
    #wak = 
    #url = 
    url = 'http://localhost:5000/skelouse/todo'
    #headers = {'Content-Type': 'application/json'}
    headers = {"Content-type": "application/json"}
    

    def test(self, name):
        #hero = {'local_id': name}
        hero = {'local_id': name}
        data = json.dumps(hero)
        req = requests.post(self.url, data=data, headers=self.headers)
        print(req.ok)
        print(json.loads(req.content.decode()))

    def sign_in(self, email, password):
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key="+self.wak
        signin_data = {"email": email, "password": password, "returnSecureToken": True}
        signin_request = requests.post(signin_url, data=signin_data)
        signin_data = json.loads(signin_request.content.decode())

        if signin_request.ok == True:
            self.local_id = signin_data['localId']
            self.id_token = signin_data['idToken']
            refresh_token = signin_data['refreshToken']
            filename = join("refresh_token.txt")
            with open(filename, "w") as f:
                f.write(refresh_token)
        else:
            print("Invalid Email or Password")


if __name__ == '__main__':
    fb = FireBase()
    fb.sign_in('test@gmail.com', '123456')
    local_id, id_token = fb.local_id, fb.id_token
    fb.test(local_id)
