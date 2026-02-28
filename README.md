# MuseScore Sheet Music Downloader

A parser for downloading sheet music from MuseScore and converting it to PDF. Consists of a Tampermonkey script for collecting image URLs and a FastAPI server for PDF conversion.

## Setup

### 1. Server setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
fastapi dev main.py
```

### 2. Tampermonkey

1. Install [Tampermonkey](https://www.tampermonkey.net/) extension for your browser
2. Create a new script and copy the contents of `PostUrlsFromMuse.js`
3. Save the script

## Usage

1. Launch FastAPI server
2. Open a sheet music page on MuseScore
3. Wait untill script finishes parsing 
4. Enjoy your PDF sheet in project directory! 
