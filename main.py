import netmiko
import click
import re


def get_tunnels(ssh: netmiko.BaseConnection) -> list:
    """show tunnels and parse for names"""
    data = ssh.send_command('show router mpls lsp')
    return re.findall(r'(.*?) +\d+\.', data)


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
    commands = [f'tools perform router mpls resignal lsp "{i}" path "loose"' for i in tunnels]
    for command in commands:
        print(ssh.send_command(command, strip_prompt=False, strip_command=False))
    print(f'Done!')
    ssh.disconnect()


if __name__ == '__main__':
    main()
