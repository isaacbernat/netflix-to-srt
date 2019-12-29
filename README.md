# netflix-to-srt
1. Get the subtitles from netflix (`.xml` dfxp or `.vtt` files)
2. Convert them into `.srt`

## Get the subtitles from netflix
### Method 1
You need [Google Chrome](https://www.google.com/chrome/browser/desktop/). *not tested on other web browsers*

1. Open devtools. This is usually accomplished by either:
    - Pressing `Cmd` + `Alt` + `i`.
    - Pressing `F12`.
2. Go to Network tab within dev tools.
3. Load your movie/episode.
4. Select the subtitle you want.
5. In devtools sort by name and look for a file with `?o=` at the beginning of the name (see image below).

<img src="https://github.com/isaacbernat/netflix-to-srt/blob/master/chrome_console.png?raw=true" alt="Chrome console screenshot" width="557px" height="607px">

### Method 2
The information is extracted from [this post](http://forum.opensubtitles.org/viewtopic.php?t=15141).

You need FireFox and AdblockPlus Add-On. *not tested on other browsers*
- Start Netflix and your movie/episode (stream is active!)
- Start AdblockPlus, open blockable items
- Search: dfxp *(e.g. >> #.nflximg.com/#/#/########.dfxp?v=1&e=#########&t=######_#####&random=1234567890)*
- open the dfxp in a new window
- Save as

## Convert them into .srt
- [Get python](https://www.python.org/downloads/) (tested under python 2.7, 3.3 and newer). *If you have mac or linux you may skip this step*
- Clone this repository or download `to_srt.py`
- Run the script in the terminal (`python to_srt.py`)
  - Input and output directories default to the same directory `to_srt.py` is run
  - Use `-i INPUT_PATH` and `-o OUTPUT_PATH` for custom file locations
  - All `.xml` and `.vtt` files in the input directory will generate a converted `.srt` file on the output one
- Enjoy! (And star the repo if you liked it ;D)

## Why this repository?
VLC player could not reproduce that kind of xml subtitles and I could not find any tool that could easily transform the xml files to a suitable format (e.g. SubRip (`.srt`)) in Linux or Mac. I got a request for WebVTT (`.vtt`) and did the same.

## TODOs
- More robust file parsing than just some quick and dirty regexes
- Javascript/web version so this can be done entirely through a browser
- Real tests. The way to "test" it now is by running `python to_srt.py -i samples -o samples` from the the project's root directory and check the `.srt` results (or `python3 to_srt.py -i samples -o samples`).
- Create a pip package for this

## Note:
In no way I am encouraging any kind of illegal activity. Please know your local laws and ask for written permissions from content owners (e.g. Netflix) when necessary.
