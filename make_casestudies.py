#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 make_casestudies.py

 Makes the case studies table and TeX files.

 See the README.md file and the GitHub wiki for more information.

 http://www.gridpp.ac.uk

"""

#...for the Operating System stuff.
import os

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for the JSOB.
import json

#...for the time (being).
import time

#...for the case study wrapper class.
from wrappers.casestudies import CaseStudy, make_tex_links


if __name__ == "__main__":

    print("*")
    print("*=====================*")
    print("* make_casestudies.py *")
    print("*=====================*")
    print("*")

    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFilePath",   help="Path to the input file.")
    parser.add_argument("outputPath",      help="Path to the output folder.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The output path.
    output_path = args.outputPath
    #
    # Check if the output directory exists. If it doesn't, raise an error.
    if not os.path.isdir(output_path):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (output_path))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    ## Log file path.
    log_file_path = os.path.join(output_path, 'log_make_casestudies.log')

    # Configure the logging.
    lg.basicConfig(filename=log_file_path, filemode='w', level=level)

    ## The path to the input file.
    input_file_path = args.inputFilePath
    #
    if not os.path.exists(input_file_path):
        raise IOError("* ERROR: Unable to find input file at '%s'." % (input_file_path))

    lg.info(" *===========================*")
    lg.info(" * make_casestudies_table.py *")
    lg.info(" *===========================*")
    lg.info(" *")
    lg.info(" * Input file path : %s" % (input_file_path))
    lg.info(" * Output path     : %s" % (output_path))
    lg.info(" *")
    print("* Input file path : %s" % (input_file_path))
    print("* Output path     : %s" % (output_path))
    print("*")


    # Get the case studies from the JSON file.

    with open(input_file_path, "r") as jf:
        js = json.load(jf)

    #print js

    ## The string for the case studies input list.
    l = ""

    ## The string for the case studies impact table.
    t = """
%______________________________________________________________________________
\\begin{table}[htbp]
\\caption{\\label{tab:casestudies}A list of the new user community case studies
included in this document.}
\\lineup
\\begin{indented}
\\item[]\\begin{tabular}{@{}llC{\\servw}C{\\servw}C{\\servw}C{\\servw}C{\\servw}C{\\servw}}
\\br
\\centre{1}{$\\quad$ User community $\\quad$} &
\\centre{1}{$\\quad$ Sector         $\\quad$} &
\\centre{1}{$\\quad$ Compute        $\\quad$} &
\\centre{1}{$\\quad$ Storage        $\\quad$} &
\\centre{1}{$\\quad$ CernVM         $\\quad$} &
\\centre{1}{$\\quad$ CVMFS          $\\quad$} &
\\centre{1}{$\\quad$ DIRAC          $\\quad$} &
\\centre{1}{$\\quad$ Ganga          $\\quad$} \\\\
\\mr
"""

    ## A list of case studies.
    cs = []

    # Add the case studies to the list.
    for cj in js:
        case_study = CaseStudy(cj)
        cs.append(case_study)
        lg.info(" * Adding case study '%s'." % (case_study.get_full_user_community_name()))

    lg.info(" * Processing case studies:")
    lg.info(" *")

    # Loop over the case studies.
    for c in sorted(cs):
        label = c.get_label()
        print("* Adding case study '%s'." % (c.get_full_user_community_name()))
        lg.info(" * Label       : %s" % (label))
        lg.info(" *")

        s = "%"
        s += "%=============================================================================\n"
        s += "\\section{%s}\n" % (c.get_full_user_community_name())
        s += "\\label{sec:%s}\n" % (c.get_label())
        s += "%=============================================================================\n"
        s += "%s\n\n" % (c.get_overview_tex())
        if c.get_number_of_figures() >= 1:
            s += "%s\n\n" % (c.get_figure_tex(1))
        s += "%s\n\n" % (c.get_the_problem_tex())
        if c.get_number_of_figures() >= 2:
            s += "%s\n\n" % (c.get_figure_tex(2))
        s += "%s\n\n" % (c.get_the_solution_tex())
        if c.has_what_they_said():
            s += "%s\n\n" % (c.get_what_they_said())
        s += "%=============================================================================\n"
        s += "\\subsection{Further details}\n"
        s += "%=============================================================================\n"
        s += "%s\n\n" % (c.get_services_used_tex())
        s += "%s\n\n" % (c.get_supporting_sites_tex())
        if c.has_virtual_organisations():
            s += "%s\n\n" % (c.get_vos_tex())
        if c.has_publications():
            s += "%s\n\n" % (c.get_publications_tex())
        if c.has_acknowledgements():
            s += "%s\n\n" % (c.get_acknowledgements_tex())

        # Make the TeX links.
        s = make_tex_links(s, c.get_links())

        ## The TeX output path for each case study TeX file.
        case_study_tex_output_path = os.path.join(output_path, "casestudies/auto%s.tex" % (label))
        #
        with open(case_study_tex_output_path, "w") as cf:
            cf.write(s)

        # Add the case study to the list.
        l += "\\input{casestudies/auto%s}\n\\newpage\n" % (c.get_label())

        # Add the case study entry to the table.
        t += "%s (p\\pageref{sec:%s}) & %s & " % \
            (c.get_full_user_community_name(), c.get_label(), c.get_sector())
        #
        # Compute
        if "Virtual Organisations" in c.get_list_of_services() or "Compute" in c.get_list_of_services():
            t += "\\checkmark & "
        else:
            t += "& "
        #
        # Storage
        if "Storage" in c.get_list_of_services():
            t += "\\checkmark & "
        else:
            t += "& "
        #
        # CernVM
        if "CernVM" in c.get_list_of_services():
            t += "\\checkmark & "
        else:
            t += "& "
        #
        # CVMFS
        if "CVMFS" in c.get_list_of_services():
            t += "\\checkmark & "
        else:
            t += "& "
        #
        # GridPP DIRAC
        if "The GridPP DIRAC service" in c.get_list_of_services():
            t += "\\checkmark & "
        else:
            t += "& "
        #
        # Ganga
        if "Ganga" in c.get_list_of_services():
            t += "\\checkmark \\\\\n"
        else:
            t += "\\\\\n"

    # Complete the presentations table.
    t += """
\\br
\\end{tabular}
\\end{indented}
\\end{table}
%______________________________________________________________________________
"""

    lg.info(" *")
    print("*")

    ## The path of the table TeX file.
    output_tex_table_path = os.path.join(output_path, "autotable.tex")
    #
    with open(output_tex_table_path, "w") as tf:
        tf.write(t)

    ## The path of the input TeX file.
    output_tex_list_path = os.path.join(output_path, "casestudies/autolist.tex")
    #
    with open(output_tex_list_path, "w") as tf:
        tf.write(l)

    print("* Done! Don't forget to edit and rename:")
    print("*")
    print("* autotable.tex            --> table.tex, and")
    print("* casestudies/autolist.tex --> casestudies/list.tex")
    print("*")
    print("* Before compiling with:")
    print("*")
    print("$ source process.sh")
