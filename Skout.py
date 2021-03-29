#!/bin/python3

import argparse
from Route import Route
import json
import numpy as np
from PlayList import PlayList

def main():
  parser = argparse.ArgumentParser(description='Make PDF output for scouting statistics.')
  parser.add_argument('inputFiles', metavar='File.json', nargs='+',
                      help='The names of the input files.')

  args = parser.parse_args()
  print("Reading from: {}".format(args.inputFiles))

  # testRoute = Route()
  # testRoute.setRoute("Slant")
  # print("{} is: {}".format(testRoute.getRoute(), testRoute.route))

  for fileName in args.inputFiles:
    with open(fileName) as json_file:
      data = json.load(json_file)
      # print(data)

      listOfPlays = np.array(data['plays'])
      # unique, counts = np.unique(plays, return_counts=True)
      # final = dict(zip(unique, counts))

      plays = PlayList()

      plays.addPlays(listOfPlays)

      plays.printAllPlays()

      # for p in data['plays']:
      #     print('Routes: {}'.format(p['routes']))
          # print('Website: ' + p['website'])
          # print('From: ' + p['from'])
          # print('')



if __name__ == "__main__":
  #Run as main program
  main()
