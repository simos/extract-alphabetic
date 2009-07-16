#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# extract-alphabetic.py
#
# Parses Unicode-data.txt and creates a table for alphabetic characters, those
# characters that are part of a lowercase-uppercase pair.
#
# You may need to switch your python installation to utf-8, if you get 'ascii' codec errors.
#
# Complain to Simos Xenitellis (simos@gnome.org, http://simos.info/blog) for this craft.

from re             import findall, match, split, sub
from string         import atoi
from unicodedata    import normalize, decimal
from urllib         import urlretrieve
from os.path        import isfile, getsize

import sys
import getopt

# We grab files off the web, left and right.
URL_UNICODEDATA = 'http://unicode.org/Public/UNIDATA/UnicodeData.txt'
FILENAME_UNICODEDATA = 'UnicodeData.txt'

def download_hook(blocks_transferred, block_size, file_size):
    """ A download hook to provide some feedback when downloading """
    if blocks_transferred == 0:
        if file_size > 0:
            print "Downloading", file_size, "bytes: ",
    sys.stdout.write('#')
    sys.stdout.flush()

def download_file(url):
    """ Downloads a file provided a URL. Returns the filename. """
    """ Borks on failure """
    localfilename = url.split('/')[-1]
    if not isfile(localfilename) or getsize(localfilename) <= 0:
        print "Downloading ", url, "..."
        try: 
            urlretrieve(url, localfilename, download_hook)
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)
            sys.exit(-1)
        except:
            print "Unexpected error: ", sys.exc_info()[0]
            sys.exit(-1)
        print " done."
    else:
        print "Using cached file for ", url
    return localfilename

def process_unicodedata():
    """ Grabs and opens the UnicodeData.txt file from Unicode.org """
    filename_unicodedatatxt = download_file(URL_UNICODEDATA)
    try: 
        unicodedatatxt = open(filename_unicodedatatxt, 'r')
    except IOError, (errno, strerror):
        print "I/O error(%s): %s" % (errno, strerror)
        sys.exit(-1)
    except:
        print "Unexpected error: ", sys.exc_info()[0]
        sys.exit(-1)

    """ Parse the UnicodeData.txt file """
    linenum_unicodedatatxt = 0
    for line in unicodedatatxt.readlines():
        linenum_unicodedatatxt += 1
        line = line.strip()
        components = split(';', line)

        codepoint = components[0]
        description = components[1]
        character_type = components[2] # το τρίτο πεδίο
        field13 = components[12]
        field14 = components[13]
        if character_type == 'Ll' and field13 != '':
            print codepoint, description
        elif character_type == 'Lu' and field14 != '':
            print codepoint, description
        else:
            pass
    unicodedatatxt.close()

process_unicodedata()
