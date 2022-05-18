import netmiko
import click
import re


def get_tunnels(ssh: netmiko.BaseConnection) -> str:
    """show tunnels and parse for names"""
    # TODO show and parse, return list
    return ''


@click.command()
@click.option('-u', '--username', help='username for ssh')
@click.option('-d', '--device_ip', help='IP of device on which to resignal RSVP tunnels')
def main(username, device_ip):
    passwd = input('Enter password: ')
    dev_config = {
        'device_type': 'alcatel_sros',
        'host': device_ip,
        'username': username,
        'password': passwd
    }
    ssh = netmiko.ConnectHandler(**dev_config)
    tunnels = get_tunnels(ssh)
    print(f'Found {len(tunnels)} tunnels, re-signaling...')
    # TODO list comprehension for commands set
    commands = [f'{i}' for i in tunnels]
    for command in commands:
        ssh.send_command(command)
    print(f'Done!')
    ssh.disconnect()
