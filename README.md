# Canvas Notes Video Downloader 

Automates the process of opening a page of notes from [my university's canvas site](webcourses.ucf.edu), finding embedded videos, changing the resolution, and downloading them with a descriptive filename

## Motivations

I wrote this tool to save myself time by automating a repetitive task I had to do over and over. At the time of writing, I am graduating college and have been archiving course content for my own use after graduation. However, I probably spent more time making this than I will save... 🤷‍♂️

## Dependencies

The [Chrome Webdriver](https://chromedriver.chromium.org/) must be installed, as well as [selenium](https://pypi.org/project/selenium/) for python

## Usage
An input file is a file containing urls to canvas pages to download (each on a newline). See `example_input.txt`

```bash
usage: download_videos.py [-h] input_file_path output_directory_path canvas_username canvas_password

Download videos from canvas pages

positional arguments:
  input_file_path       the path to the input file
  output_directory_path the path to the output directory
  canvas_username       your canvas username
  canvas_password       your canvas password

optional arguments:
  -h, --help            show this help message and exit
```

Each video will download as an `.mp4` to the given output directory