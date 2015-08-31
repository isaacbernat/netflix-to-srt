# netflix-to-srt
1. Get the subtitles from netflix
2. Convert them into .srt

## Get the subtitles from netflix
The information is extracted from [this post](http://forum.opensubtitles.org/viewtopic.php?t=15141)

you need... FireFox and AdblockPlus Add-On. *not tested on other browsers*
- Start Netflix and your movie/episode (stream is active!)
- Start AdblockPlus, open blockable items
- Search: dfxp *(e.g. >> #.nflximg.com/#/#/########.dfxp?v=1&e=#########&t=######_#####&random=1234567890)*
- open the dfxp in a new window
- Save as.

## Convert them into .srt
- Get python (works under both 2.7 and 3.3)
- Clone this repository or download `to_srt.py`
- Place `to_srt.py` in the same directory where subtitle file is
- Edit `FILE_NAME = "sample.xml"` to match your subtitle file
- Run the script in the terminal (`python to_srt.py`)
- Enjoy! (You will have a newly created *.srt file with the subtitles)


## Why this repository?
VLC player could not reproduce that kind of xml subtitles and I could not find any tool that could easily transform the xml files to a suitable format (e.g. .srt) in linux or mac.

## TODOs
- Change file names on the command line, no need to edit the file.
- Multiple files/directories at once.
- More robust file parsing than just some quick and dirty regexes.
- Javascript/web version so this can be done entirely through a browser
- Tests (not just the "sample" file)

## Note:
In no way I am encouraging any kind of illegal activity. Please know your local laws and ask for written permissions from content owners (e.g. Netflix) when necessary.
