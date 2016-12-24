#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

class VirtualOrganisation(object):
    """
    Wrapper base class for a Virtual Organisation.
    """

    def __init__(self, jvo):
        """
        @param [in] jvo JSON object representaing a VO.
        """

        ## The VO name.
        self.__name = jvo.keys()[0]

        vo_details = jvo.values()[0]

        ## The Operations Portal ID card URL.
        self.__ops_portal_url = vo_details['egi_ops']

        ## The VOMS server URL.
        self.__voms_server_url = vo_details['voms_server']

    def __lt__(self, other):
        return self.get_name() < other.get_name()
    def get_name(self):
        return self.__name
    def get_full_name(self):
        return self.__full_name
    def get_ops_portal_url(self):
        return self.__ops_portal_url
    def get_voms_server_url(self):
        return self.__voms_server_url
