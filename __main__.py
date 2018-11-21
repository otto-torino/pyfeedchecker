import sys
import os
from argparse import ArgumentParser

from feedchecker import Checker

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="input path to check and filter")
parser.add_argument("-o", "--output", dest="output",
                    help="output path")

args = parser.parse_args()

if not args.input:
    sys.exit('Specify an input file, run with -h option for help')
if not args.output:
    sys.exit('Specify an output file, run with -h option for help')
if not os.path.isfile(args.input):
    sys.exit('Cannot find the input file, dude')

checker = Checker(args.input, args.output)
checker.run()
