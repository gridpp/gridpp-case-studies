#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

#...for the BibTeX files.
import bibtexparser

# Import the Paper wrapper class.
from paper import Paper

# Import the VO wrapper class.
from vo import VirtualOrganisation

# Import the Figure wrapper class.
from figure import Figure

def replace_accents(s):
    s = s.replace('&eacute;', '\\\'e')
    s = s.replace('&oacute;', '\\\'o')
    return s

def replace_dashes(s):
    s = s.replace('&mdash;', '--')
    return s

def make_tex_links(s, links):
    for link_text, link in links.iteritems():
        tex_link = "\\href{%s}{%s}" % (link.replace("_","\_"), link_text)
        s = s.replace(link_text, tex_link)
    return s

class CaseStudy(object):
    def __init__(self, j):
        """
        Constructor.

        @param [in] j JSON representation of the case study.
        """

        ## The user community name.
        self.__full_user_community_name = j['full_name']

        ## The label.
        self.__label = j['label']

        ## The sector.
        self.__sector = j['sector']

        ## The raw overview text.
        self.__overview_raw = j['overview']

        ## The raw "The problem" text.
        self.__the_problem_raw = j['the_problem']

        ## The raw "The solution" text.
        self.__the_solution_raw = j['the_solution']

        ## The "What they said" raw quote text.
        self.__what_they_said = None
        #
        ## Who said it?
        self.__who_said_it = None
        #
        if 'what_they_said' in j.keys():
            self.__what_they_said = j['what_they_said']['quote']
            self.__who_said_it = j['what_they_said']['contact']

        ## A dictionary of the supporting sites.
        self.__sites = {}
        #
        for site in j['supporting_sites']:
            self.__sites[site.keys()[0]] = site.values()[0]

        ## A dictionary of services.
        self.__services = {}
        #
        for service in j['services']:
            self.__services[service.keys()[0]] = service.values()[0]

        ## A dictionary of Virtual Organisations (VOs).
        self.__vos = {}
        #
        if 'vos' in j.keys():
            for vo in j['vos']:
                my_vo = VirtualOrganisation(vo)
                self.__vos[my_vo.get_name()] = my_vo

        ## The acknowledgements raw text.
        self.__acknowledgements = None
        #
        if 'acknowledgements' in j.keys():
            self.__acknowledgements = j['acknowledgements']

        ## Dictionary of the hyperlinks.
        self.__links = {}
        #
        for link in j['links']:
            self.__links[link.keys()[0]] = link.values()[0]

        ## A dictionary of figures.
        self.__figures = {}
        #
        for fig in j['figures']:
            self.__figures[fig['label']] = Figure(fig)

        # Get the BibTeX items from the BibTeX file.
        with open("common/bib/GridPP.bib", 'r') as bibtex_file:
            bibtex_str = bibtex_file.read()

        ## The BibTeX database.
        bib_database = bibtexparser.loads(bibtex_str)

        lg.info(" *")
        lg.info(" * Number of entries in the BibTeX file: %d" % (len(bib_database.entries)))
        lg.info(" *")

        ## A dictionary of the papers.
        papers = {}

        # Get the papers (and check whether the PDF is there).
        for entry in bib_database.entries:
            if entry['ENTRYTYPE'] == 'article':
                paper = Paper(entry)
                papers[paper.get_id()] = paper

        ## A dictionary of publications used in the case study.
        self.__papers = {}
        #
        if 'references' in j.keys():
            for p in j['references']:
                # Get the paper.
                citecode = p.keys()[0]
                if citecode in papers.keys():
                    self.__papers[citecode] = papers[citecode]

    def get_full_user_community_name(self):
        return self.__full_user_community_name
    def get_label(self):
        return self.__label
    def get_sector(self):
        return self.__sector
    def get_list_of_services(self):
        return self.__services.keys()
    def get_number_of_figures(self):
        return len(self.__figures)
    def get_links(self):
        return self.__links
    def has_what_they_said(self):
        return self.__what_they_said != None
    def has_virtual_organisations(self):
        return len(self.__vos) > 0

    def get_overview_tex(self):
        s = """
%=============================================================================
\\subsection{Overview}
%=============================================================================
"""
        s += self.__overview_raw
        s = replace_accents(s)
        s = replace_dashes(s)
        return s

    def get_the_problem_tex(self):
        s = """
%=============================================================================
\\subsection{The problem}
%=============================================================================
"""
        s += self.__the_problem_raw
        s = replace_accents(s)
        s = replace_dashes(s)
        return s

    def get_the_solution_tex(self):
        s = """
%=============================================================================
\\subsection{The solution}
%=============================================================================
"""
        s += self.__the_solution_raw
        s = replace_accents(s)
        s = replace_dashes(s)
        return s

    def get_what_they_said(self):
        s = """
%=============================================================================
\\subsection{What they said}
%=============================================================================
"""
        s += "\\begin{quote}\n"
        s += "``\\emph{%s}''\n" % (self.__what_they_said)
        s += "\\end{quote}\n"
        s += "\\rightline{{\\rm --- %s}}\n" % (self.__who_said_it)
        return s

    def get_supporting_sites_tex(self):
        s = """
%=============================================================================
\\subsubsection{Supporting GridPP sites}
%=============================================================================
\\begin{itemize}
"""
        for site in sorted(self.__sites.keys()):
            s += "%\n"
            s += "\\item \\href{%s}{\\code{%s}}\n" % (self.__sites[site].replace("_","\_"), site)
        s += "\\end{itemize}\n"
        s += "%\n"
        return s

    def get_services_used_tex(self):
        s = """
%=============================================================================
\\subsubsection{Services used}
%=============================================================================
\\begin{itemize}
"""
        for service in sorted(self.__services.keys()):
            s += "%\n"
            s += "\\item \\bullettext{%s}: %s\n" % (service, self.__services[service])

        s += "\\end{itemize}\n"
        s += "%\n"
        return s

    def get_vos_tex(self):
        s = """
%=============================================================================
\\subsubsection{Virtual Organisations}
%=============================================================================
\\begin{itemize}
"""
        for vo in sorted(self.__vos.keys()):
            s += "%\n"
            s += "\\item \\href{%s}{\\bullettext{%s}} " % (self.__vos[vo].get_voms_server_url(), self.__vos[vo].get_name())
            s += "(\\href{%s}{Ops portal entry})\n" % (self.__vos[vo].get_ops_portal_url().replace('_','\_'))

        s += "\\end{itemize}\n"
        s += "%\n"
        return s

    def has_acknowledgements(self):
        return self.__acknowledgements != None
    def get_acknowledgements_tex(self):
        s = """
%=============================================================================
\\subsubsection{Acknowledgements}
%=============================================================================
"""
        s += "%s\n" % (self.__acknowledgements)
        return s

    def has_publications(self):
        return len(self.__papers) > 0
    def get_publications_tex(self):
        s = """
%=============================================================================
\\subsubsection{Publications}
%=============================================================================
\\begin{itemize}\n
"""
        for paper in sorted(self.__papers.values()):
            author = paper.get_authors()
            s += "\\item %s " % (author)
            s += "(%s), " % (paper.get_year())
            s += "``\emph{%s}'', " % (paper.get_title())
            s += "%s " % (paper.get_journal())
            s += "\\textbf{%d} " % (paper.get_volume())
            s += "%s " % (paper.get_pages())
            if paper.has_doi():
                s += "DOI:~\\href{%s}{%s}" % (paper.get_url().replace('_','\_'), paper.get_doi())
            else:
                s += "DOI:~\\href{%s}{%s}" % (paper.get_url().replace('_','\_'), paper.get_url())
            s += "\n"
        s += "\\end{itemize}\n\n"
        return s

    def get_figure_tex(self, num=1):
        fig = sorted(self.__figures.values())[num-1]
        s = """
%
\\begin{figure}[htbp]
  \\centering
  \\includegraphics[width=0.9\\textwidth]{assets/images/FILENAME}
  \\caption[SHORT_CAPTION]
  {\label{fig:LABEL}FULL_CAPTION}
\end{figure}
%
"""
        s = s.replace("SHORT_CAPTION", "%s" % (fig.get_short_caption_raw()))
        s = s.replace("FULL_CAPTION", "%s" % (fig.get_caption_raw()))
        s = s.replace("_", "\_")
        s = s.replace("FILENAME", "%s" % (fig.get_filename()))
        s = s.replace("LABEL", "%s" % (fig.get_label()))
        s = replace_accents(s)
        s = replace_dashes(s)
        return s

    def get_wordpress_html_overview(self):
        s = "<h3>Overview</h3>\n"
        s += """<p>The <a href="http://www.lsst.org" target="_blank">Large Synoptic Survey Telescope</a> (LSST) is an international physics facility being built at the Cerro Pach&oacute;n ridge in north-central Chil&eacute;.  It will use a three-billion-pixel camera to conduct a ten-year survey of the night sky in the visible electromagnetic spectrum.  The resulting catalogue of images &mdash; an estimated 200 petabytes of data &mdash; will enable scientists to answer some of the most <a href="http://www.lsst.org/about" target="_blank">fundamental questions we have about our Universe</a>.  One such use of this data is being explored by <a href="http://www.jb.man.ac.uk/research/" target="_blank">researchers at the University of Manchester</a>, who are studying the effect of dark matter and dark energy on the observed shape of galaxies.  By examining how galaxies are distorted by an effect known as <a href="http://dx.doi.org/10.1088/0034-4885/78/8/086901" target="_blank">cosmic shear</a>, insights can be gained into this missing ninety-five percent of everything we believe exists &mdash; the so-called <a href="http://www.stfc.ac.uk/research/astronomy-and-space-science/dark-matter/dark-matterenergy/" target="_blank">Dark Universe</a>.</p>\n"""

        return s

    def get_wordpress_page_html(self):
        """ Get the HTML for the WordPress site entry. """

        ## The HTML string.
        s = ""

        return s
