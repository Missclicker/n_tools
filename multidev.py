import click
from concurrent import futures
from main import resignal_tunnels


@click.command()
@click.option('-u', '--username', default='warrior', help='username for ssh')
@click.option('-db', '--debug', is_flag=True, default=False, help='more prints during run')
@click.argument('file_with_ips', nargs=1)
def main(file_with_ips: str, username: str, debug: bool) -> None:
    with open(file_with_ips) as f:
        devices = [i.strip().replace(',', '').replace(';', '') for i in f.readlines() if i]

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        passwd = input('Enter password: ').strip()
        threads = [executor.submit(
            resignal_tunnels,
            device_ip,
            username,
            debug,
            passwd
        ) for device_ip in devices]

        for task in futures.as_completed(threads):
            dev, tun_num = task.result()
            print(f'Resignaled {tun_num} tunnels on {dev}')


if __name__ == '__main__':
    main()
