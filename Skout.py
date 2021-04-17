#!/bin/python3

import argparse
import json
import numpy as np
from PlayList import PlayList
from PlayStats import PlayStats
from SkoutPage import SkoutPage

def main():
  parser = argparse.ArgumentParser(description='Make PDF output for scouting statistics.')
  parser.add_argument('inputFiles', metavar='File.json', nargs='+',
                      help='The names of the input files.')

  args = parser.parse_args()
  print("Reading from: {}".format(args.inputFiles))

  playList = PlayList()
  teamName = ""
  date = ""
  for fileName in args.inputFiles:
    with open(fileName) as json_file:
      data = json.load(json_file)

      listOfPlays = np.array(data['plays'])

      playList.setTeamNames(data['team'], "")
      playList.setDate(data['date'])
      playList.addPlays(listOfPlays)

      # teamName = data['team']
      # date = data['date']

  stats = PlayStats(playList)
  # stats.print()

  page = SkoutPage(stats)
  page.draw()


  
if __name__ == "__main__":
  #Run as main program
  main()
