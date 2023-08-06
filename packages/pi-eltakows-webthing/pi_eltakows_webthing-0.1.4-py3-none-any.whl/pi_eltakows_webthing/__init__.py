import os
import logging
from string import Template
from pi_eltakows_webthing.app import App
from pi_eltakows_webthing.eltako_webthing import run_server


PACKAGENAME = 'pi_eltakows_webthing'
ENTRY_POINT = "eltakows"
DESCRIPTION = "A web connected Eltako windsensor measuring wind speed on Raspberry Pi"

UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --hostname $hostname --verbose $verbose --port $port --gpio $gpio
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')


class WsApp(App):

    def do_add_argument(self, parser):
        parser.add_argument('--gpio', metavar='gpio', required=False, type=int, help='the gpio number wired to the device')

    def do_additional_listen_example_params(self):
        return "--gpio 14"

    def do_process_command(self, command:str, hostname: str, port: int, verbose: bool, args) -> bool:
        if command == 'listen' and (args.gpio is not None):
            print("running " + self.packagename + " on " + hostname + "/" + str(port) + " (gpio " + str(args.gpio) + ")")
            run_server(args.hostname, port, int(args.gpio), self.description)
            return True
        elif args.command == 'register' and (args.gpio is not None):
            print("register " + self.packagename + " on " + hostname + "/" + str(port) + " (gpio " + str(args.gpio) + " and starting it)")
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename, entrypoint=self.entrypoint, hostname=hostname, port=port, verbose=verbose, gpio=args.gpio)
            self.unit.register(hostname, port, unit)
            return True
        else:
            return False


def main():
    WsApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()
