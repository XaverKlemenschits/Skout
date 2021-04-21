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
import pathlib

def get_schema():
    """This function loads the given schema available"""
    path = str(pathlib.Path(__file__).parent.absolute()) + '/skout.schema.json'
    with open(path, 'r') as file:
        schema = json.load(file)
    return schema

def listAsIndices(listOfIndices):
    result = ""
    for val in listOfIndices:
      result = result + "[\'" + str(val) + "\']"
    return result


def validate_json(json_data):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema()

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err.message + "\n")
        print("Failed validating \'{}\' in {}{}:".format(err.validator,
            err._word_for_schema_in_error_message,
            listAsIndices(list(err.relative_schema_path)[:-1])))
        print("    During validation of {}{}".format(err._word_for_instance_in_error_message, listAsIndices(err.path)))
        # print(err.path)
        return False

    return True

def main():
  parser = argparse.ArgumentParser(description='Make PDF output for scouting statistics.')
  parser.add_argument('inputFiles', metavar='File.json', nargs='+',
                      help='The names of the input files.')

  args = parser.parse_args()
  print("Reading from: {}".format(args.inputFiles))

  playList = PlayList()
  for fileName in args.inputFiles:
    with open(fileName) as json_file:
      data = json.load(json_file)
      if(not validate_json(data)):
        sys.exit(1)

      listOfPlays = data['plays']

      playList.setTeamNames(data['team'], data.get('opponent', "nA"))
      playList.setDate(data.get('date', "nA"))
      score = data.get('score', ["nA", "nA"])
      playList.setScore(score[0], score[1])
      playList.addPlays(listOfPlays)

  stats = PlayStats(playList)
  # stats.print()

  page = SkoutPage(stats)
  page.makeSvg()


  
if __name__ == "__main__":
  #Run as main program
  main()
