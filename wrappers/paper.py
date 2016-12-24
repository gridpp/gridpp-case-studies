#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

class Paper(object):
    """
    Wrapper base class for a paper.
    """

    def __init__(self, bd):
        """
        Constructor.

        @param [in] bd BibTeX entry dictionary.
        """

        ## The ID.
        self.__id = bd['ID']

        ## The title.
        self.__title = None
        #
        if 'title' in bd.keys():
            self.__title = bd['title']

        ## The author(s).
        self.__author = None
        #
        if 'author' in bd.keys():
            self.__author = bd['author']

        ## The year of publication.
        self.__year = None
        #
        if 'year' in bd.keys():
            self.__year = bd['year']

        if bd['ENTRYTYPE'] == "book":
            lg.info(" * %s is a book, skipping." % (self.get_id()))
            lg.info(" *")
            return None

        ## The journal.
        self.__journal = None
        #
        if 'journal' in bd.keys():
            self.__journal = bd['journal']

        ## The volume.
        self.__volume = None
        #
        if 'volume' in bd.keys():
            self.__volume = int(bd['volume'])

        ## The pages.
        self.__pages = None
        #
        if 'pages' in bd.keys():
            self.__pages = bd['pages']

        ## The Digital Object Identifier (DOI).
        self.__doi = None
        #
        if 'doi' in bd.keys():
            self.__doi = bd['doi']

        ## The URL.
        self.__url = None
        #
        if 'link' in bd.keys():
            self.__url = bd['link']

        ## Custom annotation - used in summary tables etc.
        self.__annotation = None
        #
        if 'annote' in bd.keys():
            self.__annotation = bd['annote']

        lg.info(" * Paper ID  : '%s'" % (self.get_id()))
        lg.info(bd)

        if self.has_title(): lg.info(" * Title     : '%s'" % (self.get_title()))
        else:                lg.info(" * '%s' HAS NO TITLE!" % (self.get_id()))
        if self.has_year():  lg.info(" * Year      : '%s'" % (self.get_year()))
        else:
            lg.info(" * '%s' HAS NO YEAR!" % (self.get_id()))
            #raise IOError("* %s has no year!" % (self.get_id()))
        if self.has_doi():  lg.info(" * DOI     : '%s'" % (self.get_doi()))
        else:
            lg.info(" * '%s' HAS NO DOI!"    % (self.get_id()))
            #raise IOError("* %s has no DOI!" % (self.get_id()))
        lg.info(" *")


    def __lt__(self, other):
        return self.get_year() < other.get_year()
    def get_id(self):
        return self.__id
    def has_title(self):
        return self.__title != None
    def get_title(self):
        return self.__title
    def has_author(self):
        return self.__author != None
    def get_authors(self):
        authors = self.__author.split('and')
        author_s = authors[0]
        if "and others" in self.__author.lower():
            author_s += "et al."
        return author_s
    def has_year(self):
        return self.__year is not None
    def get_year(self):
        return self.__year
    def has_journal(self):
        return self.__journal != None
    def get_journal(self):
        return self.__journal
    def has_volume(self):
        return self.__volume != None
    def has_pages(self):
        return self.__pages != None
    def get_pages(self):
        return self.__pages
    def get_volume(self):
        return self.__volume
    def has_doi(self):
        return self.__doi is not None
    def get_doi(self):
        return self.__doi
    def has_url(self):
        return self.__url is not None
    def get_url(self):
        return self.__url
    def has_annotation(self):
        return self.__annotation is not None
    def get_annotation(self):
        return self.__annotation
