document.getElementById('convertButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const output = document.getElementById('output');

    if (fileInput.files.length === 0) {
        output.textContent = 'Please select a valid XML, VTT or SRT file.';
        return;
    }

    for (let i = 0; i < fileInput.files.length; i++) {
        const file = fileInput.files[i];
        const reader = new FileReader();

        reader.onload = function(event) {
            const xmlText = event.target.result;
            const srtText = toSrt(xmlText, file.name.slice(-4), 0);
            output.textContent += srtText + "\n\n";

            // Create a Blob for the SRT text
            const blob = new Blob([srtText], { type: 'text/srt' });
            const url = URL.createObjectURL(blob);

            // Create a download link
            const a = document.createElement('a');
            a.href = url;
            a.download = file.name.replace(/\.[^/.]+$/, "") + ".srt"; // Append .srt to the original filename
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url); // Clean up the URL object
        };

        reader.readAsText(file);
    }
});

// Function to add leading zeros
function leadingZeros(value, digits = 2) {
    value = '000000' + String(value);
    return value.slice(-digits);
}

// Convert raw time to SRT format
function convertTime(rawTime) {
    if (parseInt(rawTime) === 0) {
        return '00:00:00,000';
    }

    let ms = '000';
    if (rawTime.length > 4) {
        ms = leadingZeros(parseInt(rawTime.slice(0, -4)) % 1000, 3);
    }
    const timeInSeconds = rawTime.length > 7 ? parseInt(rawTime.slice(0, -7)) : 0;
    const second = leadingZeros(timeInSeconds % 60);
    const minute = leadingZeros(Math.floor(timeInSeconds / 60) % 60);
    const hour = leadingZeros(Math.floor(timeInSeconds / 3600));
    return `${hour}:${minute}:${second},${ms}`;
}

function xmlIdDisplayAlignBefore(text) {
    /*
    displayAlign="before" means the current sub will be displayed on top.
    That is and not at bottom. We check what's the xml:id associated to it
    to have an {\an8} position tag in the output file.
    */
    const alignBeforeRe = /<region.*tts:displayAlign="before".*xml:id="(.*)"/;
    const match = alignBeforeRe.exec(text);
    return match && match[1];
}

function xmlGetCursiveStyleIds(text) {
    const styleSection = text.match(/<styling>([\s\S]*?)<\/styling>/);
    if (!styleSection) {
        return [];
    }
    const styleIdsRe = /<style.* tts:fontStyle="italic".* xml:id=\"([a-zA-Z0-9_.]+)\"/g;
    const matches = [];
    let match;
    while ((match = styleIdsRe.exec(styleSection[0])) !== null) {
        matches.push(match[1]);
    }
    return matches;
}

function xmlCleanupSpansStart(spanIdRe, cursiveIds, text) {
    const hasCursive = [];
    const spanStartTags = text.match(spanIdRe);
    if (spanStartTags) {
        for (let i = 0; i < spanStartTags.length; i++) {
            const s = spanStartTags[i];
            hasCursive.push(cursiveIds.includes(s[1]) ? '<i>' : '');

            let maxSplit = 1; // javascript split has different optionals than Python!
            let result = text.split(s).slice(0, maxSplit); // +1 to include the remainder
            result.push(text.split(s).slice(maxSplit).join(s)); // Join the remainder

            text = hasCursive[hasCursive.length - 1] + result.join('');
        }
    }
    return [text, hasCursive];
}

function xmlCleanupSpansEnd(spanEndRe, text, hasCursive) {
    const spanEndTags = text.match(spanEndRe);
    if (spanEndTags) {
        for (let i = 0; i < spanEndTags.length; i++) {
            const s = spanEndTags[i];
            const cursive = hasCursive[i] ? '</i>' : '';

            let maxSplit = 1; // javascript split has different optionals than Python!
            let result = text.split(s).slice(0, maxSplit); // +1 to include the remainder
            result.push(text.split(s).slice(maxSplit).join(s)); // Join the remainder

            text = result.join(cursive);
        }
    }
    return text;
}

function toSrt(text, extension, delayMs) {
    if (extension.toLowerCase() === '.xml') {
        text = xmlToSrt(text);
    } else if (extension.toLowerCase() === '.vtt') {
        text = vttToSrt(text);
    }
    return shiftSrtTimestamp(text, delayMs);
}

function shiftSrtTimestamp(text, delayMs = 0) {
    if (!delayMs) {
        return text;
    }

    function shiftTime(timeStr, shift) {
        let [h, m, sMs] = timeStr.split(":");
        let [s, ms] = sMs.split(",");
        let totalMs = parseInt(h) * 3600000 + parseInt(m) * 60000 + parseInt(s) * 1000 + parseInt(ms);
        let newMs = totalMs + shift;

        h = Math.floor(newMs / 3600000); newMs %= 3600000;
        m = Math.floor(newMs / 60000); newMs %= 60000;
        s = Math.floor(newMs / 1000); ms = newMs % 1000;
        return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
    }

    function replaceTimestamp(match) {
        const start = shiftTime(match[1], delayMs);
        const end = shiftTime(match[2], delayMs);
        return (start && end) ? `${start} --> ${end}` : match[0];
    }

    const timestampRegex = /(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})/g;
    return text.replace(timestampRegex, replaceTimestamp);
}

function convertVttTime(line) {
    let times = line.replace(".", ",").split(" --> ");
    if (times[0].length === 9) {
        times = ["00:" + times[0], times[1]];
    }
    return `${times[0]} --> ${times[1].split(" ")[0]}`;
}

function vttToSrt(text) {
    if (!text.startsWith("\ufeffWEBVTT") && !text.startsWith("WEBVTT")) {
        throw new Error(".vtt format must start with WEBVTT, wrong file?");
    }
    const styles = getVttStyles(text);
    const styleTagRe = /<c\.(.*)>(.*)<\/c>/;

    const lines = [];
    let currentSubLine = [];
    text.split("\n").forEach((line) => {
        if (currentSubLine.length) {
            if (line) {
                const styleTag = line.match(styleTagRe);
                if (styleTag) {
                    line = styleTag[2];  // line is just the text part
                    const color = styles[styleTag[1].split(".")[0]];
                    if (color) {
                        line = `<font color="${color}">${line}</font>`;
                    }
                }
                currentSubLine.push(line);
            } else {
                lines.push(currentSubLine.join("\n") + "\n\n");
                currentSubLine = [];
            }
        } else if (line.includes(" --> ")) {
            currentSubLine = [convertVttTime(line)];
        }
    });
    if (currentSubLine.length) {
        lines.push(currentSubLine.join("\n"));
    }

    return lines.map((l, i) => `${i + 1}\n${l}`).join("");
}

function getVttStyles(text) {  // just using it for color ATM
    const styles = {};
    const lines = text.split("\n");
    let n = 0;
    const styleNameRe = /::cue\(\.(.*)\).*/;
    const colorRe = /.*color: (\#.*);/;
    while (n < lines.length) {  // not efficient to go through all text, but it's ok
        const styleName = lines[n].match(styleNameRe);
        if (styleName && styleName[1]) {
            const name = styleName[1];
            const color = lines[n + 1].match(colorRe);
            if (color && color[1]) {
                styles[name] = color[1];
            }
        }
        n++;
    }
    return styles;
}

function xmlToSrt(text) {
    function appendSubs(start, end, prevContent, formatTime) {
        subs.push({
            start_time: formatTime ? convertTime(start) : start,
            end_time: formatTime ? convertTime(end) : end,
            content: prevContent.join("\n"),
        });
    }

    const displayAlignBefore = xmlIdDisplayAlignBefore(text);
    const beginRe = /(?=.*begin=)\s*<p\s(?=.*>)/;
    const subLines = text.split("\n").filter(line => beginRe.test(line));
    const subs = [];
    let prevTime = { start: 0, end: 0 };
    let prevContent = [];
    let start = '';
    let end = '';
    const startRe = /begin="([0-9:.]*)/;
    const endRe = /end="([0-9:.]*)/;
    const contentRe = />.*<\/p>/;

    const cursiveIds = xmlGetCursiveStyleIds(text);
    const spanIdRe = /(<span style="([a-zA-Z0-9_.]+)">)+/;
    const spanEndRe = /(<\/span>)+/;
    const brRe = /(<br\s*\/?>)+/;
    let fmtT = true;

    for (let s of subLines) {
        const [cleanedString, hasCursive] = xmlCleanupSpansStart(spanIdRe, cursiveIds, s);
        s = cleanedString;

        const stringRegionRe = new RegExp(`<p(.*region="${displayAlignBefore}".*")>(.*)</p>`);
        if (!s) {
            continue;
        }
        
        s = s.replace(stringRegionRe, `<p$1>{\\an8}$2</p>`);
        const contentMatch = s.match(contentRe);
        let content = contentMatch ? contentMatch[0].slice(1, -4) : '';

        const brTags = content.match(brRe);
        if (brTags) {
            content = content.split(brTags[0]).join("\n");
        }

        content = xmlCleanupSpansEnd(spanEndRe, content, hasCursive);

        const prevStart = prevTime.start;
        start = s.match(startRe)[1];
        end = s.match(endRe)[1];
        if (start.split(":").length > 1) {
            fmtT = false;
            start = start.replace(".", ",");
            end = end.replace(".", ",");
        }
        if ((prevStart === start && prevTime.end === end) || !prevStart) {
            prevTime = { start: start, end: end };
            prevContent.push(content);
            continue;
        }
        appendSubs(prevTime.start, prevTime.end, prevContent, fmtT);
        prevTime = { start: start, end: end };
        prevContent = [content];
    }
    appendSubs(start, end, prevContent, fmtT);

    const lines = subs.map((sub, index) => `${index + 1}\n${sub.start_time} --> ${sub.end_time}\n${sub.content}\n`);
    return lines.join("\n");
}
