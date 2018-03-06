# cli-firewall
Provides a way to interact with firewall and siteshield related information via Open APIs and without manually having to go into the Luna Portal. Provides various functionality such as viewing firewall rules services, listing subscriptions, siteshield maps, CIDR blocks and acknowledge siteshield map updates.

## Local Install
* Python 3+
* pip install edgegrid-python

### Credentials
In order to use this module, you need to:
* Set up your credential files as described in the [authorization](https://developer.akamai.com/introduction/Prov_Creds.html) and [credentials](https://developer.akamai.com/introduction/Conf_Client.html) sections of the Get Started pagegetting started guide on developer.akamai.comthe developer portal.  
* When working through this process you need to give grants for the Certificate Provisionig System API.  The section in your configuration file should be called **firewall**.

## Functionality (version 0.1.0)
The initial version of the firewall provides the following functionality:
* List all Maps
* List all Subscriptions
* Subscribe to the firewall notification list
* Unsubscribe to the firewall notification list
* List the CIDR block 
* List the siteshield maps
* Acknowledge Siteshield map update

## akamai-firewall
Main program that wraps this functionality in a command line utility:
* [List all Maps](#list-services)
* [List all Subscriptions](#list-subscriptions)
* [Subscribe to the firewall notification list](#subscribe)
* [Unsubscribe to the firewall notification list](#unsubscribe)
* [List the CIDR block](#list-cidrs)
* [List the siteshield maps](#list-ss-maps)
* [Acknowledge Siteshield map update](#ack-ss-change)


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

### list-ss-maps
List sisteshield maps that you are mapped to.

```bash
%  akamai firewall list-ss-maps --cn demo.devops.com
```

The flags of interest for cancel are:

```
--cn <common name>  Common name to be used to cancel the certificate/enrollment information from CPS.

```
