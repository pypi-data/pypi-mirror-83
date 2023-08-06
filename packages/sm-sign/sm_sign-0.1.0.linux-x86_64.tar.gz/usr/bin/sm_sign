#!/usr/bin/python
from sm_sign import *
from sm_sign.parse import *
import sys
# from .parse import *
# import sign
# import sys
def main():
    # print(args.command)
    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    if(args.command in ['genkey', 'sign', 'verify']):
        args.func(args)
    
if __name__ == '__main__':
    main()