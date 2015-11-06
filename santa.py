import argparse

dataLocation = 'data/default.csv'
dataDestination = 'data/pairs.csv'
sendEmails = False
verbose = False

parser = argparse.ArgumentParser(description='Welcome to Santa Script, the terrible and low-feature tool to manage Secret Santa events at the Command Line!')
parser.add_argument('-s', '--spread', metavar='', type=str, help='the location of your participant spreadsheet')
parser.add_argument('-p', '--pairs', metavar='', type=str, help='the name and location of where the pairs spreadsheet will be saved. Defaults to /data/pairs.csv')
parser.add_argument('-e', '--send_emails', metavar='', help='this flag will cause the script to attempt to automatically email participants about their pairing')
parser.add_argument('-v', '--verbose', metavar='', help='get verbose output as program is running')

# Parse args and runtime and configure run settings
args = parser.parse_args()
if args.spread != None:
    dataLocation = args.spread
if args.pairs != None:
    dataDestination = args.pairs
if args.send_emails != None:
    sendEmails = True
if args.verbose != None:
    verbose = True
