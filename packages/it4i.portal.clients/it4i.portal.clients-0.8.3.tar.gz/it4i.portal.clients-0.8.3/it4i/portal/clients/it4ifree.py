#!/usr/bin/env python
"""
Show some basic information from IT4I PBS accounting
"""
import argparse
import getpass
import sys
import pycent

from tabulate import tabulate
from .logger import LOGGER
from .config import API_URL
from .config import IT4IFREETOKEN
from .config import CONFIG_FILES
from .jsonlib import jsondata

TABLE_ME_TITLE = 'Projects I am participating in'
TABLE_ME_AS_PI_TITLE = 'Projects I am Primarily Investigating'
TABLE_LEGENDS_TITLE = 'Legend'

def ifpercent(part, whole, percent):
    """
    Return percent if required and it is possible, otherwise return origin number
    """
    if percent:
        try:
            return pycent.percentage(part, whole)
        except ZeroDivisionError:
            raise ZeroDivisionError
    else:
        return part

def user_header(unit):
    """ Return user header """
    header = ['PID', 'Type', 'Days left', 'Total']
    if unit == 'wch' or unit == 'both':
        header.append('Used WCHs')
    if unit == 'nch' or unit == 'both':
        header.append('Used NCHs')
    if unit == 'wch' or unit == 'both':
        header.append('My WCHs')
    if unit == 'nch' or unit == 'both':
        header.append('My NCHs')
    header.append('Free')
    return header

def pi_header(unit):
    """ Return pi header """
    header = ['PID', 'Type', 'Login']
    if unit == 'wch' or unit == 'both':
        header.append('Used WCHs')
    if unit == 'nch' or unit == 'both':
        header.append('Used NCHs')
    return header

def user_row(row, arguments):
    """ Return user row """
    table_row = []
    for key in ['pid', 'type', 'days_left', 'total']:
        table_row.append(row[key])
    try:
        if arguments.unit == 'wch' or arguments.unit == 'both':
            table_row.append(ifpercent(row['used'], row['total'], arguments.percent))
        if arguments.unit == 'nch' or arguments.unit == 'both':
            table_row.append(ifpercent(row['used_with_factor'], row['total'],
                                       arguments.percent))
        if arguments.unit == 'wch' or arguments.unit == 'both':
            table_row.append(ifpercent(row['used_by_me'], row['total'], arguments.percent))
        if arguments.unit == 'nch' or arguments.unit == 'both':
            table_row.append(ifpercent(row['used_by_me_with_factor'], row['total'],
                                       arguments.percent))
    except ZeroDivisionError:
        return None
    table_row.append(ifpercent(row['free'], row['total'], arguments.percent))
    return table_row

def pi_row(row, row_previous, jsonout, arguments):
    """ Return pi row """
    total = [project['total'] for project in jsonout['me'] if project['pid'] == row['pid']][0]
    table_row = []
    for key in ['pid', 'type']:
        table_row.append(row[key] if row[key] != row_previous[key] else '')
    table_row.append(row['login'])
    try:
        if arguments.unit == 'wch' or arguments.unit == 'both':
            table_row.append(ifpercent(row['core_hours'], total, arguments.percent))
        if arguments.unit == 'nch' or arguments.unit == 'both':
            table_row.append(ifpercent(row['core_hours_with_factor'], total, arguments.percent))
    except ZeroDivisionError:
        return None
    return table_row

def main():
    """
    main function
    """

    parser = argparse.ArgumentParser(description="""
The command shows some basic information from IT4I PBS accounting. The
data is related to the current user and to all projects in which user
participates.""",
                                     epilog="""
Columns of "%s":
         PID: Project ID/account string.
        Type: Standard or multiyear project.
   Days left: Days till the given project expires.
       Total: Core-hours allocated to the given project.
        Used: Sum of core-hours used by all project members.
          My: Core-hours used by the current user only.
        Free: Core-hours that haven't yet been utilized.

Columns of "%s" (if present):
         PID: Project ID/account string.
        Type: Standard or multiyear project.
       Login: Project member's login name.
        Used: Project member's used core-hours.
""" % (TABLE_ME_TITLE, TABLE_ME_AS_PI_TITLE),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--percent', action='store_true',
                        help="""
show values in percentage. Projects with unlimited resources are not displayed""")
    parser.add_argument('-u', '--unit', action='store', help='unit', default='nch',
                        choices=['wch', 'nch', 'both'])
    arguments = parser.parse_args()

    if IT4IFREETOKEN is None:
        LOGGER.error("""Missing or unset configuration option: %s
Suggested paths:
%s
""", "it4ifreetoken", CONFIG_FILES)
        sys.exit(1)

    username = getpass.getuser().strip()
    jsonout = jsondata(('%s/it4ifree/%s' % (API_URL, username)), {'it4ifreetoken' : IT4IFREETOKEN})

    table_me_headers = user_header(arguments.unit)
    table_me = []
    for row in jsonout['me']:
        table_row = user_row(row, arguments)
        if table_row:
            table_me.append(table_row)

    table_me_as_pi_headers = pi_header(arguments.unit)
    table_me_as_pi = []
    row_previous = {'pid': '', 'type': ''}
    for row in jsonout['me_as_pi']:
        table_row = pi_row(row, row_previous, jsonout, arguments)
        if table_row:
            table_me_as_pi.append(table_row)
        row_previous = {'pid': row['pid'], 'type': row['type']}

    if table_me:
        print >> sys.stdout, '\n%s\n%s' % (TABLE_ME_TITLE,
                                           len(TABLE_ME_TITLE) * '=')
        print tabulate(table_me, table_me_headers)

    if table_me_as_pi:
        print >> sys.stdout, '\n%s\n%s' % (TABLE_ME_AS_PI_TITLE,
                                           len(TABLE_ME_AS_PI_TITLE) * '=')
        print tabulate(table_me_as_pi, table_me_as_pi_headers)

    print >> sys.stdout, '\n%s\n%s' % (TABLE_LEGENDS_TITLE,
                                       len(TABLE_LEGENDS_TITLE) * '=')
    print 'WCH   =    Wall-clock Core-Hour'
    print 'NCH   =    Normalized Core-Hour'

if __name__ == "__main__":
    main()
