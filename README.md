Collection of scripts I use for comic management. If you need a new script created or functionality added/changed feel free to make an issue request. 

For most of the scripts you will need to modify some variables at the beginning, such as `MYLAR_API_KEY` or `MYLAR_API_URL`. If I make enough scripts I'll make a config.py for these

# CBZ to Mylar

This expects the comics to have been tagged with ComicTagger.

Goes through all the CBZ files in the directory(and subdirectories) it is ran from, checks the CV issue IDs from the notes in ComicInfo.XML, gets the series ID from ComicVine and adds them all to Mylar.

## Usage
You can copy the script in the directory you have your comics, or open a terminal in that directory and run it as such:
`python3 /path/to/cbz_to_mylar.py`

The default is to verify every single CBZ file in the current directory. 

Arguments:
`--folder-per-series` - Only verifies one comic in each sub-directory.
`--one-series-per-name` - Expects the comic names to be in the format: `<series_name> <issue_id> (<issue_year>)`. If you want a different format, request it in an issue, or modify line 78 with your own regex.

NOTE: This uses my own comicvine cache. You can use this as a drop-in replacement in ComicTagger, just drop the URL in. The data I've cached so far is for older comics, and at most a month or two old. For the purpose of finding a series ID that should generally be fine, but if you use it in ComicTagger you might miss some artist or whatever metadata was updated for those comics, so use it at your own risk. I haven't personally found anything missing though.

If there's any data I don't have, it will go through my api keys, so please be gentle. I have no rate limits of my own, but I do forward the 420 from ComicVine when I hit their limits


# Add to Mylar

Adds a comic to Mylar by CVID.

## Usage

`python3 add_to_mylar.py <cvid>`
