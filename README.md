# cli-firewall
Provides a way to interact with firewall rules and Site Shield related information via Open APIs. Functionality includes viewing firewall rules services, subscribing and unsubscribing to firewall rules services, viewing and acknowledging Site Shield maps, and listing CIDR blocks.

## Local Install
* Python 3+
* pip install edgegrid-python

### Credentials
In order to use this module, you need to:
* Set up your credential files as described in the [authorization](https://developer.akamai.com/introduction/Prov_Creds.html) and [credentials](https://developer.akamai.com/introduction/Conf_Client.html) sections of the Get Started pagegetting started guide on developer.akamai.comthe developer portal.  
* When working through this process you need to give grants for the Firewall Rules Manager and Siteshield API.  The section in your configuration file should be called 'firewall'.
```
[firewall]
client_secret = [CLIENT_SECRET]
host = [HOST]
access_token = [ACCESS_TOKEN_HERE]
client_token = [CLIENT_TOKEN_HERE]
```

## Functionality
This version includes the following functionality:
* List all firewall rules services available for subscription
* Subscribe and unsubscribe to firewall rules services
* List CIDRs for all current subscriptions or a specific firewall rules subscribed to
* List all available Site Shield maps
* List CIDRs for a specified Site Shield map
* Acknowledge a pending Site Shield map update

## akamai-firewall-rules
This is the main program that wraps this functionality in a command line utility:
* [list-services](#list-services)
* [list-subscriptions](#list-subscriptions)
* [subscribe](#subscribe)
* [unsubscribe](#unsubscribe)
* [list-cidrs](#list-cidrs)
* [ss-list-maps](#ss-list-maps)
* [ss-list-cidrs](#ss-list-cidrs)
* [ss-ack-change](#ss-ack-change)


### list-services
List available firewall rules services available for subscription. A service must be subscribed to before CIDRs can be displayed for that service.

```bash
%  akamai firewall list-services
```


### list-subscriptions
List current subscriptions.

```bash
%  akamai firewall list-subscriptions
```


### subscribe
Subscribe to a firewall rules service (email address is mandatory).

```bash
%  akamai firewall subscribe --service-id 1 --email email@example.com
%  akamai firewall subscribe --service-name FIRSTPOINT --email email@example.com
```

The flags of interest are (please specify either --service-name or --service-id):

```
--service-id <value>            ID of service to be subscribed for
--service-name <value>          Name of service to be subscribed for
--email <value>                 Email address to subscribe for service specified
```


### unsubscribe
Unsubscribe from a specific firewall rules service.

```bash
%  akamai firewall unsubscribe --service-id 1
%  akamai firewall unsubscribe --service-name FIRSTPOINT
```

The flags of interest are (please specify either --service-name or --service-id):

```
--service-id <value>            ID of service to be unsubscribed from
--service-name <value>          Name of service to be unsubscribed from
--email <value>                 Email address to unsubscribe for service specified
```


### list-cidrs
List the CIDR blocks for all current subscriptions or a specific firewall rules service subscription.

```bash
%  akamai firewall list-cidrs
%  akamai firewall list-cidrs --file
%  akamai firewall list-cidrs --service-name FIRSTPOINT
%  akamai firewall list-cidrs --service-id 20
%  akamai firewall list-cidrs --service-name 'Global Traffic Management - Siteshield' --file sample.txt
```

The flags of interest are:

```
--service-id <value>            ID of service to be unsubscribed from (optional)
--service-name <value>          Name of service to be unsubscribed from (optional)
--file <filename>               Filename to output CIDRs (optional)
```


### ss-list-maps
List available Site Shield maps.

```bash
%  akamai firewall ss-list-maps
```


### ss-list-cidrs
List the CIDRs for a specified Site Shield map

```bash
%  akamai firewall ss-list-cidrs --map-id 12345
%  akamai firewall ss-list-cidrs --map-name sample.akamaiedge.net
%  akamai firewall ss-list-cidrs --map-name sample.akamaiedge.net --file sample.txt
```

The flags of interest are (please specify either --map-id or --map-name):

```
--map-id <value>            	ID of desired Site Shield map
--map-name <value>          	Name of desired Site Shield map
--file <filename>               Filename to output CIDRs (optional)
```


### ss-ack-change
Acknowledge a pending Site Shield map update.

```bash
%  akamai firewall ss-ack-change --map-id 12345
%  akamai firewall ss-ack-change --map-name sample.akamaiedge.net
```

The flags of interest are (please specify either --map-id or --map-name):

```
--map-id <value>            	ID of desired Site Shield map
--map-name <value>          	Name of desired Site Shield map
```
