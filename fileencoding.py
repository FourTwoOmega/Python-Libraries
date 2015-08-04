#!/usr/bin/env python
'''
This library is for functionality pertaining to file encoding (ASCII, Unicode, etc.).

Python 2.7
'''

__author__ = "Ken Kauffman"
__version__ = "1.0.0"

import codecs
import os

#
# This method changes one type of encoding to another based on the arguments.
# INPUT: sourcefile - the file whose encoding is to change
# INPUT: sourceencoding - the original encoding of the source file
# INPUT: desiredencoding - the encoding to which to convert the source file
# INPUT: blocksize - the block size to read at a time from the source file
#
def changefileencoding(sourcefile, sourceencoding, desiredencoding, blocksize=32):
    # Temp file to which to write data in desired encoding
    tmpfile = sourcefile + '.tmp'

    # Read source file in blocks, write blocks to temp file as desired encoding
    with codecs.open(sourcefile, 'rb', sourceencoding) as sf:
        with codecs.open(tmpfile, 'wb', desiredencoding) as tf:
            for block in iter(lambda: sf.read(blocksize), b''):
                tf.write(block)
        tf.close()
    sf.close()

    # Remove old ASCII file
    os.remove(sourcefile)

    # Rename tmpfile to what ASCII file was called
    os.rename(tmpfile, sourcefile)

