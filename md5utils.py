#!/usr/bin/env python
'''
This file contains functions to utilize Python's hashlib for MD5s.
'''

__author__ = 'Ken Kauffman'
__version__ = '1.0.0'

import datetime
import hashlib
import os

#
# This method reads in a file a piece at a time to avoid loading the entire file
#+ into memory at once.
# INPUT: filename - the file name of the file whose MD5 is to be generated
# INPUT: numblocks - the number of blocks to read from the file at a time
# OUTPUT: hex string of file md5
#
def generatefilemd5(filename, numblocks=32):
    result = ''
    filehash = hashlib.md5()
    chunksize = numblocks * filehash.block_size
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(chunksize), b''):
            filehash.update(chunk)
            result = filehash.hexdigest()
        f.close()
    return result

#
# This method retrieves the stored MD5 from the specified file.
# INPUT: filename - the name of the file that contains the stored MD5
# OUTPUT: the value from the file
#
def retrievemd5(filename):
    result = ''
    try:
        # Store file size for later use. This ensures this value is populated
        #+ in error messages.
	filesize = os.path.getsize(filename)

        # Read in value from file.
        with open(filename, 'rb') as f:
            result = str(f.read()).strip()
        f.close()

        # Assert that file is 32 hex digits in size.
        assert filesize is 32

        # Check if value read is in hexidecimal (ValueError)
	int(result, 16)
    except (AssertionError, ValueError) as e:
        print "MD5 is corrupt!\n\tfile=%s\n\tSize=%s\n\tValue=%s" % \
            (filename, str(filesize), str(result))
        result = '00000000000000000000000000000000'
        print "Using all zeroes as \"old\" MD5 value"
    # Catch OSError and IOError when file does not exist.
    except EnvironmentError as (errno, strerror):
        # If file does not exist, just assign all zeroes as MD5.
        if errno == 2:
            print "No hash to read from file ", filename
            result = '00000000000000000000000000000000'
            print "Returning all zeros as MD5"
        # For all other errors and exceptions, let them occur.
        else:
            raise
    return result

#
# This method clears the file where an MD5 is stored then writes the new MD5 to
#+ it.
# INPUT: newmd5 - the value which to write into filename
# INPUT: filename - the name of the file that is to contain the stored MD5
#
def storemd5(md5, filename):
    with open(filename, 'wb') as f:
        f.seek(0)
        f.truncate()    # Clear file contents
        f.write(md5)
    f.close()

