import argparse
import csv
import re   # Regex module

class CSVError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def main():
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

    # Try to read in the initial data file...
    participants = getParticipants(dataLocation)

def getParticipants(fileString):
    participantList = []
    try:
        with open(fileString, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row[0] is '':
                    raise CSVError('Participant name left blank.')
                elif not isAnEmail(row[1]):
                    raise CSVError('Participant email left blank.')
                else:
                    participantList.append({'name': row[0], 'email': row[1]})
    except IOError as e:
        print 'Couldn\'t open file at ' + fileString + '.\nMaybe you forgot to specify a location for the initial spreadsheet?'
    except CSVError as e:
        print e
        print 'CSV file at ' + fileString + ' was poorly formatted. Please check docs and try again.'

    return participantList

def isAnEmail(emailString):
    return re.match('^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', emailString)

if __name__ == '__main__':
    main()
