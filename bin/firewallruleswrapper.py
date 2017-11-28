""" Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.
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

import json


class fireShield(object):
    def __init__(self, access_hostname):
        self.access_hostname = access_hostname


    def listMaps(self, session):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        listMapsRespose : listMapsRespose
            (listMapsRespose) Object with all details
        """

        listMapsUrl = 'https://' + self.access_hostname + \
            '/siteshield/v1/maps'
        listMapsResponse = session.get(
            listMapsUrl)
        return listMapsResponse

    def getMap(self, session, mapId):
        """
        Function to Get an Enrollment

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        getMapRespose : getMapRespose
            (getMapRespose) Object with all details
        """

        getMapUrl = 'https://' + self.access_hostname + \
            '/siteshield/v1/maps/' + str(mapId)
        getMapResponse = session.get(getMapUrl)
        return getMapResponse

    def acknowledgeMap(self, session, mapId):
        """
        Function to Create an Enrollment

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        acknowledgeMapRespose : acknowledgeMapRespose
            (acknowledgeMapRespose) Object with all details
        """

        acknowledgeMapUrl = 'https://' + self.access_hostname + \
            '/siteshield/v1/maps/' + str(mapId) + '/acknowledge'
        acknowledgeMapResponse = session.post(
            acknowledgeMapUrl)
        return acknowledgeMapResponse

    def listServices(self, session):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        listServicesRespose : listServicesRespose
            (listServicesRespose) Object with all details
        """

        listServicesUrl = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/services'
        listServicesResponse = session.get(
            listServicesUrl)
        return listServicesResponse

    def getService(self, session, serviceId):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        getServiceRespose : getServiceRespose
            (getServiceRespose) Object with all details
        """

        getServiceUrl = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/services/' + str(serviceId)
        getServiceResponse = session.get(
            getServiceUrl)
        return getServiceResponse

    def listCidr(self, session):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        listCidrRespose : listCidrRespose
            (listCidrRespose) Object with all details
        """

        listCidrUrl = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/cidr-blocks'
        listCidrResponse = session.get(
            listCidrUrl)
        return listCidrResponse

    def listSubscriptions(self, session):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        listSubscriptionsRespose : listSubscriptionsRespose
            (listSubscriptionsRespose) Object with all details
        """

        listSubscriptionsUrl = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/subscriptions'
        listSubscriptionsResponse = session.get(
            listSubscriptionsUrl)
        return listSubscriptionsResponse

    def updateSubscriptions(self, session, subscriptionData):
        """
        Function to Create an Enrollment

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        updateSubscriptionsRespose : updateSubscriptionsRespose
            (updateSubscriptionsRespose) Object with all details
        """

        updateSubscriptionsUrl = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/subscriptions'
        updateSubscriptionsResponse = session.put(
            updateSubscriptionsUrl, data=subscriptionData)
        return updateSubscriptionsResponse
