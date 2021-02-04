from dataclasses import dataclass


@dataclass
class Device:
    """ Class to store information pertaining to a smart device"""
    vendor: str
    services: dict

    def match_services(self, ext_services):
        for service in ext_services:
            try:
                if (str(service) in self.services['tcp']) and (ext_services[service]['state'] == 'open'):
                    return True
            except KeyError:
                return False

        return False

    def match(self, ext_vendor, ext_services):
        if (self.vendor != '') and (self.vendor.lower().replace(' ','') == ext_vendor.lower().replace(' ','')):
            return True
        else:
            return self.match_services(ext_services)


arlo_device = Device(
                vendor='Arlo Technology',
                services={
                    'tcp': {
                        '5061': 'sip-tls',
                    },
                    'udp': {

                    }
                }
            )

categories = {
    'FRIDGE': {
            'devices': {}
        },
    'ROUTER': {
            'devices': {}
        },
    'CAMERA': {
        'devices': {
            'ArloHub': arlo_device,
            'Generic RTSP Device': Device(
                vendor='',
                services={
                    'tcp': {
                        '554': 'rtsp'
                    },
                    'udp': {

                    }
                }
            ),
        }
    },
    'DOORBELL': {
        'devices': {
            'ArloHub': arlo_device
        }
    },
    'LOCK': {
        'devices': {}
    },
    'SECURITY': {
            'devices': {}
        },
    'PARENTAL_CONTROLS': {
            'devices': {}
        },
    'PHONES': {
        'devices': {
            'iPhone': Device(
                vendor='',
                services={
                    'tcp': {
                        '62078': 'iphone-sync'
                    },
                    'udp': {

                    }
                })
        }
    },
    'NONE': {
            'devices': {}
        },
    }