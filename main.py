import netmiko
import click
import re


def get_tunnels(ssh: netmiko.BaseConnection, debug) -> list:
    """show tunnels and parse for names"""
    data = ssh.send_command('show router mpls lsp')
    if debug:
        print(data)
    return re.findall(r'(.*?) +\d+\.', data)


@click.command()
@click.option('-u', '--username', help='username for ssh')
@click.option('-d', '--device_ip', help='IP of device on which to resignal RSVP tunnels')
@click.option('-db', '--debug', is_flag=True, default=False, help='more prints during run')
def main(username, device_ip, debug):
    passwd = input('Enter password: ')
    dev_config = {
        'device_type': 'alcatel_sros',
        'host': device_ip,
        'username': username,
        'password': passwd
    }
    ssh = netmiko.ConnectHandler(**dev_config)
    tunnels = get_tunnels(ssh, debug)
    print(f'Found {len(tunnels)} tunnels, re-signaling...')
    commands = [f'tools perform router mpls resignal lsp "{i}" path "loose"' for i in tunnels]
    if debug:
        print (commands)
    for command in commands:
        cli_out = ssh.send_command(command, strip_prompt=False, strip_command=False)
        if debug:
            print(cli_out)
    print(f'Done!')
    ssh.disconnect()


if __name__ == '__main__':
    main()
