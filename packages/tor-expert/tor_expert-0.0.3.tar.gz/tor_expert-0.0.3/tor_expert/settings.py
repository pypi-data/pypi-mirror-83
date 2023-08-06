import getpass

user_folder= r'C:\Users\{}\Documents'.format(getpass.getuser())
tor_base_url = 'https://www.torproject.org'
tor_url = f'{tor_base_url}/download/tor/'
tor_dir = f'{user_folder}\Tor'  # default install path
tor_user_path = f'{user_folder}'
tor_ip_check = 'https://check.torproject.org/'
tor_setup_default = {1: {'number of tor instances': 1}, 2: {'reset identity': 30}, 'tor_path': tor_dir}
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
tor_config = r'{}\tor_config.pkl'.format(user_folder)

tor_settings = r'''# Where data will be stored?
DataDirectory {0}\TorData\data\{1}

# Countdown time before exit
ShutdownWaitLength 5

# Where to write PID
PidFile {0}\TorData\data\{1}\pid

# Communication ports
SocksPort {3}:{1}
ControlPort {3}:{2}

# Authentication of Tor
CookieAuthentication 1

# GeoIP file paths?
GeoIPFile {0}\Data\Tor\geoip
GeoIPv6File {0}\Data\Tor\geoip6

SocksListenAddress {3}
SocksPolicy accept {3}/24
'''