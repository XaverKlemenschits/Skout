# Skout - Flagfootball Scouting Analysis Tool

## Using the packaged windows version with VSCode

- Install [VS Code](https://code.visualstudio.com/)
- Download the latest release of Skout from the [Releases Page](https://github.com/XaverKlemenschits/Skout/releases) choosing the correct .zip file for your operating system (for example `Skout_Windows-vx.x.x.zip`)
- Unpack the .zip file containing the `Skout.exe` and `skout.schema.json` into a folder.
- Open this folder in VSCode by clicking on "File" -> "Open Folder..."
- Code-highlighting und auto-completion in VSCode must be enabled. See the section below for details.

In order to generate your scout file:
- Click on the menu item `Terminal` and then `New Terminal` in VSCode.
- In the terminal, type `Skout.exe example.skout.json` to generate a single `.pdf` file for the example scout.

**Nota Bene**: If windows stops the execution with a security warning, you can still execute it by clicking on "More info" and then "Run Anyway".

## Code Highlighting and Auto Completion in VSCode

- Press `Ctrl`+`Shift`+`P`. This will open a line at the top of the VSCode window.
- In this line, type "Open Settings" and choose "Preferences: Open Settings (JSON)" from the list of available options.
- This will open a new file, which starts with a `{` in the first line.
- After this first `{`, insert the following text:
```json
    "json.schemas": [
    {
        "fileMatch": [
            "/*.skout.json"
        ],
        "url": "./skout.schema.json"
    }
    ],
```
- Now press `Ctrl`+`S` to save the file
- Now you can close the file and restart VSCode for the changes to become effective.
- When you now open a file ending in `.skout.json`, VSCode will list the available options for each entry.

## Fromat of the .skout.json file

The format of the data is given in the file `skout.schema.json`. Use any editor supporting [json schemas](https://json-schema.org) to get auto-completion, default values, etc. We recommend using [VS Code](https://code.visualstudio.com/), since we use it and optimize towards its use.

### Strongside

You have to specify a strongside for each play, if none is given, **strong right is chosen automatically**.

### Route numbers

**The numbering of receivers depends on the strongside**: The receivers are always listed from left to right looking into the direction of progression.
Therefore, the order the routes should be given in changes depending on the strong side:
- strong right: ACBD
- strong left:  ABCD
- trips right:  CABD
- trips left:   ABDC

When specifying the routes, you have to use numbers since route names are not recognized. The numbers for the specific routes are listed below.

- 0 "Stop",
- 1 "Quick Out",
- 2 "Slant",
- 3 "Comeback Out",
- 4 "Comeback In",
- 5 "10 Out",
- 6 "10 In",
- 7 "Corner",
- 8 "Post",
- 9 "Go",
- 10 "5 In",
- 11 "5 Out",
- 12 "Pivot",
- 13 "Post-Corner",
- 14 "Reverse",
- 15 "Quick In",
- 16 "Yoyo",
- 17 "Stop&Go"
- 18 "Out&Up"
- 19 "Post Comeback"
- 20 "Screen"

## Using the packaged Windows version without VSCode

The Skout program is contained in `Skout.exe` and must be started using the windows command line (`CMD`).
To start `CMD`, press the windows button and enter `cmd`, then press `Enter`.
A window with the command line should open, displaying something like this in the last line:

```bash
PS C:\Users\myUser>
```
This means you are currently in the folder `User\myUser`.

Now navigate to the folder where your `Skout.exe` is located. This is done by using *change directory* (`cd`):

```bash
cd FolderName
```
where `FolderName` is the name of the folder you want to enter.

Once you are in the folder containing `Skout.exe`, you can run the example file by entering

```
Skout.exe example.skout.json
```
This will create a `.pdf` file containing the final scout in your current folder.
**Nota Bene**: If windows stops the execution with a security warning, you can still execute it by clicking on "More info" and then "Run Anyway".

If you have problems, make sure that `skout.schema.json` is also in the same folder.

In order to create your own scout, make a new file ending in `.skout.json` and enter the plays in the format shown in `example.skout.json`.
For all available options, look at `skout.schema.json`.

## Usage of the Python lib

- Create a file ending in ".skout.json" and pass it to the Skout.py script:
```sh
./Skout.py mySkout.skout.json
```

- The script will output a `.pdf` file with the plays sorted by the number of times they were run.

## Dependencies

- Python3
- reportlab (`pip3 install reportlab`)
- argparse (`pip3 install argparse`)
- jsonschema (`pip3 install jsonschema`)

## Contributing

Have a look at `TODO.md` for a list of missing features if you want to contribute. Bug reports, pull requests and feature requests should be filed on GitHub.

## License

See LICENSE.txt