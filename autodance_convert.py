import ftplib
import json
import sys
from pathlib import Path
from typing import Dict, List

import click
import ffmpeg

GAME_ID_MAP = {
    "2016_eur": "101b9800",
    "2016_usa": "101b9000",
    "2017_eur": "101eaa00",
    "2017_usa": "101eb200",
    "2018_eur": "10210c00",
    "2018_usa": "10211300",
}
LOCATION_MAP = {
    "nand": "mlc",
    "usb": "usb",
}

GAME_PATH_BASE = (
    "/storage_{location}/usr/save/00050000/{game_id}/"
    "user/{user_id}/JustDance{year}/"
)

SAVE_DATA = "JDSave_0"
output_dir = Path("./output")

config_file = Path("config.json")
DEFAULT_CONFIG = {
    "address": None,
    "user_id": None,
    "year": None,
    "region": None,
    "location": None,
}


def save_config(config) -> None:
    with config_file.open(mode="w") as f:
        json.dump(config, f, indent=4)


def load_config() -> Dict[str, str]:
    if config_file.exists():
        return json.loads(config_file.read_text())
    return DEFAULT_CONFIG


def files_in_directory(directory: Path) -> List[Path]:
    return [
        file.absolute() for file in list(directory.glob("*")) if file.is_file()
    ]


def download_videos(address: str, game_path: str) -> None:
    click.echo(f"Attempting FTP connection to {address}...")
    try:
        with ftplib.FTP(address, timeout=5) as ftp:
            click.echo(f"Connection to {address} accepted.")
            ftp.login()
            ftp.cwd(game_path)
            for file in ftp.nlst():
                if file == SAVE_DATA:
                    click.echo("Save data skipped.")
                    continue
                with (output_dir / file).open(mode="wb") as f:
                    click.echo(f"Downloading {file}...")
                    ftp.retrbinary(f"RETR {file}", f.write)
    except ftplib.error_perm:
        click.echo(
            "An error occurred trying to download videos. "
            "Did you enter the correct parameters?"
        )
        sys.exit(1)
    except TimeoutError:
        click.echo(f"No FTP connections found at {address}. Exiting...")
        sys.exit(1)


def extract_videos() -> None:
    def extract_video(video: Path) -> None:
        click.echo(f"Extracting {video.name}...")

        with video.open(mode="rb") as f:
            data = f.read()

        name_nullbyte = data.find(0, 188)
        artist_nullbyte = data.find(0, 316)

        name = data[188:name_nullbyte].decode("utf-8")
        artist = data[316:artist_nullbyte].decode("utf-8")

        click.echo(f"{video.name}: {name} - {artist}")
        filename = f"{name} - {artist}.webm"

        output = output_dir.joinpath(filename)
        if output.is_file():
            output.unlink()
        with output.open(mode="xb") as f:
            f.write(data[512460:])

    videos = [
        video
        for video in files_in_directory(output_dir)
        if video.name.startswith("JDSave") and video.suffix == ""
    ]

    if len(videos) == 0:
        click.echo("No videos were found to extract. Exiting...")
        sys.exit(1)

    for video in videos:
        extract_video(video)
        video.unlink()

    click.echo("All videos have been extracted. Ready to convert.")


def convert_videos() -> None:
    def convert_video(video: Path) -> None:
        click.echo(f"Converting {video.name}...")

        output = video.with_suffix(".mp4")
        if output.exists():
            output.unlink()

        stream = ffmpeg.input(str(video))
        stream = ffmpeg.output(stream, str(output))

        try:
            ffmpeg.run(stream, quiet=True)
        except ffmpeg.Error as e:
            click.echo(f"Error converting video: {e.stderr}")

    videos = [
        video
        for video in files_in_directory(output_dir)
        if video.suffix == ".webm"
    ]

    if len(videos) == 0:
        click.echo("No videos were found to convert. Exiting...")
        sys.exit(1)

    for video in videos:
        convert_video(video)
        video.unlink()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main() -> None:
    config = load_config()

    address = click.prompt(
        "Please enter your Wii U's IP address",
        type=str,
        default=config.get("address"),
    )
    user_id = click.prompt(
        "Please enter the ID of the user to get the saves of",
        type=str,
        default=config.get("user_id"),
    )
    year = click.prompt(
        "Please enter your Just Dance game version",
        type=click.Choice(["2016", "2017", "2018"], case_sensitive=False),
        default=config.get("year"),
    )
    region = click.prompt(
        "Please enter your game's region",
        type=click.Choice(["EUR", "USA"], case_sensitive=False),
        default=config.get("region"),
    )
    location = click.prompt(
        "Please enter your game's location",
        type=click.Choice(["NAND", "USB"], case_sensitive=False),
        default=config.get("location"),
    )

    game_id = GAME_ID_MAP[f"{year}_{region.lower()}"]
    internal_location = LOCATION_MAP.get(location.lower())

    path = GAME_PATH_BASE.format(
        location=internal_location,
        game_id=game_id,
        user_id=user_id,
        year=year,
    )

    if not output_dir.is_dir():
        output_dir.mkdir()

    download_videos(address, path)
    extract_videos()
    convert_videos()
    click.echo("All done.")

    config = {
        "address": address,
        "user_id": user_id,
        "year": year,
        "region": region,
        "location": location,
    }
    save_config(config)
    click.echo("Config saved.")


if __name__ == "__main__":
    main()
