const { readdir, readFile } = require('fs/promises');
const { resolve, join } = require('path');
const { test, describe } = require('node:test');
const assert = require('node:assert');

const { toSrt } = require('../web/script.js');

const SAMPLES_DIR = resolve(__dirname, '..', 'samples');

describe('toSrt conversion tests', () => {
    test('sample files in samples/ directory', async () => {
        const inputExtensions = new Set(['.xml', '.vtt']);
        const files = await readdir(SAMPLES_DIR);
        const sortedFiles = files.sort();

        for (const inputFile of sortedFiles) {
            const base = inputFile.substring(0, inputFile.lastIndexOf('.'));
            const ext = inputFile.substring(inputFile.lastIndexOf('.')).toLowerCase();

            if (!inputExtensions.has(ext)) continue;
            if (inputFile.includes('ep2')) continue;

            const expectedSrt = join(SAMPLES_DIR, base + '.srt');
            const inputPath = join(SAMPLES_DIR, inputFile);

            const inputContent = await readFile(inputPath, 'utf-8');
            const expectedContent = await readFile(expectedSrt, 'utf-8');
            const generatedContent = toSrt(inputContent, ext, 0);

            assert.equal(generatedContent, expectedContent, `Failed for ${inputFile}`);
        }
    });
});

describe('toSrt delay tests', () => {
    test('delay subdirectory', async () => {
        const delayDir = join(SAMPLES_DIR, 'delay');
        const delayPattern = /^(.+?)_(plus|minus)_(\d+)\.srt$/;
        const files = await readdir(delayDir);
        const sortedFiles = files.sort();

        const delayFiles = sortedFiles.filter(f => delayPattern.test(f));
        assert.ok(delayFiles.length > 0, 'No delay test files found');

        for (const f of delayFiles) {
            const match = f.match(delayPattern);
            assert.ok(match, `Filename "${f}" does not match delay pattern`);

            const [, prefix, sign, delayVal] = match;
            const delayMs = sign === 'plus' ? parseInt(delayVal, 10) : -parseInt(delayVal, 10);

            let inputExt = null;
            for (const ext of ['.vtt', '.xml', '.srt']) {
                try {
                    await readFile(join(delayDir, prefix + ext), 'utf-8');
                    inputExt = ext;
                    break;
                } catch {
                    continue;
                }
            }

            assert.ok(inputExt, `No input file found for prefix "${prefix}" (looked for .vtt, .xml, .srt)`);

            const expectedSrt = join(delayDir, f);
            const inputPath = join(delayDir, prefix + inputExt);

            const inputContent = await readFile(inputPath, 'utf-8');
            const expectedContent = await readFile(expectedSrt, 'utf-8');
            const generatedContent = toSrt(inputContent, inputExt, delayMs);

            assert.equal(generatedContent, expectedContent, `Failed for ${f} with delay ${delayMs}`);
        }
    });
});
