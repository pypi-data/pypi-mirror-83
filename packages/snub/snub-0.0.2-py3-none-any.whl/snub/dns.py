import os, socket, time
from threading import Thread
from .base import Base


class DNS(Base):

    __dns_spam_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'dns.spam' + '.yml'))
    __dns_spam_list = []

    def __init__(self):
        if not self.__dns_spam_list:
            self.__dns_spam_list = self.get_yml_data(self.__dns_spam_path)['spam']
        self.__spam_list = []
        self._threads = []

    def _check_dns_blacklist(self, ip, server):
        try:
            url = '{ip}.{server}'.format(ip=ip, server=server)
            res = socket.gethostbyname(url)
            self.__spam_list.append({
                'blacklist': server,
                'url': url,
                'ip': self._reverse_ip_address(ip)
            })
        except socket.gaierror:
            pass

    def _check_dns_blacklists(self, ip):
        for server in self.__dns_spam_list:
            t = Thread(target=self._check_dns_blacklist, args=(ip,server,))
            t.start()
            time.sleep(0.1)
            self._threads.append(t)

    def check(self, value):
        ip = None
        try:
            if self.is_valid_ipv4_address(value):
                ip = self._reverse_ip_address(value)
            elif self.is_valid_ipv6_address(value):
                ip = self._reverse_pointer(value)
            else:
                ip = self._reverse_ip_address(socket.gethostbyname(value))
        except:
            return None
        self._check_dns_blacklists(ip)
        while len(self._threads) > 0:
            new_threads = []
            for t in self._threads:
                if t and t.isAlive():
                    new_threads.append(t)
            self._threads = new_threads
            time.sleep(1)
        return {
            'list': self.__spam_list,
            'count': len(self.__spam_list)
        }

    def _reverse_ip_address(self, ip):
        if len(ip) <= 1:
            return ip
        l = ip.split('.')
        return '.'.join(l[::-1])

    def _reverse_pointer(self, ip):
        """Return the reverse DNS pointer name for the IPv6 address.

        This implements the method described in RFC3596 2.5.

        """
        reverse_chars = self.exploded[::-1].replace(':', '')
        return '.'.join(reverse_chars)

    def is_valid_ipv4_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True

    def is_valid_ipv6_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True
