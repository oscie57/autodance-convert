# autodance-convert

 A python project to convert Just Dance Wii U Autodances to MP4.

 Special thanks to [this GBAtemp post](https://gbatemp.net/threads/extract-just-dance-autodance-video.493341/) for information on how to do this.

 Some information used from [jdext](https://github.com/yurijmikhalevich/jdext).

 Assistance (really basic) from [Sketch](https://github.com/noahpistilli).

## Setup

In order to use this, you will need a Wii U with custom firmware installed, I recommend using [this guide](https://wiiu.hacks.guide/) and installing Tiramisu/Aroma, either should work for this.

You will also need [FTPiiu_everywhere](https://wiidatabase.de/wii-u-downloads/wii-u-tools/ftpiiu-everywhere/) running.

Make sure you have Python installed, I use 3.9, not sure if anything before that works.

Run `py -m pip install ftputil ffmpeg-python` to install the required packages.

## Running the program

In order to extract your autodances, there are a few things you'll need.

- IP Address | The IP of your Wii U to connect to.
- JD Version | Version of the game to extract from. Valid options are: `2016`, `2017`, `2018`.
- JD Region | Region of the game. Valid options are: `EUR`, `USA`.
- User ID | The User ID to extract the save from. This can be done in many ways. Should be something like `8000000a`.

Once you have all of these, you can run `py convert.py` and follow all of the prompts.
