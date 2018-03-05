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

    def list_maps(self, session):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        list_mapsRespose : list_mapsRespose
            (list_mapsRespose) Object with all details
        """

        list_maps_url = 'https://' + self.access_hostname + \
            '/siteshield/v1/maps'
        list_maps_response = session.get(
            list_maps_url)
        return list_maps_response

    def get_map(self, session, mapId):
        """
        Function to Get an Enrollment

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        get_mapRespose : get_mapRespose
            (get_mapRespose) Object with all details
        """

        get_map_url = 'https://' + self.access_hostname + \
            '/siteshield/v1/maps/' + str(mapId)
        get_map_response = session.get(get_map_url)
        return get_map_response

    def acknowledge_map(self, session, mapId):
        """
        Function to Create an Enrollment

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        acknowledge_mapRespose : acknowledge_mapRespose
            (acknowledge_mapRespose) Object with all details
        """

        acknowledge_map_url = 'https://' + self.access_hostname + \
            '/siteshield/v1/maps/' + str(mapId) + '/acknowledge'
        acknowledge_map_response = session.post(
            acknowledge_map_url)
        return acknowledge_map_response

    def list_services(self, session):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        list_servicesRespose : list_servicesRespose
            (list_servicesRespose) Object with all details
        """

        list_services_url = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/services'
        list_services_response = session.get(
            list_services_url)
        return list_services_response

    def get_service(self, session, serviceId):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        get_serviceRespose : get_serviceRespose
            (get_serviceRespose) Object with all details
        """

        get_service_url = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/services/' + str(serviceId)
        get_service_response = session.get(
            get_service_url)
        return get_service_response

    def list_cidr(self, session):
        """
        Function to List Enrollments

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        list_cidr_response : list_cidr_response
            (list_cidr_response) Object with all details
        """

        list_cidr_url = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/cidr-blocks'
        list_cidr_response = session.get(
            list_cidr_url)
        return list_cidr_response

    def list_subscriptions(self, session):
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

        listSubscriptions_url = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/subscriptions'
        listSubscriptions_response = session.get(
            listSubscriptions_url)
        return listSubscriptions_response

    def update_subscriptions(self, session, subscriptionData):
        """
        Function to Create an Enrollment

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        update_subscriptionsRespose : update_subscriptionsRespose
            (update_subscriptionsRespose) Object with all details
        """

        update_subscriptions_url = 'https://' + self.access_hostname + \
            '/firewall-rules-manager/v1/subscriptions'
        update_subscriptions_response = session.put(
            update_subscriptions_url, data=subscriptionData)
        return update_subscriptions_response

    def acknowledge_map(self, session, mapId):
        """
        Function to Create an Enrollment

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        acknowledge_mapRespose : acknowledge_mapRespose
            (acknowledge_mapRespose) Object with all details
        """

        acknowledge_map_url = 'https://' + self.access_hostname + \
            '/siteshield/v1/maps/' + str(mapId) + '/acknowledge'
        acknowledge_map_response = session.post(
            acknowledge_map_url)
        return acknowledge_map_response
