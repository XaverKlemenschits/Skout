# Skout - Flagfootball Scouting Analysis Tool

## Usage

- Create a file ending in ".skout.json" and pass it to the Skout.py script:
```sh
./Skout.py mySkout.skout.json
```

- The script will output an svg in A4 format containing the 15 most often used plays.

## Prerequisits

- Python3
- drawSvg (`pip3 install drawSvg`)
- argparse (`pip3 install argparse`)

## Fromat of the .skout.json file

The format of the data is given in the file `skout.schema.json`. Use any editor supporting [json schemas](https://json-schema.org) to get auto-completion, default values, etc.

## Contributing

Have a look at `TODO.md` for a list of missing features if you want to contribute. Bug reports, pull requests and feature requests should be filed on GitHub.

## License
 