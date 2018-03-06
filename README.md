# cli-firewall
Provides a way to interact with firewall rules and Site Shield related information via Open APIs. Functionality includes viewing firewall rules services, subscribing and unsubscribing to firewall rules services, viewing and acknowledging Site Shield mps, and listing CIDR blocks.

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
List maps

```bash
%  akamai firewall list-services
```

### list-subscriptions
List all the available subscriptions.

```bash
%  akamai firewall list-subscriptions
```

### subscribe
Subscribe to a service.

```bash
%  akamai firewall subscribe --service-id 1 --email vbhat@akamai.com
%  akamai firewall subscribe --service-name FIRSTPOINT --email vbhat@akamai.com
```

The flags of interest for create are:

```
--service-id <value>            ID of service to be subscribed for.
--service-name <value>          Name of service to be subscribed for.

```

### unsubscribe
Unsubscribe to a service.

```bash
%  akamai firewall unsubscribe --service-id 1
%  akamai firewall unsubscribe --service-name FIRSTPOINT
```

The flags of interest for update are:

```
--service-id <value>            ID of service to be unsubscribed from.
--service-name <value>          Name of service to be unsubscribed from.
```

### list-cidrs
List the CIDR blocks.

```bash
%  akamai firewall list-cidrs
```

The flags of interest for download are:

```
--cn <common name>  Common name to be used to download the certificate/enrollment information from CPS.
--format <json/yml/yaml>        Data format to be used to save the downloaded certificate information.

```

### ss-list-maps
List sisteshield maps that you are mapped to.

```bash
%  akamai firewall list-ss-maps --cn demo.devops.com
```

The flags of interest for cancel are:

```
--cn <common name>  Common name to be used to cancel the certificate/enrollment information from CPS.

```

### ss-list-cidrs
List sisteshield maps that you are mapped to.

```bash
%  akamai firewall list-ss-maps --cn demo.devops.com
```

The flags of interest for cancel are:

```
--cn <common name>  Common name to be used to cancel the certificate/enrollment information from CPS.

```

### ss-ack-change
List sisteshield maps that you are mapped to.

```bash
%  akamai firewall list-ss-maps --cn demo.devops.com
```

The flags of interest for cancel are:

```
--cn <common name>  Common name to be used to cancel the certificate/enrollment information from CPS.

```
