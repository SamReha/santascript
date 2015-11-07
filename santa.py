import argparse
import csv
import re   # Regex module
import smtplib
import json
from random import randrange

class CSVError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def main():
    # First things first, let's read in our config file
    config = json.loads(open('config.json', 'r').read())

    dataLocation = 'data/default.csv'
    dataDestination = 'data/pairs.csv'
    emailAddr = config['sendAddress']
    emailPswrd = config['sendAddressPassword']
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

    participants = getParticipants(dataLocation)
    pairs = getPairs(participants)
    csvString = stringifyPairs(pairs)

    writeTextFile(dataDestination, csvString)
    if sendEmails:
        sendAllEmails(emailAddr, emailPswrd, pairs)


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

def getPairs(participants):
    pairs = []
    index = randrange(0, len(participants))
    firstElement = participants[index]
    firstElementCopy = firstElement  # We use this at the end
    del participants[index]

    while (len(participants) > 0):
        index = randrange(0, len(participants))
        secondElement = participants[index]
        del participants[index]

        pairs.append([firstElement, secondElement])
        firstElement = secondElement

    # To complete the loop, pair the resulting secondElement with our copy of the origin firstElement
    pairs.append([secondElement, firstElementCopy])

    return pairs

def isAnEmail(emailString):
    return re.match('^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', emailString)

def stringifyPairs(pairs):
    csvString = ''
    for pair in pairs:
        csvString = csvString + (pair[0]['name'] + ',' + pair[0]['email'] + ',' + pair[1]['name'] + ',' + pair[1]['email'] + '\n')

    return csvString

def writeTextFile(location, content):
    outputFile = open(location, 'w')
    outputFile.write(content)
    outputFile.close

def sendAllEmails(address, password, pairs):
    # Do email setup
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(address,password)

    # For each pairing, send an email
    for pair in pairs:
        recepientName = pair[0]['name']
        recepientEmail = pair[0]['email']
        pairName = pair[1]['name']

        body = ('Hello ' + recepientName + ',\n\n'
                'This is an automatically generated email to inform you of your Secret Santa match.\n'
                'Your match is ' + pairName + '.\n\n'
                'Merry Christmas!\n'
                'SantaBot')

        server.sendmail(address, recepientEmail, body)

    server.quit()

if __name__ == '__main__':
    main()
