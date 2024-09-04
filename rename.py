# /rename.py
import os, dotenv, re, shutil

dotenv.load_dotenv()

TARGET_DIR = os.getenv("TARGET_DIR")
RESTORE_DIR = os.getenv("RESTORE_DIR")
NAMELIST = os.getenv("NAMELIST")

KEEP_ORIGINAL = os.environ.get('KEEP_ORIGINAL', 'True') == 'True'

def getNameList():
    path = NAMELIST
    nameList = []
    with open(path, "r") as f:
        for line in f:
            # explode the line with |
            lineConfig = line.split("|")
            # append the name to the list
            nameList.append(lineConfig)
    return nameList

def getTargetFiles():
    path = TARGET_DIR
    targetFiles = []
    # get all files in the target directory
    for root, dirs, files in os.walk(path):
        for file in files:
            # get file extension
            ext = os.path.splitext(file)[1]
            # check if the file is a video file
            if ext in [".mp4", ".mkv", ".avi"]:
                file = file.replace("\n", "")
                fielpath = os.path.relpath(os.path.join(root, file), path)
            else:
                continue
                
            # append the file to the list
            targetFiles.append(fielpath)
    return targetFiles

def convert2RegexTemplate(template):
    #remove the new line character
    template = template.replace("\n", "")
    # 转义字符串中的特殊正则符号
    escaped_template = re.escape(template)
    
    # 将 {number} 替换为一个捕获组，用于匹配数字
    regex_template = escaped_template.replace(r'\{number\}', r'(?P<number>\d+)')
    
    return regex_template

def renameFiles():
    nameList = getNameList()
    targetFiles = getTargetFiles()

    for renameConfig in nameList:
        pattern = convert2RegexTemplate(renameConfig[1])

        # print(f"Pattern: {pattern}")
        if renameConfig[0] == "BANGUMI":
            dirType = ""
        elif renameConfig[0] == "MOVIE":
            dirType = "Movie/"
        elif renameConfig[0] == "TV":
            dirType = "TV/"
        else :
            dirType = "OTHERS/"

        for file in targetFiles:
            # print(f"File: {file}")
            originalFilePath = f"{TARGET_DIR}/{file}"

            fileWithoutExt = os.path.splitext(file)[0]
            # print(f"Pattern: {pattern}")
            match = re.search(pattern, fileWithoutExt)
            if match:
                extention = os.path.splitext(file)[1]
                number = re.search(r"\d{2}", match.group()).group()
                # print(f"Matched string: {match.group()}")
                # print(f"Extracted number: {number}")

                # replace the number with the new number
                newFileName = renameConfig[2].replace("{number}", number)
                newFileName = newFileName.replace("\n", "")
                print(f"New file name: {newFileName}")

                newFilePath = f"{TARGET_DIR}/{dirType}{newFileName}{extention}"
                print(f"New file path: {newFilePath}")

                # copy the file to the restore directory
                if KEEP_ORIGINAL == True:
                    shutil.copyfile(originalFilePath, newFilePath)
                    print(f"File copied: {file} -> {newFileName}{extention}")
                else :
                    shutil.move(originalFilePath, newFilePath)                    
                    print(f"File renamed: {file} -> {newFileName}{extention}")

                
            # else:
                # print("No match found")
        # print(renameConfig)

renameFiles()