"""Command-line interface."""
import base64
import fileinput
import hashlib
import hmac
import logging
import os
import random
# from win32com.client import Dispatch
import subprocess
import time
import json
from configparser import ConfigParser
import xml.etree.ElementTree as ET
from collections import defaultdict

import arrow
import click
import psutil
import regobj
import requests
from requests.auth import AuthBase

host = ''
base_url = ''
mac_id = ''
mac_token = ''
state = 'InitialMonitoring'

logging.basicConfig(filename='agcoinstall.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


class MACAuth(AuthBase):
    """
    Attaches HTTP Authentication to the given Request object, and formats the header for every API call used
    """

    def __init__(self, mac_id, mac_token, host):
        # setup any auth-related data here
        self.mac_id = mac_id
        self.mac_token = mac_token
        self.host = host

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = self.generate_header(r.method, r.path_url)
        return r

    def get_hmac(self, method, uri, milliseconds, nonce):
        http_version = 'HTTP/1.1'
        # host = HOST
        request_string = f'{method} {uri} {http_version}\n{self.host}\n{milliseconds}\n{nonce}\n'
        return base64.b64encode(
            hmac.new(self.mac_token.lower().encode(), request_string.encode(), hashlib.sha256).digest()).decode()

    def generate_header(self, method, uri):
        milliseconds = str(int(time.time() * 1000))
        nonce = ''.join([str(random.randint(0, 9)) for i in range(8)])
        formatted_hmac = self.get_hmac(method, uri, milliseconds, nonce)
        return f'MAC kid={self.mac_id},ts={milliseconds},nonce={nonce},mac=\"{formatted_hmac}\"'


def download_auc_client(url):
    url = 'https://dl.agco-ats.com/AUC_EDT.exe'
    save_path = os.path.expanduser('~\\Desktop\\AUC_DL.exe')
    try:
        r = requests.get(url, allow_redirects=True)
        try:
            open(save_path, 'wb').write(r.content)
        except:
            print('Unable to download the AUC client')
    except:
        print('The link to download the latest AUC is down')


def run_auc_client():
    execute_command(os.path.expanduser('~\\Desktop\\AUC_DL.exe /S'))


def active_packages():
    parser = ConfigParser()
    parser.read(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')
    active_packages_string = parser.get('Status', 'ActivePackages')
    logging.info(f'Number of active packages in AUC: {active_packages_string}')
    return int(active_packages_string)


def pause_downloads_set():
    parser = ConfigParser()
    parser.read(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')
    download_schedule_value = parser.get('Settings', 'DownloadSchedule')
    logging.info(f'DownloadSchedule: {download_schedule_value}')
    return 'toggle' in download_schedule_value


def ready_to_install():
    parser = ConfigParser()
    parser.read(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')
    return parser.get('Status', 'ReadyToInstall')


def config_ini_find_and_replace(find_text, replace_text):
    logging.info(f'Attempting to replace \"{find_text}\" with \"{replace_text}\" in the config.ini file')
    kill_process_by_name('AGCOUpdateService')
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            print(line.replace(find_text, replace_text), end='')
    set_service_running('AGCO Update')
    start_auc()
    time.sleep(10)


def config_ini_set_environment(env_base_url):
    # other_urls = set(remaining_urls.values())
    # logging.info(f'Attempting to replace \"{find_text}\" with \"{replace_text}\" in the config.ini file')
    # kill_process_by_name('AGCOUpdateService')
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\test.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            if "UpdateHost" in line:
                line = f'UpdateHost=https://{env_base_url}/api/v2\n'
            print(line, end='')
    # set_service_running('AGCO Update')
    # start_auc()
    # time.sleep(10)


def set_config_ini_to_original():
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            print(line.replace('IsExplicitInstallRunning=True', 'IsExplicitInstallRunning=False'), end='')


def set_config_ini_to_install():
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            print(line.replace('IsExplicitInstallRunning=False', 'IsExplicitInstallRunning=True'), end='')


# TODO change this method to use the command line method of schedule change
def clear_auc_download_schedule():
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            print(line.replace('DownloadSchedule=Start: On  Toggle: 06:00, 17:00', 'DownloadSchedule=Start: On'),
                  end='')


def execute_command(path_and_command):
    """
    Runs an inputted command. If the command returns a non-zero return code it will fail. This method is not for
    capturing the output
    """
    logging.debug(f'Attempting to execute: {path_and_command}')
    p1 = subprocess.run(path_and_command,
                        shell=True,
                        check=True,
                        capture_output=True,
                        text=True,
                        )
    logging.debug(f'Command: {path_and_command}')
    logging.debug(f'ReturnCode: {str(p1.returncode)}')


def kill_process_by_name(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        current_proc_name = proc.info['name']
        if process_name in current_proc_name:
            logging.info(f'Killing process: {current_proc_name}')
            try:
                proc.kill()
                logging.debug(f'Killed process: {current_proc_name}')
            except:
                logging.debug(f'Unable to kill process: {current_proc_name}')


def start_auc():
    logging.debug('Attempting to start AUC')
    # execute_command(r'start \MIN C:\Program Files (x86)\AGCO Corporation\AGCO Update Client\AGCOUpdateService.exe')
    os.startfile(r'C:\Program Files (x86)\AGCO Corporation\AGCO Update Client\AGCOUpdateService.exe')


def apply_certs():
    subprocess.call(
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe certutil -addstore TrustedPublisher "
        r"C:\Users\fraserda\dev\agcoinstall\data\SontheimCertificate1.cer", shell=True)
    subprocess.call(
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe certutil -addstore TrustedPublisher "
        r"C:\Users\fraserda\dev\agcoinstall\data\SontheimCertificate2.cer", shell=True)


def set_service_running(service):
    """
    Sets a windows service's start-up type to runnig
    :param service: string name of windows service
    """
    logging.debug(f'Attempting to set the following service to running: {service}')

    p1 = subprocess.run(fr'net start "{service}"',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=True,
                        )

    with open(r'C:\Vagrant\temp_output.txt', 'w') as f:
        f.write(p1.stdout)
    with open(r'C:\Vagrant\temp_output.txt', 'r') as f:
        for line in f.readlines():
            if f"The {service} service was started successfully." in line:
                logging.debug(f"{service} has started")


def set_host_environment(env_base_url):
    files = [r'C:\Program Files (x86)\AGCO Corporation\EDT\EDTUpdateService.exe.config',
             r'C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe.config']
    for file in files:
        mytree = ET.parse(file)
        myroot = mytree.getroot()
        for child in myroot.iter('value'):
            if 'https' in child.text:
                child.text = fr'https://{env_base_url}/api/v2'
        mytree.write(file)


def apply_voucher():
    voucher = create_voucher()
    execute_command(rf'C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe APPLYVoucher {voucher} NA0001 30096')


def file_watcher():
    moddate = os.stat(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')[8]
    print(f'Start: {moddate}')
    while True:
        current_moddate = os.stat(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')[8]
        if current_moddate == moddate:
            time.sleep(5)
        else:
            print("Change detected...testing for state")
            moddate = current_moddate
            current_state = get_state()
            if current_state == 'EDTDownloadsPaused':
                config_ini_find_and_replace('DownloadSchedule=Start: On  Toggle: 06:00, 18:00',
                                            'DownloadSchedule=Start: On')
                get_state()
            if current_state == 'EDTReadyToInstall':
                config_ini_find_and_replace('IsExplicitInstallRunning=False', 'IsExplicitInstallRunning=True')
                get_state()
            if current_state == 'NeedsVoucher':  ##TODO this will vary depending on environment
                apply_voucher()
                get_state()


def set_config_init_to_install():
    # print(f'{datetime.datetime.now()}: Downloads have completed')
    kill_process_by_name('AGCOUpdateService')
    set_config_ini_to_install()
    set_service_running('AGCO Update')
    start_auc()
    time.sleep(10)


def set_config_init_to_install():
    # print(f'{datetime.datetime.now()}: Downloads have completed')
    kill_process_by_name('AGCOUpdateService')
    set_config_ini_to_original()
    set_service_running('AGCO Update')
    start_auc()
    time.sleep(10)


def get_client_id():
    try:
        return (
            regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation')
                .get_subkey(r'AGCO Update')['ClientID']
                .data
        )
    except AttributeError as e:
        click.secho("Client Id was not present in registry. Please confirm that you have AUC installed \n{e}", fg='red')


def voucher_in_registry():
    """
    gets and return the voucher in the registry
    @return: voucher code as text
    """
    try:
        voucher_id = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Voucher'].data
    except AttributeError as e:
        click.secho(f'Voucher ID was not present in registry. Please confirm that EDT has been vouchered {e}', fg='red')
        voucher_id = ''
    return voucher_id


def get_reg_client_id():
    try:
        client_id = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(r'AGCO Update')[
            'ClientID'].data
    except AttributeError as e:
        click.secho(
            f'Client ID was not present in registry. Please confirm that you have AGCO update client installed. {e}',
            fg='red')
    return client_id


def get_date_x_weeks_from_now(number_of_weeks=8):
    utc = arrow.utcnow()
    x_weeks_from_now = utc.shift(weeks=+number_of_weeks)
    return x_weeks_from_now.isoformat()


def create_voucher(duration=8):
    """Creates temporary voucher"""
    expire_date = get_date_x_weeks_from_now(duration)
    uri = f'{base_url}/api/v2/Vouchers'
    payload = {
        "Type": "Temporary",
        "DealerCode": "NA0001",
        "LicenseTo": "Darrin Fraser",
        "Purpose": "Testing",
        "Email": "darrin.fraser@agcocorp.com",
        "ExpirationDate": expire_date,
    }
    r = requests.post(f'{uri}', auth=MACAuth(mac_id, mac_token, host), data=payload)
    return r.text.strip('"')


def get_client_relationships(client_id):
    uri = f'{base_url}/api/v2/UpdateGroupClientRelationships'
    payload = {
        "limit": 100,
        "ClientID": client_id
    }
    r = requests.get(uri, auth=MACAuth(mac_id, mac_token, host), params=payload)
    returned_relationships = json.loads(r.text)
    ug_client_relationship_list = returned_relationships['Entities']
    return ug_client_relationship_list


def subscribe_or_update_client_relationships(ug_to_be_assigned, ug_client_relationships, remove_ug_dict, client_id):
    ugs_to_be_removed = set(remove_ug_dict.values())
    to_be_assigned_in_relationships = False
    for relationship in ug_client_relationships:
        if ug_to_be_assigned == relationship['UpdateGroupID']:
            to_be_assigned_in_relationships = True

        if relationship['UpdateGroupID'] in ugs_to_be_removed and relationship['Active']:
            relationship['Active'] = False
            relationship_id = relationship['RelationshipID']
            uri = f'{base_url}/api/v2/UpdateGroupClientRelationships/{relationship_id}'
            r = requests.put(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)

        if relationship['UpdateGroupID'] == ug_to_be_assigned and not relationship['Active']:
            relationship['Active'] = True
            relationship_id = relationship['RelationshipID']
            uri = f'{base_url}/api/v2/UpdateGroupClientRelationships/{relationship_id}'
            r = requests.put(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)
            to_be_assigned_in_relationships = True

    if not to_be_assigned_in_relationships:
        uri = f'{base_url}/api/v2/UpdateGroupClientRelationships'
        relationship = {'UpdateGroupID': ug_to_be_assigned,
                        'ClientID': client_id,
                        'Active': 'true',
                        }
        r = requests.post(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)


def get_state():
    global state
    install_ready = ready_to_install()
    number_of_packages = active_packages()

    if not install_ready and not number_of_packages and state == 'InitialMonitoring':
        return state

    elif (
            not install_ready
            and number_of_packages
            and state in ['InitialMonitoring', 'EDTDownloadsPaused']
    ):
        state = 'EDTDownloadsPaused' if pause_downloads_set() else 'EDTDownloading'
        return state

    elif install_ready and number_of_packages and state == 'EDTDownloading':
        state = 'EDTReadyToInstall'
        return state

    elif not install_ready and number_of_packages and state == 'EDTReadyToInstall':
        state = 'EDTInstalling'
        return state

    elif not install_ready and not number_of_packages and state in {'NeedsVoucher', 'EDTInstalling'}:
        state = 'Vouchered' if voucher_in_registry() else 'NeedsVoucher'
        return state

    elif not install_ready and number_of_packages and state == 'Vouchered':
        state = 'DownloadingMasters'
        return state

    elif install_ready and number_of_packages and state == 'DownloadingMasters':
        state = 'InstallingMasters'
        return state

    elif not install_ready and not number_of_packages and state == 'InstallingMasters':
        state = 'AllDownloadsComplete'
        return state

    else:
        print(f'get_state function failed to account for the following:\n'
              f'ReadyToInstall: {install_ready}\n'
              f'NumberOfActivePackages: {number_of_packages}\n'
              f'LastKnownState: {state}')


@click.command()
@click.version_option()
@click.option('--env', '-e', default='prod', type=click.Choice(['prod', 'test', 'dev']))
@click.option('--updategroup', '-ug', default='InternalTestPush', type=click.Choice(['EDTUpdates',
                                                                                     'Dev',
                                                                                     'RC',
                                                                                     'TestPush',
                                                                                     'InternalTestPush',
                                                                                     'InternalDev',
                                                                                     'InternalRC',
                                                                                     ]))
@click.option('--m_id', '-mi', prompt=True, default=lambda: os.environ.get('MAC_ID', ''), help="Supply MAC_ID")
@click.option('--m_token', '-mt', prompt=True, default=lambda: os.environ.get('MAC_TOKEN', ''), help="Supply MAC_TOKEN")
def main(env, updategroup, m_id, m_token) -> None:
    """Agcoinstall."""

    global host, base_url, mac_id, mac_token
    mac_id = m_id
    mac_token = m_token

    ug_dict = {'EDTUpdates': 'eb91c5e8-ffb1-4060-8b97-cb53dcd4858d',
               'Dev': '29527dd4-3828-40f1-91b4-dfa83774e0c5',
               'RC': '30ae5793-67a2-4111-a94a-876a274c3814',
               'InternalTestPush': 'd76d7786-1771-4d3b-89b1-c938061da4ca',
               'TestPush': '42dd2226-cdaa-46b4-8e23-aa98ec790139',
               'InternalDev': '6ed348f3-8e77-4051-a570-4d2a6d86995d',
               'InternalRC': "75a00edd-417b-459f-80d9-789f0c341131",
               }

    env_dict = {'dev': 'edtsystems-webtest-dev.azurewebsites.net',
                'prod': 'secure.agco-ats.com',
                'test': 'edtsystems-webtest.azurewebsites.net',
                }

    update_group_id = ug_dict.pop(updategroup)

    host = env_dict[env]
    base_url = f'https://{host}'
    apply_certs()
    # env_base_url = env_dict.pop(env)

    # current_state = get_state()
    # cid = get_client_id()
    # c_relationships = get_client_relationships(cid)
    # subscribe_or_update_client_relationships(update_group_id, c_relationships, ug_dict, cid)
    # set_host_environment(host)


if __name__ == "__main__":
    main(prog_name="agcoinstall")  # pragma: no cover
