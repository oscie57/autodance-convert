import os

jd16eur = "/storage_usb/usr/save/00050000/101b9800/user/[userid]/JustDance2016/"
jd16usa = "/storage_usb/usr/save/00050000/101b9000/user/[userid]/JustDance2016/"
jd17eur = "/storage_usb/usr/save/00050000/101eaa00/user/[userid]/JustDance2017/"
jd17usa = "/storage_usb/usr/save/00050000/101eb200/user/[userid]/JustDance2017/"
jd18eur = "/storage_usb/usr/save/00050000/10210c00/user/[userid]/JustDance2018/"
jd18usa = "/storage_usb/usr/save/00050000/10211300/user/[userid]/JustDance2018/"

def file_check():
    if "temp" not in os.listdir():
        os.mkdir("temp")
    if "output" not in os.listdir():
        os.mkdir("output")

def get_info():
    ""

if __name__ == '__main__':
    file_check()