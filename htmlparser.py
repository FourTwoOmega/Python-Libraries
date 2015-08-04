#!/usr/bin/env python
'''
This library contains classes to parse and store HTML.

Python 2.7
'''

__author__ = 'Ken Kauffman'
__version__ = '1.0.0'

from HTMLParser import HTMLParser

#
# This class will take in an HTML file and store data from a table contained
#+ within. The class will NOT properly handle an invalidly formatted HTML table.
#+ This class assumes there is only one table per HTML file fed to it.
#
class TableParser(HTMLParser):
    # This integer represents the value of the index of the current table
    #+ row. It is used to keep track of which row number is currently being
    #+ written to the self.table matrix class data member.
    trindex = 0

    # These flags correspond to HTML tags (trflag to tag tr, etc.). When a
    #+ start tag that corresponds to one of these flags is encountered, it
    #+ is set to 'True' (see def handle_starttag()). When an end tag that
    #+ corresponds to one of these flags is encountered, it is set to
    #+ 'False' (see def handle_endtag()).
    tableflag = False
    trflag = False
    thflag = False
    tdflag = False

    # This two-dimensional matrix holds the data parsed from the HTML table.
    table = [[]]

    #
    # Constructor; calls parent constructor and initializes variables.
    #
    def __init__(self):
        HTMLParser.__init__(self)
        self.trindex = 0
        self.tableflag = False
        self.trflag = False
        self.thflag = False
        self.tdflag = False

    #
    # Any start tag in the HTML fed to this class will be handled by this
    #+ function.
    # This function overrides the base class' version of this function.
    # INPUT: tag - The HTML start tag is fed automatically to this function
    #+ when calling feed().
    # INPUT: attrs - The HTML start tag's attributes are fed automatically
    #+ to this function when calling feed().
    #
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.tableflag = True
        if tag == 'tr':
            self.trflag = True
            # A row is created at initialization; this condition prevents an
            #+ extra row from being created.
            if self.trindex > 0:
                # Add a row to the table
                self.table.append([])
        if tag == 'th':
            self.thflag = True
        if tag == 'td':
            self.tdflag = True

    #
    # Any end tag in the HTML fed to this class will be handled by this function.
    # This function overrides the base class' version of this function.
    # INPUT: tag - The HTML end tag is fed automatically to this function
    #+ when calling feed().
    # 
    def handle_endtag(self, tag):
        if tag == 'table':
            self.tableflag = False
        if tag == 'tr':
            self.trflag = False
            self.trindex += 1    # Increase row index for next row
        if tag == 'th':
            self.thflag = False
        if tag == 'td':
            self.tdflag = False

    #
    # Any data between HTML tags fed to this class will be handled by this function.
    # This function overrides the base class' version of this function.
    # INPUT: data - The HTML data is fed automatically to this function when
    #+ calling feed().
    #
    def handle_data(self, data):
        if self.tableflag:
            if self.trflag:
                if self.thflag:
                    # Prevent table header information from being written more than once
                    assert self.trindex == 0, "Table header in multiple rows: row %s" % \
                        self.trindex
                if self.thflag or self.tdflag:
                    # Write data to next column in row of table, but strip whitespace
                    self.table[int(self.trindex)].append(data.strip())

    #
    # This function is called to extract the data from an HTML table.
    # INPUT: sourcefile - The HTML file from which to extract the table
    #
    def parsefile(self, sourcefile):
        with open(sourcefile, 'rb') as s:
            self.feed(s.read())
            s.close()

    #
    # This function prints the whole table.
    #
    def printtable(self):
        for index, row in enumerate(self.table):
            print index, '\t'.join(row)

    #
    # This function returns the table data member of this class which is a
    #+ two-dimensional list.
    # OUTPUT: self.table - The table data member of this class
    #
    def gettable(self):
        return self.table

    #
    # This function returns a specified column belonging to the table data
    #+ member of this class. It assumes the header row is row 0 of self.table().
    # INPUT: columnname - The name of the specified column to be returned
    # INPUT: includename - Boolean value where True means include header name in results
    # OUTPUT: column - The column as a list from self.table
    #
    def getcolumn(self, columnname, includename=False):
        # Retrieve header row (assumed to be first row)
        header = self.getrow(0)

        # Ensure specified column exists, then get its position (0, 1, 2...)
        assert columnname in header, "Invalid column name: \"%s\"" % columnname
        columnnum = self.table[0].index(columnname)

        # This is the list that will be returned by the function. It is
        #+ only declared here so it will be in the same scope as the
        #+ return statement.
        column = []

        # Iterate through all the rows in the table and get the item at the same
	#+ position as the specified column in the header row, adding it to a list.
        for row in self.table:
            column.append(row[columnnum])

        # If it is not desirable for the column name to be returned with the
	#+ column data, remove it from the list containing the data.
        if not includename:
            del column[0]

        return column
		
    #
    # This function returns a specified row belonging to the table data
    #+ member of this class.
    # INPUT: row - The desired row number to be returned.
    # OUTPUT: self.table[row] - The row as a list from self.table
    #
    def getrow(self, row):
        return self.table[row]

