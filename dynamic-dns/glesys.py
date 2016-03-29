import requests
import json

class GleSYSAPI:
    headers = {'content-type': 'application/json'}

    def __init__(self, auth_user, auth_token):
        self.auth = (auth_user, auth_token)

    def update_record(self, recordid, host, domain_name, ip):
        url = 'https://api.glesys.com/domain/updaterecord'
        data = {
            recordid: recordid,
            host: host,
            domainname: domain_name,
            data: ip,
            type: 'A'
        }
        resp = requests.post(url, auth=self.auth,
            headers=self.headers, data =json.dumps(data))
        r = resp.json()
        return r

    def add_record(self, host, domain_name, ip):
        url = 'https://api.glesys.com/domain/addrecord'
        data = {
            host: host,
            domainname: domain_name,
            data: ip,
            type: 'A'
        }
        resp = requests.post(url, auth=self.auth,
            headers=self.headers, data =json.dumps(data))
        r = resp.json()
        return r

    def list_domains(self):
        url = 'https://api.glesys.com/domain/list'
        resp = requests.get(url, auth=self.auth, headers=self.headers)
        r = resp.json()
        return r['response']['domains']

    def list_records(self, domain_name):
        url = 'https://api.glesys.com/domain/listrecords'
        data = {'domainname': domain_name }
        resp = requests.post(url, auth=self.auth, headers=self.headers,
            data = json.dumps(data))
        r = resp.json()
        return [r for r in r['response']['records'] if r['type'] == 'A']
