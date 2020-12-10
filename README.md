# netflix-to-srt
1. [Get the subtitles](https://github.com/isaacbernat/netflix-to-srt#get-the-subtitles) from Netflix (`.xml` dfxp or `.vtt` files), YouTube or other sources.
2. [Convert them](https://github.com/isaacbernat/netflix-to-srt#convert-them-into-srt) into `.srt`
- **Note:** There is a [video-tutorial covering all instructions step-by-step in Youtube on how to to download and convert subtitles from Netflix](https://www.youtube.com/watch?v=ZpejTczG8Ho) using Windows and Google Chrome. [![YouTube link to the tutorial](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/tutorial.png "YouTube link to the tutorial")](https://www.youtube.com/watch?v=ZpejTczG8Ho)

## Get the subtitles:
### From Netflix: method 1
You need [Google Chrome](https://www.google.com/chrome/browser/desktop/). *not tested on other web browsers*

1. Open devtools. This is usually accomplished by either:
    - Pressing `Cmd` + `Alt` + `i`.
    - Pressing `F12`.
2. Go to Network tab within dev tools.
3. Load your movie/episode.
4. Select the subtitle you want.
5. In devtools sort by name and look for a file with `?o=` at the beginning of the name (see image below).

<img src="https://github.com/isaacbernat/netflix-to-srt/blob/master/chrome_console.png?raw=true" alt="Chrome console screenshot" width="557px" height="607px">

### From Netflix: method 2
The information is extracted from [this post](http://forum.opensubtitles.org/viewtopic.php?t=15141).

You need FireFox and AdblockPlus Add-On. *not tested on other browsers*
- Start Netflix and your movie/episode (stream is active!)
- Start AdblockPlus, open blockable items
- Search: dfxp *(e.g. >> #.nflximg.com/#/#/########.dfxp?v=1&e=#########&t=######_#####&random=1234567890)*
- open the dfxp in a new window
- Save as

### From YouTube
- Install [youtube-dl](https://github.com/ytdl-org/youtube-dl) (available for Windows, Mac and Linux)
- Download subs from the YouTube URL you like e.g. `youtube-dl --all-subs "https://www.youtube.com/watch?v=VHNfvFOBC0A"`
- Subtitles should be downloaded in the same folder were the command was ran. E.g. `NameOfTheVideo VHNfvFOBC0A.ca.vtt, NameOfTheVideo VHNfvFOBC0A.tlh.vtt`
- If you are missing a language, check that it's actually available. E.g. `youtube-dl --list-subs "https://www.youtube.com/watch?v=VHNfvFOBC0A"`

## Convert them into .srt
- [Get python](https://www.python.org/downloads/) (tested under python 2.7, 3.3 and newer). *If you have mac or linux you may skip this step*
- Clone this repository or [download `to_srt.py`](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/to_srt.py)
- Run the script in the terminal (type `python to_srt.py` from the terminal on the folder you have `to_srt.py`)
  - Copy your subtitle files in the same directory as `to_srt.py`
    - Or use `-i INPUT_PATH` and `-o OUTPUT_PATH` for custom file locations
  - All `.xml` and `.vtt` files in the input directory will generate a converted `.srt` file on the output one
- Enjoy! (And **star the repo** if you liked it ;D)

## Why this repository?
VLC player could not reproduce that kind of xml subtitles and I could not find any tool that could easily transform the xml files to a suitable format (e.g. SubRip (`.srt`)) in Linux or Mac. I got a request for WebVTT (`.vtt`) and did the same.

## TODOs
- More robust file parsing than just some quick and dirty regexes
- Javascript/web version so this can be done entirely through a browser
- Real tests. The way to "test" it now is by running `python to_srt.py -i samples -o samples` from the the project's root directory and check the `.srt` results (or `python3 to_srt.py -i samples -o samples`).
- Create a pip package for this

## Note:
In no way I am encouraging any kind of illegal activity. Please know your local laws and ask for written permissions from content owners (e.g. Netflix, YouTube) when necessary.
