<p align="center">
  <span style="font-size: 2em; font-weight: bold; font-family: 'Arial', sans-serif; background-color: rgba(0, 255, 0, 0.5); padding: 15px; border: 2px solid rgba(0, 255, 0, 0.7); color: white;">SRT Converter</span>
</p>

---
---

#### It is used to convert the <span style="color: pink;">`.vtt`</span> and <span style="color: pink;">`.xml`</span> files into the <span style="color: pink;">`.srt`</span> format. We do this because it is widely supported by various media players, platforms, and devices, as many popular media players (e.g., VLC, Windows Media Player) and streaming services prefer <span style="color: pink;">`.srt`</span>, as it is universal and simple & standardized.

> **<span style="color: pink;">Note:</span>**  
> I also found that VLC Player could not reproduce these kinds of XML subtitles, and I could not find any tool that could easily transform XML files to a suitable format (e.g., SubRip <span style="color: pink;">`.srt`</span>) on Linux or macOS. I got a request for WebVTT (<span style="color: pink;">`.vtt`</span>) and added support for it as well; that's why it encouraged me to make this.

---

<p align="center" style="width: 100%; padding: 0; margin: 0;">
  <span style="font-size: 1.5em; font-weight: bold; font-family: 'Arial', sans-serif; border: 2px solid rgba(255, 0, 0, 0.5); padding: 15px; display: inline-block; background-color: rgba(255, 0, 0, 0.7); color: white; width: 100%; text-align: center;">Get the subtitles:</span>
</p>

---
---

# 1. Netflix-To-SRT <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="red" style="vertical-align: middle; margin-left: 5px;"><title>Netflix</title><path d="M5.398 0v.006c3.028 8.556 5.37 15.175 8.348 23.596 2.344.058 4.85.398 4.854.398-2.8-7.924-5.923-16.747-8.487-24zm8.489 0v9.63L18.6 22.951c-.043-7.86-.004-15.913.002-22.95zM5.398 1.05V24c1.873-.225 2.81-.312 4.715-.398v-9.22z"/></svg>


Get the subtitles from Netflix (`.xml` dfxp or `.vtt` files), YouTube, or other sources and convert them into `.srt` format.



## Method 1

| Step | Description |
|------|-------------|
| 1    | You need one of the following web browsers: <ul><li>[Google Chrome](https://www.google.com/chrome/browser/desktop/)</li><li>Firefox</li><li>Safari</li><li>Microsoft Edge</li><li>Opera</li></ul> |
| 2    | Install [Tampermonkey](https://www.tampermonkey.net/). Links below: <ul><li>[Chrome extension](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)</li><li>[Firefox addon](https://addons.mozilla.org/firefox/addon/tampermonkey/)</li><li>[Safari how-to](https://www.tampermonkey.net/?browser=safari)</li><li>[Microsoft Edge addon](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd)</li><li>[Opera addon](https://addons.opera.com/extensions/details/tampermonkey-beta/)</li></ul> |
| 3    | Install [Netflix - subtitle downloader](https://greasyfork.org/en/scripts/26654-netflix-subtitle-downloader) script for Tampermonkey. |
| 4    | To download the subtitles file from Netflix, open the episode in Netflix and download them by clicking on "Download subs from this episode". ![Tampermonkey Subtitle Downloader](netflix-to-srt-master/chrome_console.png) |

## Method 2

| Step | Description |
|------|-------------|
| 1    | You need [Google Chrome](https://www.google.com/chrome/browser/desktop/). *Not tested on other web browsers* |
| 2    | Open devtools by pressing `Cmd + Alt + i` or `F12`. |
| 3    | Go to the Network tab within dev tools. |
| 4    | Load your movie/episode. |
| 5    | Select the subtitle you want. |
| 6    | In devtools, sort by name and look for a file with `?o=` at the beginning of the name. ![Chrome Console](path-to-image/Screenshot-from-2024-10-18-00-02-41.png) |

## Method 3

| Step | Description |
|------|-------------|
| 1    | The information is extracted from [this post](http://forum.opensubtitles.org/viewtopic.php?t=15141). |
| 2    | You need Firefox and AdblockPlus Add-On. *Not tested on other browsers* |
| 3    | Start Netflix and your movie/episode (stream is active!). |
| 4    | Start AdblockPlus, open blockable items. |
| 5    | Search for: dfxp (e.g. `> #.nflximg.com/#/#/########.dfxp?v=1&e=#########&t=######_#####&random=1234567890`). |
| 6    | Open the dfxp in a new window. |
| 7    | Save as. |

---
---
# 2. YouTube-To-SRT <span style="color: red; font-size: 2.5em;"></span> <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="fill: red; width: 40px; height: 40px; vertical-align: middle;"><title>YouTube</title><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>

- Install [youtube-dl](https://github.com/ytdl-org/youtube-dl) (available for Windows, Mac and Linux)
- Download subs from the YouTube URL you like e.g. `youtube-dl --all-subs "https://www.youtube.com/watch?v=VHNfvFOBC0A"`
- Subtitles should be downloaded in the same folder where the command was run. E.g. `NameOfTheVideo VHNfvFOBC0A.ca.vtt, NameOfTheVideo VHNfvFOBC0A.tlh.vtt`
- If you are missing a language, check that it's actually available. E.g. `youtube-dl --list-subs "https://www.youtube.com/watch?v=VHNfvFOBC0A"`

> <br>

> **<span style="color: pink;">Install using Snap:</span>**  
> - Install [yt-dlp](https://github.com/yt-dlp/yt-dlp) using Snap:
> ```bash
> sudo snap install yt-dlp
> ```
> - To download subtitles in SRT format from a YouTube URL, use:
> ```bash
>  yt-dlp --skip-download --write-auto-subs --convert-subs srt --sub-lang "en" "https://youtu.be/cVsyJvxX48A" 
> ```
> This command downloads only the subtitles in SRT format.
> - If you want to download the subtitles in VTT format, you can use:
> ```bash
> yt-dlp --skip-download --write-auto-subs --sub-lang "en" "https://youtu.be/cVsyJvxX48A"
> ```
> - To download the video with audio and subtitles, simply omit the --skip-download option:
> ```bash
> yt-dlp --write-auto-subs --sub-lang "en" "https://youtu.be/cVsyJvxX48A"
> ```
>> <span style="color: pink;">Note:</span>
>> If you don't enable subtitles in the YouTube video (captions), then the command will not work as expected. Make sure to enable subtitles before running the command.
> <br>
>
> <br>



## Clone Repo & Run files

- [Get Python](https://www.python.org/downloads/) (tested under Python 2.7, 3.3, and newer). *If you have Mac or Linux, you may skip this step.*

- Clone this repository or [download the ZIP file](https://github.com/isaacbernat/netflix-to-srt/archive/refs/heads/master.zip).

```bash
git clone https://github.com/isaacbernat/netflix-to-srt.git
```
- Navigate to the project directory and run the script using the terminal:
```bash
cd netflix-to-srt
```
- Run the conversion script with the following command:

```bash 
python3 main.py --input ./samples/vtt_input --output ./samples/srt_output
```
This will convert all .vtt files of the vtt_input folder into .srt format and place them in the srt_output folder.

- If you want to convert .xml files into .srt, use the following command:

```bash
python3 main.py --input ./samples/xml_input --output ./samples/srt_output
```
This will convert all .xml files of the xml_input folder into .srt format and place them in the srt_output folder.

- You will now see all the .srt files in the srt_output folder located under the samples folder.




## TODOs 🐙
- **Javascript/web version:** This would allow users to convert subtitles directly through a browser without needing to install Python or any dependencies.

- **Real tests:** You could create proper unit or integration tests to automate checking whether subtitle conversion works as expected.

- **Create a pip package:** This would simplify installation for users by allowing them to install the script via Python's package manager.

---

## Note 📝
In no way am I encouraging any kind of illegal activity. Please make sure to know your local laws and always seek proper permissions from content owners (e.g. Netflix, YouTube) when necessary. 🚨

## Contribution 🤗
Contributions are always welcome! Feel free to create a Pull Request and add screenshots for each step/method that works best for you. Your help will make this project even better for everyone. 💻✨

Thank you for stopping by and for your support! Every bit of help is greatly appreciated. Let's build something amazing together! 😄🌟
