# Import required libraries
import os
import ftputil
import ffmpeg

# Declare URLs
jd16eur = "/storage_mlc/usr/save/00050000/101b9800/user/[userid]/JustDance2016/"
jd16usa = "/storage_mlc/usr/save/00050000/101b9000/user/[userid]/JustDance2016/"
jd17eur = "/storage_mlc/usr/save/00050000/101eaa00/user/[userid]/JustDance2017/"
jd17usa = "/storage_mlc/usr/save/00050000/101eb200/user/[userid]/JustDance2017/"
jd18eur = "/storage_mlc/usr/save/00050000/10210c00/user/[userid]/JustDance2018/"
jd18usa = "/storage_mlc/usr/save/00050000/10211300/user/[userid]/JustDance2018/"

# Declare FTP variables
address = input("Enter the Wii U's IP address. Do not include the port.\n -> ")

# Declare other variables
jdversion = input("Enter the Just Dance version. Only include the year. Example: '2018'.\n -> ")
jdregion = input("Enter the region of the game. Example: 'EUR'.\n -> ")
userid = input("Enter the user ID of whom you would like to extract the save. Example: '80000003'.\n -> ")

if jdversion == "2016" and jdregion == "EUR":
    gameurl = jd16eur.replace("[userid]", userid)
elif jdversion == "2016" and jdregion == "USA":
    gameurl = jd16usa.replace("[userid]", userid)
elif jdversion == "2017" and jdregion == "EUR":
    gameurl = jd17eur.replace("[userid]", userid)
elif jdversion == "2017" and jdregion == "USA":
    gameurl = jd17usa.replace("[userid]", userid)
elif jdversion == "2018" and jdregion == "EUR":
    gameurl = jd18eur.replace("[userid]", userid)
elif jdversion == "2018" and jdregion == "USA":
    gameurl = jd18usa.replace("[userid]", userid)
else:
    quit("\nIncorrect value. Are you sure you put in the correct items?")

def file_check():

    if "saves" not in os.listdir():
        os.mkdir("saves")
    if "output" not in os.listdir():
        os.mkdir("output")
    
    if ".gitkeep" in os.listdir('./output'):
        os.remove("./output/.gitkeep")
    if ".gitkeep" in os.listdir('./temp'):
        os.remove("./temp/.gitkeep")

def transfer_saves():

    with ftputil.FTPHost(address, "anonymous", "anonymous") as ftp_host:
        print("\nConnected to Wii U!")

        ftp_host.chdir(gameurl)
        names = ftp_host.listdir(ftp_host.curdir)

        print(f"\nThere are {len(names) - 1} autodances. They may take a while to download, so please be patient.\n")

        for savefile in names:
            print(f" -> Downloading '{savefile}'...")
            ftp_host.download(f"{gameurl}/{savefile}", f"./saves/{savefile}")

        print("\nAll save files have been downloaded.")
    
    print("\nDisconnected from Wii U!")

def extract_saves():

    if len(os.listdir('./saves')) == 0:
        quit("\nThere are no files in the 'saves' folder. No videos were extracted.")
    
    for file in os.listdir('./saves'):
        if file == "JDSave_0" or file == ".gitkeep":
            os.remove(f'./saves/{file}')

    print("\nCleaned 'saves' folder. Ready to extract.")

    for file in os.listdir('./saves'):
        print("")
        
        with open(f"./saves/{file}", "rb") as f:
            buffer = f.read()

        # if buffer[512460] != 0 or buffer[512461] != 0x1A:
        #     print(f"Error with '{file}', skipping...")
        #     continue

        name_nullbyte = buffer.find(0, 188)
        artist_nullbyte = buffer.find(0, 316)

        name = buffer[188:name_nullbyte]
        artist = buffer[316:artist_nullbyte]

        name = name.decode('utf-8')
        artist = artist.decode('utf-8')

        filename = f"{str(name)} - {str(artist)}"

        with open(f"./saves/{filename}.webm", "xb") as o:
            print(f" -> Extracting '{file}'...")
            o.write(buffer[512460:])
            

    print("\nAll videos have been extracted.")

    for file in os.listdir('./saves'):
        if ".webm" not in file:
            os.remove(f'./saves/{file}')

    print("Cleaned 'saves' folder. Ready to convert.")

def convert_videos():

    if len(os.listdir('./saves')) == 0:
        quit("\nThere are no files in the 'saves' folder. No videos were converted.")

    for file in os.listdir('saves'):
        print(f" -> Converting '{file}'...")
        filename = "./output/" + file[:-5]

        ffmpeg.input("./saves/" + file).output(f'{filename}.mp4').global_args('-loglevel', 'quiet').run()

    print("\nAll videos have been converted. Please check the 'output' folder.")

    for file in os.listdir('./saves'):
        os.remove(f'./saves/{file}')

    print("Cleaned 'saves' folder.")

if __name__ == '__main__':
    file_check()
    transfer_saves()
    extract_saves()
    convert_videos()
