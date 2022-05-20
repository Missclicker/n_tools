import netmiko
import click
import re
# from test_ssh_class import TestSSH
#
#
# def swap_netmiko_for_test(func):
#     global netmiko
#     netmiko = TestSSH
#     return func


class WrongIPValue(Exception):
    pass


def get_tunnels(ssh: netmiko.BaseConnection, debug: bool) -> list:
    """show tunnels and parse for names"""
    data = ssh.send_command('show router mpls lsp')
    if debug:
        print(data)
    return re.findall(r'(.*?) +\d+\.', data)


# @swap_netmiko_for_test
def resignal_tunnels(device_ip, username, debug, passwd) -> tuple:
    dev_config = {
        'device_type': 'alcatel_sros',
        'host': device_ip,
        'username': username,
        'password': passwd
    }
    ssh = netmiko.ConnectHandler(**dev_config)
    tunnels = get_tunnels(ssh, debug)
    print(f'Found {len(tunnels)} tunnels on {device_ip}, re-signaling...')
    commands = [f'tools perform router mpls resignal lsp "{i}" path "loose"' for i in tunnels]
    if debug:
        print(commands)
    for command in commands:
        cli_out = ssh.send_command(command, strip_prompt=False, strip_command=False)
        if debug:
            print(cli_out)
    print(f'Done!')
    ssh.disconnect()
    return device_ip, len(commands)


@click.command()
@click.option('-u', '--username', default='warrior', help='username for ssh')
@click.option('-db', '--debug', is_flag=True, default=False, help='more prints during run')
@click.argument('device_ips', nargs=-1)
def main(device_ips: str, username: str, debug: bool = False) -> None:
    """Function will resignal tunnels on provided devices

    Can provide multiple IPs separated with space or a single one"""
    for ip in device_ips:
        if not re.match(r'(\d+\.){3}\d+', ip):
            print(f'Not a valid IP provided - {ip}')
            raise WrongIPValue

    passwd = input('Enter password: ').strip()
    for ip in device_ips:
        resignal_tunnels(ip, username, debug, passwd)


if __name__ == '__main__':
    main()
