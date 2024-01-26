# autodance-convert

A python project to convert Just Dance Wii U Autodances to MP4.

Special thanks to [this GBAtemp post](https://gbatemp.net/threads/extract-just-dance-autodance-video.493341/) for information on how to do this.

Some information used from [jdext](https://github.com/yurijmikhalevich/jdext).

Assistance (really basic) from [Sketch](https://github.com/noahpistilli).

## Setup

In order to use this, you will need a Wii U with custom firmware installed. I recommend following https://wiiu.hacks.guide/ and installing Tiramisu or Aroma, either should work for this.

You will also need an FTP server running on your Wii U. If you have Tiramisu, you may use [FTPiiU Everywhere](https://wiidatabase.de/wii-u-downloads/wii-u-tools/ftpiiu-everywhere/). If you have Aroma, you may use the [FTPiiU plugin](https://wiidatabase.de/wii-u-downloads/module-und-plugins/ftpiiu-plugin/).

Be sure you have Python installed, Python 3.9+ is supported.

Run `python -r requirements.txt` to install the required packages.

## Running the program

In order to extract your autodances, there are a few things you'll need:

- IP address of the Wii U to connect to [e.g. `192.168.0.125`]
- ID of the user to get the videos from [e.g. `8000000a`]
- version of the game to extract from
    - valid options: `2016`, `2017`, `2018`
- region of the game 
    - valid options: `EUR`, `USA`
- location of the game
    - valid options: `NAND`, `USB`

Once you meet all the requirements, you can run the following command and follow the on-screen prompts:

```
python autodance_convert.py
```
