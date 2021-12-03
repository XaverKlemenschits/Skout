#!/usr/bin/env python3

# Skout - Flagfootball Scouting Analysis Tool
#   Copyright (C) 2021  Xaver Klemenschits
#   See LICENSE.txt for details

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import json
import sys
from PlayList import PlayList
from PlayStats import PlayStats
from SkoutPage import SkoutPage
from jsonschema import validate
import jsonschema
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from os import path
from os import makedirs
from platform import system as getOS


def register_ubuntu_font():
    """This function registers the ubuntu TTF font with reportlab, so it can be used in a PDF"""
    # pyinstaller puts added files into the dir saved in sys._MEIPASS
    # if we are not running from pyinstaller exe, use the current folder
    bundleDir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    fontPath = path.abspath(path.join(bundleDir, 'SkoutFonts')) + '/'
    pdfmetrics.registerFont(TTFont('Ubuntu', fontPath + 'Ubuntu-Regular.ttf'))
    pdfmetrics.registerFont(
        TTFont('Ubuntu-Bold', fontPath + 'Ubuntu-Bold.ttf'))
    pdfmetrics.registerFont(
        TTFont('Ubuntu-Italic', fontPath + 'Ubuntu-Italic.ttf'))
    pdfmetrics.registerFont(
        TTFont('Ubuntu-BoldItalic', fontPath + 'Ubuntu-BoldItalic.ttf'))


def get_schema(path):
    """This function loads the given schema available"""
    # path = 'skout.schema.json'
    # path = str(pathlib.Path(__file__).parent.absolute()) + '/skout.schema.json'
    try:
        with open(path, 'r') as file:
            schema = json.load(file)
    except IOError:
        print("Cannot open skout.schema file: \"{}\". Make sure it exists"
              " or specify the correct path using the -s option. "
              "For more details use the option --help.".format(path))
        sys.exit(1)
    return schema


def listAsIndices(listOfIndices):
    result = ""
    for val in listOfIndices:
        result = result + "[\'" + str(val) + "\']"
    return result


def validate_json(schemaFile, json_data, json_path):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(schemaFile)

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print("\nERROR in " + json_path + ":\n")
        print(err.message + "\n")
        print("In the following object:\n" + listAsIndices(err.path))
        return False

    return True


def doesFolderExist(name, createIfNoExist):
    if(not path.isdir(name)):
        if(createIfNoExist):
            makedirs(name)
        else:
            sys.exit("ERROR: Specified output folder does not exist!"
                     " Either create it first or use the \"-p\" option.")


def isUnix():
    return getOS() is not "Windows"


def isWindows():
    return getOS() is "Windows"


def getPathSeparator():
    if(isUnix()):
        return "/"
    else:
        return "\\"


def main():
    parser = argparse.ArgumentParser(
        description='Make PDF output for scouting statistics.')
    parser.add_argument('inputFiles', metavar='Skout.json', nargs='+',
                        help='The names of the input files.')
    parser.add_argument('-s', '--schema', metavar='skout.schema.json', nargs=1,
                        help='The schema file used for syntax checking the skout.json file',
                        dest='schemaFile', default=['skout.schema.json'])
    parser.add_argument('-o', metavar='TeamA_v_TeamB.pdf', nargs=1,
                        help='Name of the PDF output file', dest='outputName')
    parser.add_argument('-p', '--parents', action='store_true')

    args = parser.parse_args()
    print("Reading from: {}".format(args.inputFiles))
    print("Schema file: {}".format(args.schemaFile))

    # register Ubuntu font used for the PDF
    register_ubuntu_font()

    playList = PlayList()
    for fileName in args.inputFiles:
        with open(fileName) as json_file:
            data = json.load(json_file)
            if(not validate_json(args.schemaFile[0], data, fileName)):
                sys.exit(1)

            listOfPlays = data['plays']

            playList.setTeamNames(data['team'], data.get('opponent', ""))
            playList.setDate(data.get('date', ""))
            score = data.get('score', ["__", "__"])
            playList.setScore(score[0], score[1])
            playList.addPlays(listOfPlays)

    stats = PlayStats(playList)

    # first set default name
    outputName = stats.homeTeam + "_v_" + stats.awayTeam + \
        "-" + stats.date.replace(".", "_") + ".pdf"
    if(args.outputName is not None):
        if(args.outputName[0][-4:] == ".pdf"):
            outputName = args.outputName[0]
        elif(args.outputName[0][-1] == '/' or args.outputName[0][-1] == '\\'):
            outputName = args.outputName[0] + outputName
        else:
            sys.exit("ERROR: Invalid output filename! Must either be a PDF filename (\"name.pdf\")"
                     " or a directory (\"name" + getPathSeparator() + "\").")

    # check if folder exists and create it if it should be
    doesFolderExist(path.dirname(outputName), args.parents)

    counter = 1
    numPlays = 0
    page = SkoutPage(stats, outputName)
    while(numPlays < len(stats.routesList)):
        page.makePage(counter)
        numPlays = counter * page.rows * page.columns
        counter = counter + 1

    page.savePDF()
    print("Wrote Skout to file \'{}\'".format(outputName))


if __name__ == "__main__":
    # Run as main program
    main()
