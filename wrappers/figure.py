#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

class Figure(object):
    """
    Wrapper base class for a figure.
    """

    def __init__(self, jf):
        """
        @param [in] jvo JSON object representaing the figure.
        """

        ## The figure label.
        self.__label = jf['label']

        ## The order of the figure in the case study.
        self.__order = int(jf['order'])

        ## The figure filename.
        self.__filename = jf['filename']

        ## The short caption (for use in figure lists etc.).
        self.__caption_short = jf['short_caption']

        ## The full caption.
        self.__caption = jf['caption']

    def __lt__(self, other):
        return self.__order < other.__order
    def get_label(self):
        return self.__label
    def get_filename(self):
        return self.__filename
    def get_caption_raw(self):
        return self.__caption
    def get_short_caption_raw(self):
        return self.__caption_short
    def get_order(self):
        return self.__order
