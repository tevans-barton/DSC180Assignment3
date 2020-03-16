#!/usr/bin/env python

import sys
import json



def main(targets):

    if 'data' in targets:
    	#write data ingestion code
    if 'clean' in targets:
    	#write data cleaning code
    if 'model' in targets:
    	#write modeling code

    return


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)