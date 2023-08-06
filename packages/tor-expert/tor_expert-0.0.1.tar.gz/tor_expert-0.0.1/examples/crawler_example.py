import requests
from time import sleep
from tor_expert import tor
from random import randrange


class CrawlerExample(tor.TorBuild):
    def __init__(self):
        tor.TorBuild.__init__(self)
        self.timeout = 60

    def change_ip(self):
        control = tor.create_controller(self.tor_data.ipv4, self.tor_data.control_port)
        control.new_identity(self.tor_data.socket_port, self.tor_data.control_port)
        self.tor_data.tor_ip = tor.check_tor_ip(self.tor_data.socket_port)

    def start(self, url):
        try:
            for n_try in range(10):
                try:
                    proxies = {
                        'http': 'socks5://{0}:{1}'.format(self.tor_data.ipv4, self.tor_data.socket_port),
                        'https': 'socks5://{0}:{1}'.format(self.tor_data.ipv4, self.tor_data.socket_port)}

                    print("current tor ip", self.tor_data.tor_ip)
                    ses = requests.session()
                    resp = ses.get(url, proxies=proxies,timeout=self.timeout)
                    status_code = resp.status_code
                    print("status_code", status_code)
                    print("html response", resp.content)

                    # if ip blocked change ip and try again
                    if status_code != 200:
                        self.change_ip()
                        sleep(randrange(7, 15))
                        continue
                    break
                except TimeoutError:
                    sleep(randrange(7, 15))
                    continue
                except (requests.exceptions.ConnectionError, ):
                    self.change_ip()
                    sleep(randrange(7, 15))
                    continue
        finally:
            self.tor_remove(**self.tor_data.__dict__)


if __name__ == '__main__':
    api = CrawlerExample()
    api.start('https://databank.worldbank.org/')