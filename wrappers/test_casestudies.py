#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for handling JSONs.
import json

# The wrapper class we are testing.
from casestudies import CaseStudy

class CaseStudyTest(unittest.TestCase):

    def setUp(self):

        ## The case studies.
        self.__cs = {}

        # Get the case studies from the JSON file.
        with open("data/casestudies.json", "r") as jf:
            js = json.load(jf)

        # Add the case studies to the list.
        for cj in js:
            case_study = CaseStudy(cj)
            self.__cs[case_study.get_label()] = case_study
            lg.info(" * Adding case study '%s'." % (case_study.get_full_user_community_name()))

    def tearDown(self):
        pass

    def test_make_wordpress_page(self):

        ## The LSST case study object.
        c = self.__cs['lsst']

        # The tests.

        # Test the label name.
        self.assertEqual(c.get_label(), "lsst")

        # Test the full title.
        self.assertEqual(c.get_full_user_community_name(), "The Large Synoptic Survey Telescope")

        # TODO: Implement the rest of the tests.

        # TODO: Implement the HTML functionality for the GridPP website.
#        with open("html/lsst_overview.html", "r") as f:
#            ## The overview HTML.
#            overview_html_s = f.read()
#
#        is_overview_correct = overview_html_s == self.__cs['lsst'].get_wordpress_html_overview()
#
#        self.assertTrue(is_overview_correct)
#
#        # Test that the contents of the HTML output is the same as
#        # that on the GridPP WordPress website...
#        with open("html/lsst.html", "r") as original_html_file:
#
#            ## The original HTML as a string.
#            html_orig_s = original_html_file.read()
#
#        lg.debug("*")
#        lg.debug("* HTML original:\n%s" % (html_orig_s))
#        lg.debug("*")
#
#        ## Did the wrapper produce the HTML page correctly?
#        html_page_success = html_orig_s == self.__cs['lsst'].get_wordpress_page_html()
#
#        # Test it.
#        self.assertTrue(html_page_success)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_casestudies.log', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("=================================================")
    lg.info(" Logger output from wrappers/test_casestudies.py ")
    lg.info("=================================================")
    lg.info("")

    unittest.main()
