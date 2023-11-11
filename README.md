# MangaNeloDownloader

Simple CLI tool to download chapters from MangaNelo website.

## Installation

1. Create a python virtual environment: `python -m venv .venv` or `python3 -m venv .venv`
2. Activate it: On Win10: `.venv\Scripts\activate` & On Unix OS `source .venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`

## Configuration

In the file `global_vars.py`:

- You can change the *USER_AGENT* variable if needed.
- Change the *MS* variable that is the waiting time in seconds between each downloaded images
- You have to change the *DOWNLOAD_PATH* variable, it can be relative or absolute

## Usage

Simply start the `main.py` file: `python main.py`. <br>
Now follow the instructions. <br>
When selecting chapters to download they are few keywords to use to confirm etc: <br>

- `ALL`: to select all chapters
- `STOP`: to confirm your choice, go next

You can also use range, ex: 10-20 will select chapter 10 to chapter 20

NB: the 'chapter index' is the number that is white highlighted on the left, it's the index on the list so be careful.

## Contributing

Feel free to contribute to this project and if any errors don't hesitate to fix them and make a PR.

## TODO

- [ ] Make a GUI
- [ ] Multiple downlaod at the time
