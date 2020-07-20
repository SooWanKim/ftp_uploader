from ftplib import FTP, FTP_TLS
import os
import sys


def get_list_local(path, files=[], directories=[]):
    for file in os.listdir(path):
        item = path + file
        if os.path.isdir(item):
            directories.append(item + "\\")
            get_list_local(item + "\\", files, directories)
        else:
            files.append(item)

    return files, directories


def upload_to_ftp(root_dir, upload_path):
    ftp = FTP_TLS()
    ftp.connect(host, port)
    ftp.set_debuglevel(2)
    ftp.login("account_id", "account_password")
    files, directories = get_list_local(upload_path)

    directory_name = os.path.dirname(upload_path)
    directory_name = os.path.basename(directory_name)
    root_dir = root_dir + directory_name + "/"
    directories.insert(0, "")

    for directory in directories:
        path = directory.replace(upload_path, "").replace("\\", "/")
        path = root_dir + path
        # for fName in ftp.nlst():
        #     print(fName)
        # if folderName in ftp.nlst():
        #     continue
        try:
            ftp.mkd(path)
        except:
            continue
        print("Make directory is " + path)

    for file in files:
        path = file.replace(upload_path, "").replace("\\", "/")
        with open(file, "rb") as localfile:
            path = root_dir + path
            ftp.storbinary('STOR ' + path, localfile)
            print("Upload file is " + path)

    print("done upload")


def get_ftp_list():
    ftp = FTP_TLS()
    ftp.connect(host, port)
    ftp.set_debuglevel(2)
    ftp.login("account_id", "account_password")
    files, dir = get_list_ftp(ftp, "/")
    return files, dir


def get_list_ftp(ftp, cwd, files=[], directories=[]):
    data = []
    ftp.cwd(cwd)
    ftp.dir(data.append)
    for item in data:
        pos = item.rfind(" ")
        name = cwd + item[pos + 1:]
        if item.find("<DIR>") > -1:
            directories.append(name)
            get_list_ftp(ftp, name + "/", files, directories)
        else:
            files.append(name)
    return files, directories


# files, dir = get_ftp_list()
# print(files)
# print(dir)

print(sys.argv[2])
# files, dir = get_list_local(sys.argv[2])
# print(files)
# print(dir)

upload_to_ftp(sys.argv[1], sys.argv[2])
