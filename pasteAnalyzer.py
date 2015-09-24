#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: @EzequielTBH

# PasteAnalyzer: Search and analyze .
# Search in Google custom engine for a keyword in the text and analyze this for
# match with regular expressions.

# Support: github.com, gist.github.com, pastebin.com, pastee.org, and pastie.org.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License,or any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from googleapiclient.discovery import build
import argparse
import urllib2
import json
import sys
import re

#Check nested list, if is Empty.
def isEmpty(seq):
    flag = True

    for element in seq:
        if element != None:
            flag = False

    return flag

#Search the keyword in Google search custom engine
def searchEngine(apiKey, query, engineId, startIndex):
    try:

        service = build("customsearch", "v1", developerKey = apiKey)
        response = service.cse().list(q = "text:" + query,
            cx = engineId, start = startIndex).execute()
        return response

    except Exception as e:
        print("[!]Exception searching in Google:\n" + e.message )
        sys.exit()

#Gets the raw content links of each site
def getRawLinks(response, verbose):
    links=[]

    for i in range(0, response["queries"]["request"][0]["count"] ):

        linkTemp = response["items"][i]["link"]
        if verbose:
            print ("[*]Link: " + linkTemp )

        if linkTemp.find("pastebin.com") > -1:
            links.append("http://pastebin.com/raw.php?i=" + linkTemp[20:] )

        elif linkTemp.find("pastie.org") > -1:
            links.append("http://pastie.org/pastes/" + linkTemp[25:] + "/text")

        elif linkTemp.find("github.com") > -1:
            dataHtml = urllib2.urlopen(linkTemp).read()
            dataSplit = dataHtml.split('>Raw</a>',1)[0]

            dataSplit = dataSplit[
                dataSplit.rfind('<a href="') + 9:].split('"')[0]

            if dataSplit == '':
                links.append(linkTemp)
            else:

                if linkTemp.find("gist.github.com") > -1:
                    links.append("https://gist.github.com" + dataSplit)
                else:
                    links.append("https://github.com" + dataSplit )

        else:
            links.append(linkTemp)

    return links

#Get all results of Google , raw content link
def getLinksFinal(apiKey, query, engineId, verbose):

    print("\n[*]Searching in Google")

    res = searchEngine(apiKey, query, engineId, 1)
    links = getRawLinks(res, verbose)

    #If is the last page, throw exception and pass, no problem
    try:
        while( res["queries"]["nextPage"] ):

            res = searchEngine(apiKey, query, engineId,
                int( res["queries"]["request"][0]["startIndex"] ) + 10)

            linksTemp = getRawLinks(res, verbose)

            for i in linksTemp:
                links.append(i)
    except:
        pass

    if verbose:
        for i in links:
            print("[*]Raw Link: " + i)

    if links == []:
        print("\n[!]No Results.")
        sys.exit()

    return links

#Apply regular expresion in content and extract information
def regex(data, regexs):

    data = data.split("\n")
    info = []

    for regex in regexs:

        if regex.find("#") == 0:
            info.append(regex[1:])
        else:
            result = [x.group(1) for x in [re.search(regex,line)for line in data] if x ]

            if not isEmpty(result):
                info.append(result)
            else:
                info.pop()

    if not isEmpty(info):
        return info
    else:
        return []

#Load regular expressions in a list.
def loadRegexs(path , verbose):
    regexs = []

    try:
        with open(path,"r") as fileRegex:

            for line in fileRegex:
                line = line.strip("\n")

                if line != "":
                    regexs.append(line)

            fileRegex.close()

    except Exception as e:
        print("[!]Exception loading regular expressions:\n" + e.message)
        sys.exit()

    if verbose:

        print("\n[*]Loaded regular expressions:")
        for i in regexs:
            print(" " + i)

    return regexs

#List Results example
#[
#    u'http://pastebin.com/AB51SAQS2',
#    [
#     'Email',[ 'email@email.com','myemail@domain.com' ]
#    ],
#    u'htpp://pastee.org/jw5151a',
#    [
#     'Password',[ 'Mypasswordis123', 'Mypass' ],
#     'EMail',[ 'email@dom.com' ]
#    ]
#]
def printResults(results):

    for element in results:

        if type(element) == str or type(element) == unicode:
            print("[*]Link: " + element)

        else:

            for element2 in element:

                if type(element2) == str or type(element2) == unicode:
                    print(" => Category:\t" + element2)

                else:
                    for element3 in element2:
                        print("   " + element3)

def main():
    # Input validation
    parser = argparse.ArgumentParser(prog = 'pasteAnalyzer',
        epilog = "Example: ./%(prog)s.py -q passwords -a API_KEY" +
         " -e ENGINE_ID -r REGEX_FILE",
        description = "Search in Google custom engine for a keyword in the" +
        " text and analyze this for match with regular expressions." +
         " Support github.com, gist.github.com, pastebin.com," +
         "pastee.org and pastie.org")

    parser.add_argument('-q', '--query', action = "store", type = str,
        required = True, dest = 'query', help = 'Search query')

    parser.add_argument('-a', '--api-key', action = "store", type = str,
        required = True, dest = 'apiKey', help = 'Google custom search Api Key')

    parser.add_argument('-e', '--engine-id', action = "store", type = str,
        required = True, dest = 'engineId', help = 'Google custom search Engine Id')

    parser.add_argument('-r', '--regex-file', action = "store", type = str,
        required = True, dest = 'regexFile', help = 'File with regex for analysis')

    parser.add_argument('-v', '--verbose', action = "store_true",
        required = False, default = False , dest = 'verbose', help = 'Verbose mode')

    parser.add_argument('-j', '--json', action = "store", type = str,
        required = False, dest = 'json', help = 'Output to JSON file')

    args = parser.parse_args()

    regexs = loadRegexs(args.regexFile, args.verbose)
    links = getLinksFinal(args.apiKey, args.query, args.engineId, args.verbose)
    results = []

    #Get content and analyze
    print("[*]Analyze information")
    for link in links:

        try:
            data = urllib2.urlopen(link).read()
        except Exception as e:
            print("[!]Exception connecting URL:\n" + e.message)

        #pastee.org link not is raw content => get raw content
        if link.find("pastee.org") > -1:

            dataSplit = data.split(
                '<td class="code"><div class="syntax"><pre>',1)[1]

            returned = regex( dataSplit[ : dataSplit.find('</pre></div>') ],
                 regexs )
        else:
            returned = regex(data, regexs)

        if returned != []:
                results.append(link)
                results.append(returned)

    print("\n[*]Results:\n")

    if results == []:
        print("[!]No Results!!")

    else:
        printResults(results)

        #If is required, write results to JSON file
        try:
            if args.json:
                with open(args.json, 'w') as out:
                    json.dump(results, out)
                print("[*]JSON file writed!")

        except Exception as e:
            print("[!]Exception opening file JSON:\n" + e.message)

#Ready ... GO!
main()




