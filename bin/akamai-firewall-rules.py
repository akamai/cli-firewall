"""
Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

"""
This code leverages akamai OPEN API. to control Certificates deployed in Akamai Network.
In case you need quick explanation contact the initiators.
Initiators: vbhat@akamai.com, aetsai@akamai.com, mkilmer@akamai.com
"""

import json
from firewallruleswrapper import fireShield
import argparse
import requests
import os
import logging
import sys
from prettytable import PrettyTable
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import datetime


PACKAGE_VERSION = "0.1.0"

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')
log_file = os.path.join('logs', 'akamai-firewall-rules.log')

# Set the format of logging in console and file separately
log_formatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
console_formatter = logging.Formatter("%(message)s")
root_logger = logging.getLogger()

logfile_handler = logging.FileHandler(log_file, mode='w')
logfile_handler.setFormatter(log_formatter)
root_logger.addHandler(logfile_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)
# Set Log Level to DEBUG, INFO, WARNING, ERROR, CRITICAL
root_logger.setLevel(logging.INFO)


def init_config(edgerc_file, section):
    if not edgerc_file:
        if not os.getenv("AKAMAI_EDGERC"):
            edgerc_file = os.path.join(os.path.expanduser("~"), '.edgerc')
        else:
            edgerc_file = os.getenv("AKAMAI_EDGERC")

    if not os.access(edgerc_file, os.R_OK):
        root_logger.error("Unable to read edgerc file \"%s\"" % edgerc_file)
        exit(1)

    if not section:
        if not os.getenv("AKAMAI_EDGERC_SECTION"):
            section = "firewall"
        else:
            section = os.getenv("AKAMAI_EDGERC_SECTION")

    try:
        edgerc = EdgeRc(edgerc_file)
        base_url = edgerc.get(section, 'host')

        session = requests.Session()
        session.auth = EdgeGridAuth.from_edgerc(edgerc, section)

        return base_url, session
    except configparser.NoSectionError:
        root_logger.error("Edgerc section \"%s\" not found" % section)
        exit(1)
    except Exception:
        root_logger.info(
            "Unknown error occurred trying to read edgerc file (%s)" %
            edgerc_file)
        exit(1)


def cli():
    prog = get_prog_name()
    if len(sys.argv) == 1:
        prog += " [command]"

    parser = argparse.ArgumentParser(
        description='Akamai CLI for Site Shield and Firewall Rules Notifications',
        add_help=False,
        prog=prog)
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' +
                PACKAGE_VERSION)

    subparsers = parser.add_subparsers(
        title='Commands', dest="command", metavar="")

    actions = {}

    subparsers.add_parser(
        name="help",
        help="Show available help",
        add_help=False).add_argument(
        'args',
        metavar="",
        nargs=argparse.REMAINDER)

    actions["list_services"] = create_sub_command(
        subparsers, "list-services", "List all firewall rules services available",
        None,
        None)

    actions["list_subscriptions"] = create_sub_command(
        subparsers, "list-subscriptions", "List current subscriptions",
        None,
        None)

    actions["subscribe"] = create_sub_command(
        subparsers, "subscribe",
        "Subscribe to a firewall rules service",
        [{"name": "service-name", "help": "Name of the service to be subscribed to within SINGLE quotes"},
         {"name": "service-id", "help": "ID of the service to be subscribed to"}],
        [{"name": "email", "help": "Email Id of the subscriber"}])

    actions["unsubscribe"] = create_sub_command(
        subparsers, "unsubscribe",
        "Unsubscribe from a firewall rules service",
        [{"name": "service-name", "help": "Name of the service to be subscribed to within SINGLE quotes"},
         {"name": "service-id", "help": "ID of the service to be subscribed to"}],
        [{"name": "email", "help": "Email Id of the subscriber"}])

    actions["list_cidrs"] = create_sub_command(
        subparsers, "list-cidrs",
        "List the CIDRs for current subscription or a specific firewall rules service",
        [{"name": "service-name", "help": "Name of the service within SINGLE quotes"},
         {"name": "service-id", "help": "Id of the service"},
         {"name": "file", "help": "Name of the file to ouput CIDR blocks"}],
        None)

    actions["ss_list_maps"] = create_sub_command(
        subparsers, "ss-list-maps",
        "List the available Site Shield maps",
        None,
        None)

    actions["ss_list_cidrs"] = create_sub_command(
        subparsers, "ss-list-cidrs",
        "List the CIDRs for a specific Site Shield map ",
        [{"name": "map-name", "help": "Name of the map within SINGLE quotes"},
         {"name": "map-id", "help": "ID of the map"},
         {"name": "file", "help": "Name of the file to ouput CIDR blocks"}],
        None)

    actions["ss_ack_change"] = create_sub_command(
        subparsers, "ss-ack-change",
        "Acknowledge a pending Site Shield map update ",
        [{"name": "map-name", "help": "Name of the map within SINGLE quotes"},
         {"name": "map-id", "help": "ID of the map"}],
        None)

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        return 0

    if args.command == "help":
        if len(args.args) > 0:
            if actions[args.args[0]]:
                actions[args.args[0]].print_help()
        else:
            parser.prog = get_prog_name() + " help [command]"
            parser.print_help()
        return 0

    # Override log level if user wants to run in debug mode
    # Set Log Level to DEBUG, INFO, WARNING, ERROR, CRITICAL
    if args.debug:
        root_logger.setLevel(logging.DEBUG)

    return getattr(sys.modules[__name__], args.command.replace("-", "_"))(args)


def create_sub_command(
        subparsers,
        name,
        help,
        optional_arguments=None,
        required_arguments=None):
    action = subparsers.add_parser(name=name, help=help, add_help=False)

    if required_arguments:
        required = action.add_argument_group("required arguments")
        for arg in required_arguments:
            name = arg["name"]
            del arg["name"]
            required.add_argument("--" + name,
                                  required=True,
                                  **arg,
                                  )

    optional = action.add_argument_group("optional arguments")
    if optional_arguments:
        for arg in optional_arguments:
            name = arg["name"]
            del arg["name"]
            if name == 'force':
                optional.add_argument(
                    "--" + name,
                    required=False,
                    **arg,
                    action="store_true")
            else:
                optional.add_argument("--" + name,
                                      required=False,
                                      **arg,
                                      )

    optional.add_argument(
        "--edgerc",
        help="Location of the credentials file [$AKAMAI_EDGERC]",
        default=os.path.join(
            os.path.expanduser("~"),
            '.edgerc'))

    optional.add_argument(
        "--section",
        help="Section of the credentials file [$AKAMAI_EDGERC_SECTION]",
        default="firewall")

    optional.add_argument(
        "--debug",
        help="DEBUG mode to generate additional logs for troubleshooting",
        action="store_true")

    return action


def list_services(args):
    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    list_services_response = fire_shield_object.list_services(session)
    if list_services_response.status_code == 200:
        #root_logger.info(json.dumps(list_services_response.json(), indent=4))
        table = PrettyTable(
            ['Service ID', 'Service Name', 'Service Description'])
        table.align = "l"

        for eachItem in list_services_response.json():
            rowData = []
            serviceId = eachItem['serviceId']
            serviceName = eachItem['serviceName']
            description = eachItem['description']
            rowData.append(serviceId)
            rowData.append(serviceName)
            rowData.append(description)
            table.add_row(rowData)
        root_logger.info(table)
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(list_services_response.json(), indent=4))


def list_subscriptions(args):
    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    list_subscriptions_response = fire_shield_object.list_subscriptions(session)
    #root_logger.info(json.dumps(list_subscriptions_response.json(), indent=4))
    if list_subscriptions_response.status_code == 200:
        if len(list_subscriptions_response.json()['subscriptions']) == 0:
            root_logger.info('No subscriptions found.')
            exit(-1)

        #root_logger.info(json.dumps(list_services_response.json(), indent=4))
        table = PrettyTable(
            ['Sign-up-Date', 'Email', 'Service ID', 'Service Name', 'Service Description'])
        table.align = "l"

        for eachItem in list_subscriptions_response.json()['subscriptions']:
            rowData = []
            rowData.append(eachItem['signupDate'])
            rowData.append(eachItem['email'])
            rowData.append(eachItem['serviceId'])
            rowData.append(eachItem['serviceName'])
            rowData.append(eachItem['description'])
            table.add_row(rowData)
        root_logger.info(table)
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(list_services_response.json(), indent=4))


def subscribe(args):
    if args.service_id and args.service_name:
        root_logger.info(
            'You cannot specify both --service-id and --service-name. Please choose one.')
        exit(-1)
    if not args.service_id and not args.service_name:
        root_logger.info('Specify either of --service-id or --service-name.')
        exit(-1)

    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    root_logger.info('Validating service name...')

    validService = False
    list_services_response = fire_shield_object.list_services(session)
    if list_services_response.status_code == 200:
        for eachItem in list_services_response.json():
            if args.service_id:
                if int(args.service_id) == int(eachItem['serviceId']):
                    validService = True
                    serviceId = args.service_id
                    break
            if args.service_name:
                if args.service_name == eachItem['serviceName']:
                    validService = True
                    serviceId = eachItem['serviceId']
                    break
    else:
        root_logger.info(
            'There was error in fetching services response. Use --debug for more information.')
        root_logger.debug(json.dumps(list_services_response.json(), indent=4))

    if validService is False:
        root_logger.info(
            'Invalid service name... You can run list-services to see available service names.\n')
        exit(-1)
    else:
        root_logger.info('Updating current subscription...\n')
        list_subscriptions_response = fire_shield_object.list_subscriptions(
            session)
        if list_subscriptions_response.status_code == 200:
            # Proceed to update the subscriptions
            newSubscription = {}
            newSubscription['email'] = args.email
            newSubscription['serviceId'] = int(serviceId)
            subscriptionData = list_subscriptions_response.json()
            subscriptionData['subscriptions'].append(newSubscription)
            #root_logger.info(json.dumps(subscriptionData, indent=4))
            update_subscriptionsRespose = fire_shield_object.update_subscriptions(
                session, json.dumps(subscriptionData))
            if update_subscriptionsRespose.status_code == 200:
                root_logger.info('Subscription updated successfully!\n')
            else:
                root_logger.info(
                    json.dumps(
                        update_subscriptionsRespose.json(),
                        indent=4))
        else:
            root_logger.info(
                'There was error in fetching subscription response. Use --debug for more information.')
            root_logger.debug(
                json.dumps(
                    list_services_response.json(),
                    indent=4))


def unsubscribe(args):
    if args.service_id and args.service_name:
        root_logger.info(
            'You cannot specify both --service-id and --service-name. Please choose one.')
        exit(-1)
    if not args.service_id and not args.service_name:
        root_logger.info('Specify either of --service-id or --service-name.')
        exit(-1)

    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    root_logger.info('Validating service name...')

    list_subscriptions_response = fire_shield_object.list_subscriptions(session)
    validService = False
    if list_subscriptions_response.status_code == 200:
        subscriptionData = list_subscriptions_response.json()
        # Using Index to iterate and delete the item from list
        index = 0
        for everySubscription in subscriptionData['subscriptions']:
            if args.service_id:
                if int(args.service_id) == int(everySubscription['serviceId']):
                    if args.email == everySubscription['email']:
                        validService = True
                        serviceName = everySubscription['serviceName']
                        del subscriptionData['subscriptions'][index]
                        break
            if args.service_name:
                if args.service_name == everySubscription['serviceName']:
                    if args.email == everySubscription['email']:
                        validService = True
                        serviceName = everySubscription['serviceName']
                        del subscriptionData['subscriptions'][index]
                        break
            index += 1

        #root_logger.info(json.dumps(subscriptionData, indent=4))
        if validService is True:
            #root_logger.info('Updating the subscription by unsubscribing to: ' + serviceName)
            update_subscriptionsRespose = fire_shield_object.update_subscriptions(
                session, json.dumps(subscriptionData))
            if update_subscriptionsRespose.status_code == 200:
                root_logger.info('Subscription unsubscribed successfully!\n')
            else:
                root_logger.info(
                    json.dumps(
                        update_subscriptionsRespose.json(),
                        indent=4))
        else:
            root_logger.info(
                'Service name/id AND/OR email does not exist in current subscription...\n')
            exit(-1)
    else:
        root_logger.info(
            'There was error in fetching subscription response. Use --debug for more information.')
        root_logger.debug(json.dumps(list_services_response.json(), indent=4))


def list_cidrs(args):
    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    root_logger.info('Fetching CIDR blocks...')
    list_cidrResponse = fire_shield_object.list_cidr(session)
    #root_logger.info(json.dumps(list_cidrResponse.json(), indent=4))
    if list_cidrResponse.status_code == 200:
        #root_logger.info(json.dumps(list_services_response.json(), indent=4))
        table = PrettyTable(
            ['Service Name', 'CIDR Block', 'Port', 'Activation Date'])
        table.align = "l"

        if len(list_cidrResponse.json()) == 0:
            root_logger.info('No subscriptions exist...')
            exit(-1)

        if args.file:
            root_logger.info(
                '\nWrting the CIDR block information to file ' +
                args.file +
                '\n')
            if os.path.exists(args.file):
                os.remove(args.file)

        for eachItem in list_cidrResponse.json():
            rowData = []
            if args.service_name:
                if args.service_name == eachItem['serviceName']:
                    if not args.file:
                        rowData.append(eachItem['serviceName'])
                        rowData.append(
                            str(eachItem['cidr']) + str(eachItem['cidrMask']))
                        rowData.append(eachItem['port'])
                        rowData.append(eachItem['effectiveDate'])
                        table.add_row(rowData)
                    else:
                        with open(args.file, 'a') as fileHandler:
                            fileHandler.write(
                                str(eachItem['cidr']) + str(eachItem['cidrMask']) + '\n')
            elif args.service_id:
                if str(args.service_id) == str(eachItem['serviceId']):
                    if not args.file:
                        rowData.append(eachItem['serviceName'])
                        rowData.append(
                            str(eachItem['cidr']) + str(eachItem['cidrMask']))
                        rowData.append(eachItem['port'])
                        rowData.append(eachItem['effectiveDate'])
                        table.add_row(rowData)
                    else:
                        with open(args.file, 'a') as fileHandler:
                            fileHandler.write(
                                str(eachItem['cidr']) + str(eachItem['cidrMask']) + '\n')
            else:
                if not args.file:
                    rowData.append(eachItem['serviceName'])
                    rowData.append(
                        str(eachItem['cidr']) + str(eachItem['cidrMask']))
                    rowData.append(eachItem['port'])
                    rowData.append(eachItem['effectiveDate'])
                    table.add_row(rowData)
                else:
                    with open(args.file, 'a') as fileHandler:
                        fileHandler.write(
                            str(eachItem['cidr']) + str(eachItem['cidrMask']) + '\n')
        if not args.file:
            root_logger.info(table)
        else:
            pass
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(list_cidrResponse.json(), indent=4))


def ss_list_maps(args):
    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    root_logger.info('Fetching Site Shield Maps...')

    list_maps_response = fire_shield_object.list_maps(session)

    if list_maps_response.status_code == 200:
        #root_logger.info(json.dumps(list_maps_response.json(), indent=4))
        table = PrettyTable(['Map ID',
                             'Map Name',
                             'Status',
                             'Last Acknowledged By',
                             'Acknowledge Date',
                             'Contact Info'])
        table.align = "l"

        if len(list_maps_response.json()['siteShieldMaps']) == 0:
            root_logger.info('No Site Shield maps found...')
            exit(-1)
        for eachItem in list_maps_response.json()['siteShieldMaps']:
            rowData = []
            if eachItem['acknowledged'] is False:
                status = 'UPDATES PENDING'
            else:
                status = 'Up-To-Date'

            mapId = eachItem['id']
            ruleName = eachItem['ruleName']
            acknowledgedBy = eachItem['acknowledgedBy']
            acknowledgedOn = eachItem['acknowledgedOn']
            acknowledgedOn = '{0:%Y-%m-%d %H:%M:%S}'.format(
                datetime.datetime.fromtimestamp(acknowledgedOn / 1000))
            contacts = ''
            for eachContact in eachItem['contacts']:
                contacts = eachContact + ' ' + contacts
            rowData.append(mapId)
            rowData.append(ruleName)
            rowData.append(status)
            rowData.append(acknowledgedBy)
            rowData.append(acknowledgedOn)
            rowData.append(contacts)

            table.add_row(rowData)
        root_logger.info(table)
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(list_services_response.json(), indent=4))


def ss_list_cidrs(args):
    if args.map_id and args.map_name:
        root_logger.info(
            'You cannot specify both --map-id and --map-name. Please choose one.')
        exit(-1)
    if not args.map_id and not args.map_name:
        root_logger.info('Specify either of --map-id or --map-name.')
        exit(-1)
    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    root_logger.info('Fetching Site Shield CIDR blocks...\n')

    if args.file:
        root_logger.info(
            '\nWrting the CIDR block information to file ' +
            args.file +
            '\n')
        if os.path.exists(args.file):
            os.remove(args.file)

    list_maps_response = fire_shield_object.list_maps(session)

    if list_maps_response.status_code == 200:
        #root_logger.info(json.dumps(list_maps_response.json(), indent=4))
        mapFound = False
        for eachItem in list_maps_response.json()['siteShieldMaps']:
            if args.map_name:
                if eachItem['ruleName'] == args.map_name:
                    #root_logger.info('Current CIDR blocks are: ')
                    for eachAddress in eachItem['currentCidrs']:
                        if not args.file:
                            root_logger.info(eachAddress)
                        else:
                            with open(args.file, 'a') as fileHandler:
                                fileHandler.write(str(eachAddress) + '\n')
                    mapFound = True
            elif args.map_id:
                if str(eachItem['id']) == str(args.map_id):
                    #root_logger.info('Current CIDR blocks are: ')
                    for eachAddress in eachItem['currentCidrs']:
                        if not args.file:
                            root_logger.info(eachAddress)
                        else:
                            with open(args.file, 'a') as fileHandler:
                                fileHandler.write(str(eachAddress) + '\n')
                    mapFound = True

        if mapFound is False:
            root_logger.info(
                'Unable to find the map. Please check the --map-name or --map-id')
            exit(-1)

    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.debug(json.dumps(list_maps_response.json(), indent=4))


def ss_ack_change(args):
    if args.map_id and args.map_name:
        root_logger.info(
            'You cannot specify both --map-id and --map-name. Please choose one.')
        exit(-1)
    if not args.map_id and not args.map_name:
        root_logger.info('Specify either of --map-id or --map-name.')
        exit(-1)
    base_url, session = init_config(args.edgerc, args.section)
    fire_shield_object = fireShield(base_url)
    root_logger.info('Fetching Site Shield maps...\n')

    list_maps_response = fire_shield_object.list_maps(session)

    if list_maps_response.status_code == 200:
        #root_logger.info(json.dumps(list_maps_response.json(), indent=4))
        mapFound = False
        for eachItem in list_maps_response.json()['siteShieldMaps']:
            if args.map_name:
                if eachItem['ruleName'] == args.map_name:
                    mapFound = True
                    mapId = eachItem['id']
            elif args.map_id:
                if str(eachItem['id']) == str(args.map_id):
                    mapFound = True
                    mapId = eachItem['id']

        if mapFound is False:
            root_logger.info(
                'Unable to find the map. Please check the --map-name or --map-id')
            exit(-1)
        else:
            #Check whether there is some update to ack
            update_pending = 0
            list_maps_response = fire_shield_object.list_maps(session)

            if list_maps_response.status_code == 200:
                if len(list_maps_response.json()['siteShieldMaps']) == 0:
                    root_logger.info('No Site Shield maps found...')
                    exit(-1)
                for eachItem in list_maps_response.json()['siteShieldMaps']:
                    if eachItem['acknowledged'] is False:
                        status = 'UPDATES PENDING'
                        update_pending = 1
                    else:
                        status = 'Up-To-Date'
                        update_pending = 0
            else:
                root_logger.info(
                    'There was error in fetching list_maps_response. Use --debug for more information.')
                root_logger.debug(json.dumps(list_services_response.json(), indent=4))

            if update_pending == 1:
                root_logger.info('Acknowledging Site Shield map...\n')
                acknowledge_mapResponse = fire_shield_object.acknowledge_map(
                    session, mapId)
                if acknowledge_mapResponse.status_code == 200:
                    root_logger.info('Successfully acknowledged!')
                else:
                    root_logger.info('Unknown error: Acknowledgement unsuccessful')
                    root_logger.info(
                        json.dumps(
                            acknowledge_mapResponse.json(),
                            indent=4))
                    exit(-1)
            else:
                #There was nothing to Acknowledge
                root_logger.info('There is no update to be acknowledged.')
    else:
        root_logger.info(
            'There was error in fetching response. Use --debug for more information.')
        root_logger.info(json.dumps(list_maps_response.json(), indent=4))


def get_prog_name():
    prog = os.path.basename(sys.argv[0])
    if os.getenv("AKAMAI_CLI"):
        prog = "akamai firewall"
    return prog


def get_cache_dir():
    if os.getenv("AKAMAI_CLI_CACHE_DIR"):
        return os.getenv("AKAMAI_CLI_CACHE_DIR")

    return os.curdir


# Final or common Successful exit
if __name__ == '__main__':
    try:
        status = cli()
        exit(status)
    except KeyboardInterrupt:
        exit(1)
