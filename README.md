# How to get `.srt` subtitles from streaming services
1. [Get the subtitles](https://github.com/isaacbernat/netflix-to-srt#get-the-subtitles) (`.xml` dfxp or `.vtt` files from Netflix, YouTube... streaming media services).
    - [From Netflix](https://github.com/isaacbernat/netflix-to-srt#from-netflix)
    - [From YouTube](https://github.com/isaacbernat/netflix-to-srt#from-youtube)
2. [Convert them](https://github.com/isaacbernat/netflix-to-srt#convert-them-into-srt) into `.srt` files (and/or shift timestamps).
3. [Star this repo ⭐](https://github.com/isaacbernat/netflix-to-srt#star-this-repo)

## Get the subtitles
### From Netflix
 > **Note:** There is a [video-tutorial covering all instructions step-by-step in Youtube on how to to download and convert subtitles from Netflix](https://www.youtube.com/watch?v=ZpejTczG8Ho) using Windows and Google Chrome.[![YouTube link to the tutorial](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/images/tutorial.png "YouTube link to the tutorial")](https://www.youtube.com/watch?v=ZpejTczG8Ho)

### Get subtitles from Netflix: method 1
1. You need one of the following web browsers:
   - [Google Chrome](https://www.google.com/chrome/browser/desktop/)
   - Firefox
   - Safari
   - Microsoft Edge
   - Opera
2. Install [Tampermonkey](https://www.tampermonkey.net/), links below:
   - [Chrome extension](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
   - [Firefox addon](https://addons.mozilla.org/firefox/addon/tampermonkey/)
   - [Safari howto](https://www.tampermonkey.net/?browser=safari)
   - [Microsoft Edge addon](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd)
   - [Opera addon](https://addons.opera.com/extensions/details/tampermonkey-beta/)
3. Install [Netflix - subtitle downloader](https://greasyfork.org/en/scripts/26654-netflix-subtitle-downloader) script for Tampermonkey.
4. To download the subtitles file from Netflix, open the episode in Netflix and download them by clicking on _"Download subs from this episode"_ (see image below). ![Screenshot of "Download subs" option](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/images/netflix-tampermonkey-download-subs.png "Screenshot of 'Download subs' option")

### Get subtitles from Netflix: method 2
You need [Google Chrome](https://www.google.com/chrome/browser/desktop/). *not tested on other web browsers*

1. Open devtools. This is usually accomplished by either:
    - Pressing `Cmd` + `Alt` + `i`.
    - Pressing `F12`.
2. Go to Network tab within dev tools.
3. Load your movie/episode.
4. Select the subtitle you want.
5. In devtools sort by name and look for a file with `?o=` at the beginning of the name (see image below).

![Screenshot of Dev tools download](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/images/netflix-devtools-download-subs.png "Screenshot of Dev tools download")

### Get subtitles from Netflix: method 3
The information is extracted from [this post](http://forum.opensubtitles.org/viewtopic.php?t=15141).

You need FireFox and AdblockPlus Add-On. *not tested on other browsers*
- Start Netflix and your movie/episode (stream is active!)
- Start AdblockPlus, open blockable items
- Search: dfxp *(e.g. `>> #.nflximg.com/#/#/########.dfxp?v=1&e=#########&t=######_#####&random=1234567890`)*
- open the dfxp in a new window
- Save as

### From YouTube
> **Note:** One must ensure subtitles in the YouTube video (captions) are enabled before running commands below. 
### Get subtitles from YouTube: method 1
- Install [youtube-dl](https://github.com/ytdl-org/youtube-dl) (available for Windows, Mac and Linux)
- Download subs from the YouTube URL you like. E.g. `youtube-dl --all-subs "https://www.youtube.com/watch?v=VHNfvFOBC0A"`
- Subtitles should be downloaded in the same folder were the command was ran. E.g. `NameOfTheVideo VHNfvFOBC0A.ca.vtt, NameOfTheVideo VHNfvFOBC0A.tlh.vtt`
- If you are missing a language, check that it's actually available. E.g. `youtube-dl --list-subs "https://www.youtube.com/watch?v=VHNfvFOBC0A"`

### Get subtitles from YouTube: method 2
- Install [youtube-dlp](https://github.com/yt-dlp/yt-dlp-wiki/blob/master/Installation.md) (available for Windows, Mac and Linux). It's a fork version of youtube-dl by [Snap](https://snapcraft.io/yt-dlp).
- Download subs from the YouTube URL you like. E.g. `yt-dlp --skip-download --write-auto-subs --sub-lang "en" "https://youtu.be/cVsyJvxX48A"` 
- The above command will download YouTube subtitles in VTT format. *Alternatively*, one may use it's own integrated converter to get them in `srt` format right away. E.g. `yt-dlp --skip-download --write-auto-subs --convert-subs srt --sub-lang "en" "https://youtu.be/cVsyJvxX48A`
- To download the video with audio and subtitles, simply omit the --skip-download option. E.g. `yt-dlp --write-auto-subs --sub-lang "en" "https://youtu.be/cVsyJvxX48A"`

## Convert them into .srt
- [Get python](https://www.python.org/downloads/) (tested under python 2.7, 3.3 and newer). *If you have mac or linux you may skip this step*
- Clone this repository or [download it as a ZIP file](https://github.com/isaacbernat/netflix-to-srt/archive/refs/heads/master.zip) or [download `to_srt.py` file](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/to_srt.py)
- Run the script in the terminal (type `python to_srt.py` or `python3 to_srt.py` from the terminal on the folder you have `to_srt.py`)
  - Copy your subtitle files in the same directory as `to_srt.py`
    - Or use `-i INPUT_PATH` and `-o OUTPUT_PATH` for custom file locations
  - All `.xml` and `.vtt` files in the input directory will generate a converted `.srt` file on the output one
- *Optional:* Use `-d DELAY_MS` parameter when running the script to delay all the timestamps by the given number of milliseconds. Negative values shift timestamps backwards. Example: `python to_srt.py -i samples/delays -o samples/delays -d -1500` will take all the eligible files in `samples/delays` and shift the resulting `.srt` subtitles to be 1.5 seconds earlier than the original version
- Enjoy! (And **star the repo ⭐** if you liked it ;D)

## Star this repo
If you like this project, please **star the repository ⭐**. It's free and it helps get visibility and future improvements.
- You may skip the following step if you are already logged in Github.
  - [Sign in](https://github.com/login) if you have an account.
  - [Sign up](https://github.com/signup?source=login) if you don't have an account (it's free!).
- Scroll to the top of this page or [open it in a new tab/window](https://github.com/isaacbernat/netflix-to-srt) and check the for a star icon (it's near the screen laterals)
  - If the star icon is already yellow ⭐, congrats! It's already starred! You don't need to do anything else.
  - If the star icon is empty ☆, you may click on it once, and it'll become yellow ⭐!
  ![Wide screenshot of the star icon](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/images/star_screenshot_desktop.png "Wide screenshot of the star icon")
  ![Thin screenshot of the star icon](https://raw.githubusercontent.com/isaacbernat/netflix-to-srt/master/images/star_screenshot_mobile.png "Thin screenshot of the star icon")
- Thanks for your contribution!

## Why this repository?
[VideoLAN's VLC media player](https://www.videolan.org/vlc/) could not reproduce that kind of xml subtitles and I could not find any tool that could easily transform the xml files to a suitable format (e.g. SubRip (`.srt`)) in Linux or Mac, so I wrote this script and decided to share. I got a request for WebVTT (`.vtt`) and did the same.

Similarly, adjusting timestamps in 50ms increments was inconvenient using VLC's hotkeys (G, H and/or J) for large mismatches (e.g. 60 seconds because openings or summaries), so I added the `-d DELAY_MS` parameter so I could "advance" all the subtitles lines easily.

## TODOs
- More robust file parsing than just some quick and dirty regexes.
- Javascript/web version so this can be done entirely through a browser.
- Real tests. The way to "test" it now is by running `python to_srt.py -i samples -o samples` from the the project's root directory and check the `.srt` results (or `python3 to_srt.py -i samples -o samples`).
- Create a pip package for this.
- More screenshots so 'Get the subtitles' section is easier to follow.

## Note:
In no way I am encouraging any kind of illegal activity. Please know your local laws and ask for written permissions from content owners (e.g. Netflix, YouTube) when necessary.

## Contribution 
Contributions are always welcome! Feel free to create a Pull Request and add screenshots for each step/method that works best for you. Your help will make this project even better for everyone.
