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
jdversion = "2018" #input("Enter the Just Dance version. Only include the year. Example: '2018'.\n -> ")
jdregion = "EUR" #input("Enter the region of the game. Example: 'EUR'.\n -> ")
userid = "8000000a" #input("Enter the user ID of whom you would like to extract the save. Example: '80000003'.\n -> ")

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

    if "temp" not in os.listdir():
        os.mkdir("temp")
    if "output" not in os.listdir():
        os.mkdir("output")

def transfer_saves():

    with ftputil.FTPHost(address, "anonymous", "anonymous") as ftp_host:
        print("\nConnected to Wii U!")

        ftp_host.chdir(gameurl)
        names = ftp_host.listdir(ftp_host.curdir)

        print(f"\nThere are {len(names) - 1} autodances. They may take a while to download, so please be patient.\n")

        for savefile in names:
            print(f" -> Downloading {savefile}...")
            ftp_host.download(f"{gameurl}/{savefile}", f"./temp/{savefile}")

        print("\nAll save files have been downloaded.")
    
    print("\nDisconnected from Wii U!")

def extract_saves():

    if len(os.listdir('./temp')) == 0:
        quit("\nThere are no files in the 'temp' folder. No videos were extracted.")
    
    for file in os.listdir('./temp'):
        if file == "JDSave_0" or file == ".gitkeep":
            os.remove(f'./temp/{file}')

    print("\nCleaned 'temp' folder. Ready to extract.")

    for file in os.listdir('./temp'):
        print("")
        
        with open(f"./temp/{file}", "rb") as f:
            buffer = f.read()

        # if buffer[512460] != 0 or buffer[512461] != 0x1A:
        #     print(f"Error with '{file}', skipping...")
        #     continue

        with open(f"./temp/{file}.webm", "xb") as o:
            print(f" -> Extracting {file}...")
            o.write(buffer[512460:])

    print("\nAll videos have been extracted.")

    for file in os.listdir('./temp'):
        if ".webm" not in file:
            os.remove(f'./temp/{file}')

    print("Cleaned 'temp' folder. Ready to convert.")

def convert_videos():

    if len(os.listdir('./temp')) == 0:
        quit("\nThere are no files in the 'temp' folder. No videos were converted.")

    for file in os.listdir('temp'):
        print(f"\n -> Converting '{file}'...")
        filename = "./output/" + file[:-5]

        ffmpeg.input("./temp/" + file).output(f'{filename}.mp4').global_args('-loglevel', 'quiet').run()

    print("\nAll videos have been converted. Please check the 'output' folder.")

    for file in os.listdir('./temp'):
        os.remove(f'./temp/{file}')

    print("Cleaned 'temp' folder.")

if __name__ == '__main__':
    file_check()
    transfer_saves()
    extract_saves()
    convert_videos()
