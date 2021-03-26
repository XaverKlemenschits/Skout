#!/bin/python3

import argparse
from Route import Route

def main():
    parser = argparse.ArgumentParser(description='Make PDF output for scouting statistics.')
    parser.add_argument('inputFiles', metavar='File.json', nargs='+',
                        help='The names of the input files.')

    args = parser.parse_args()
    # print(args.inputFiles)

    testRoute = Route()
    testRoute.setRoute("Slant")
    print("{} is: {}".format(testRoute.getRoute(), testRoute.route))



if __name__ == "__main__":
  #Run as main program
  main()
