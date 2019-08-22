# Creating a Command Line Utility In Python

# to run this program open command prompt and goto inside this file path folder
# type python prog56_Command_Line_Utility.py --x 23 --y 20 --o add 

import argparse
import sys

def calc(args):
    if args.o == 'add':
        return args.x + args.y
    elif args.o == 'sub':
        return args.x - args.y
    elif args.o == 'mul':
        return args.x * args.y
    elif args.o == 'div':
        return args.x / args.y
    else:
        return "Something went wrong !!!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=float, default=1.0, help="First argument should be any number.")
    parser.add_argument('--y', type=float, default=1.0,help="Second argument should be any number." )
    parser.add_argument('--o', type=str, default="add", help="This is operator for calculation.")
    
    args = parser.parse_args()
    sys.stdout.write(str(calc(args)))




