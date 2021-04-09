#!/bin/python3

import argparse
import json
import numpy as np
from PlayList import PlayList
from PlayStats import PlayStats

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

      listOfPlays = np.array(data['plays'])

      playList.addPlays(listOfPlays)

  stats = PlayStats(playList)
  stats.print()


if __name__ == "__main__":
  #Run as main program
  main()
