Collection of scripts I use for comic management. If you need a new script created or functionality added/changed feel free to make an issue request. 

For most of the scripts you will need to modify some variables at the beginning, such as `MYLAR_API_KEY` or `MYLAR_API_URL`. If I make enough scripts I'll make a config.py for these

# CBZ to Mylar

This expects the comics to have been tagged with ComicTagger.

Goes through all the CBZ files in the directory(and subdirectories) it is ran from, checks the CV issue ID from the notes in ComicInfo.XML and adds them to Mylar.

## Usage
You can copy the script in the directory you have your comics, or open a terminal in that directory and run it as such:
`python3 /path/to/cbz_to_mylar.py`

The default is to verify every single CBZ file in the current directory. 

Arguments:
`--folder-per-series` - Only verifies one comic in each sub-directory.
`--one-series-per-name` - Expects the comic names to be in the format: `<series_name> <issue_id> (<issue_year>)`. If you want a different format, request it in an issue, or modify line 78 with your own regex.

# Add to Mylar

Adds a comic to Mylar by CVID.

## Usage

`python3 add_to_mylar.py <cvid>`
