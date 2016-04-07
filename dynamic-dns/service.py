from glesys import GleSYSAPI
from db import Token, Hostname
import uuid
import re

class DNSService:
    def __init__(self, api, db, config):
        self.api = api
        self.db = db
        self.config = config

    def split_host_and_domain(self, hostname, parent_host):
        m = re.search("([A-z0-9]+?)\."+parent_host, hostname)
        if m is None:
            raise Exception("Invalid hostname")
        return m.group(1)

    def create_token(self):
        t = Token()
        t.token = str(uuid.uuid4())
        self.db.add(t)
        self.db.commit()
        return t

    def _get_diff_between_domains(self):
        return self.split_host_and_domain(self.config.get("parent_host"), self.config.get("parent_domain"))

    def create_hostname(self, hostname):
        host = self.split_host_and_domain(hostname, self.config.get("parent_host"))
        h = self._get_diff_between_domains()

        hostname = self.db.query(Hostname).filter_by(host=host, domain=self.config.get("parent_host")).first()
        if hostname:
            print(hostname)
            return hostname

        r = self.api.add_record(host+"."+h, self.config.get("parent_domain"), "127.0.0.1")
        print(r)

        h = Hostname()
        h.host = host
        h.domain = self.config.get("parent_host")
        h.recordid = r['response']['record']['recordid']
        print(h)

        self.db.add(h)
        self.db.commit()
        return h

    def allow_token_to_hostname(self, token, hostname):
        host = self.split_host_and_domain(hostname, self.config.get("parent_host"))
        domainname = self.config.get("parent_host")

        print(host)
        print(domainname)

        token = self.db.query(Token).filter_by(token=token).first()
        hostname = self.db.query(Hostname).filter_by(host=host, domain=domainname).first()

        token.hostnames.append(hostname)
        # self.db.add(token)
        self.db.commit()

    def update_dns_record(self, token, hostname, ip):
        host = self.split_host_and_domain(hostname, self.config.get("parent_host"))
        domainname = self.config.get("parent_host")

        print()
        print()
        hostname = self.db.query(Hostname).filter_by(host=host, domain=domainname).join(Hostname.tokens).filter_by(token=token).first()
        print(hostname)
        if not hostname:
            return

        host = host + "." + self._get_diff_between_domains()
        r = self.api.update_record(hostname.recordid, host, self.config.get("parent_domain"), ip)
        print(r)

    def list_dns_records(self):
        return [d for d in self.api.list_records(domainname) if d]
