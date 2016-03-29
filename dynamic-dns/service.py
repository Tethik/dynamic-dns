from glesys import GleSYSAPI
from db import Token, Hostname
import uuid

class DNSService:
    def __init__(self, api, db):
        self.api = api
        self.db = db

    def split_host_and_domain(self, hostname):
        splits = hostname.split('.')
        host = splits[0]
        domainname = '.'.join(splits[1:])
        return (host, domainname)

    def create_new_token(self):
        t = Token()
        t.token = str(uuid.uuid4())
        self.db.add(t)
        self.db.commit()
        return t

    def create_new_hostname(self, hostname):
        host, domainname = split_host_and_domain(hostname)

        h = Hostname()
        h.host = host
        h.domain = domainname

        self.db.add(h)
        self.db.commit()
        return h

    def allow_token_to_hostname(self, token, hostname):
        host, domainname = split_host_and_domain(hostname)

        token = self.db.query(Token).filter_by(token=token).first()
        hostname = self.db.query(Hostname).filter_by(host=host, domain=domainname).first()

        if hostname in token.hostnames:
            return

        token.hostnames.append(hostname)
        self.db.commit()

    def update_dns_record(self, token, hostname):
        host, domainname = split_host_and_domain(hostname)

        token = self.db.query(Token).filter_by(token=token).first()
        if hostname in token.hostnames:
            return

        records = self.api.list_records(domainname)
