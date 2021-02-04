from PyInquirer import prompt, Separator
import socket
from sources.data.data import categories
from sources.blackout import Blackout

blkout = r'''
 ________  ___       ________  ________  ___  __    ________  ___  ___  _________        ___      ___ ________    _____     ________     
|\   __  \|\  \     |\   __  \|\   ____\|\  \|\  \ |\   __  \|\  \|\  \|\___   ___\     |\  \    /  /|\   __  \  / __  \   |\_____  \    
\ \  \|\ /\ \  \    \ \  \|\  \ \  \___|\ \  \/  /|\ \  \|\  \ \  \\\  \|___ \  \_|     \ \  \  /  / | \  \|\  \|\/_|\  \  \|____|\ /_   
 \ \   __  \ \  \    \ \   __  \ \  \    \ \   ___  \ \  \\\  \ \  \\\  \   \ \  \       \ \  \/  / / \ \  \\\  \|/ \ \  \       \|\  \  
  \ \  \|\  \ \  \____\ \  \ \  \ \  \____\ \  \\ \  \ \  \\\  \ \  \\\  \   \ \  \       \ \    / /   \ \  \\\  \ __\ \  \ ___ __\_\  \ 
   \ \_______\ \_______\ \__\ \__\ \_______\ \__\\ \__\ \_______\ \_______\   \ \__\       \ \__/ /     \ \_______\\__\ \__\\__\\_______\
    \|_______|\|_______|\|__|\|__|\|_______|\|__| \|__|\|_______|\|_______|    \|__|        \|__|/       \|_______\|__|\|__\|__\|_______|                                                                                                                                                                                                                                                           
 '''


def make_multi_category(cats: list):
    dictionary = {
        'devices': {}
    }
    if len(cats) == 0:  # treat as all
        for key in categories.keys():
            dictionary['devices'].update(categories[key]['devices'])
    else:
        for key in cats:
            dictionary['devices'].update(categories[key]['devices'])
    return dictionary


choice_dict = {
    'NO ICEREAM FOR U - Disable Fridges': categories['FRIDGE'],
    'LIGHTS OUT - Disable Cameras': categories['CAMERA'],
    'DING DONG - Disable Doorbells': categories['DOORBELL'],
    'LOCKED OUT - Disable Locks': categories['LOCK'],
    'CONTAINMENT BREACH - Disable Security Systems': categories['SECURITY'],
    'TIMMY - Disable Parental Controls': categories['PARENTAL_CONTROLS'],
    'DIALTONE - Disable Phones (and homekit)': categories['PHONES'],
    'GHOST - Disable Cameras, Doorbells, Security, Parental Controls': make_multi_category(['CAMERA', 'DOORBELL',
                                                                                            'SECURITY',
                                                                                            'PARENTAL_CONTROLS']),
    'EXFIL - Disable Cameras, Doorbells, Security, Locks': make_multi_category(['CAMERA', 'DOORBELL', 'SECURITY', 'LOCK']),
    'HAIL_MARY - Enable All Rules': make_multi_category([]),
    'NONE - Specific Devices': categories['NONE'],
}

main_menu = [
    {
        'type': 'list',
        'name': 'rule',
        'message': 'Select a blocking rule',
        'choices': ['NO ICEREAM FOR U - Disable Fridges',
                    'LIGHTS OUT - Disable Cameras',
                    'DING DONG - Disable Doorbells',
                    'LOCKED OUT - Disable Locks',
                    'CONTAINMENT BREACH - Disable Security Systems',
                    'TIMMY - Disable Parental Controls',
                    'DIALTONE - Disable Phones (and homekit)',
                    Separator(),
                    'GHOST - Disable Cameras, Doorbells, Security, Parental Controls',
                    'EXFIL - Disable Cameras, Doorbells, Security, Locks',
                    'HAIL_MARY - Enable All Rules',
                    Separator(),
                    'NONE - Specific Devices'
                    ],
    },
]


def intro_sequence():
    # Use a breakpoint in the code line below to debug your script.
    print(f'{blkout}\n\n\n\n')
    input('Hit Enter to continue...')
    answers = prompt(main_menu)
    return answers['rule']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rule = intro_sequence()
    category = choice_dict[rule]

    addr_block = f'{socket.gethostbyname(socket.gethostname()).rsplit(".", 1)[0]}.0/24'

    blackout = Blackout(category)

    blackout.update_hosts(addr_block)  # update from default hosts

    blackout.get_network_devices()

    blackout.detect_devices()
    blackout.null_route_devices()
