import falcon
import json
from service import DNSService
from config import Config
import db

class DNSResource:
    def __init__(self, service):
        self.service = service

    def on_post(self, req, resp):
        token = req.get_param("token", required=True)
        hostname = req.get_param("hostname", required=True)
        ip = req.get_param("ip") or req.env['REMOTE_ADDR']
        self.service.update_dns_record(token, hostname, ip)

class IPResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({ 'ip': req.env['REMOTE_ADDR'] })
        # resp.body = json.dumps(req.env)


def webservice(service):
    app = falcon.API()
    app.add_route('/ip', IPResource())
    app.add_route('/update', DNSResource(service))
    return app
