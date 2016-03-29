import falcon
import json

class DNSResource:
    def __init__(self, db):
        self.db = db

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        pass

class IPResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({ 'ip': req.env['REMOTE_ADDR'] })
        # resp.body = json.dumps(req.env)


app = falcon.API()
app.add_route('/ip', IPResource())
# app.add_route('/update', DNSResource())
