import os
import sys
import json
import traceback
from collections import defaultdict

#参数设置#

#语言片段文件后缀名
packExtension = "json"

#pack语言包文件夹路径(含子文件夹)
packFolderPath = "D:\stable-diffusion-webui\extensions\merge-json\zh_CN"


#参考的语言包json文件的路径
#  可为空
#defaultJSONPath = ""
defaultJSONPath = "D:\stable-diffusion-webui\extensions\stable-diffusion-webui-localization-zh_CN\localizations\zh_CN.json"

#生成新的文件路径，可以指定或空
#  若为空：
#    举例：
#      outJSONPath = "", defaultJSONPath = "D:\stable-diffusion-webui\extensions\stable-diffusion-webui-localization-zh_CN\localizations\zh_CN.json"
#      返回 D:\stable-diffusion-webui\extensions\merge-json\localizations\zh_CN-Merge-zh_CN.json
#  若为空并且defaultJSONPath也为空：
#    举例：
#      outJSONPath = "", defaultJSONPath = "",当前py文件路径："D:\stable-diffusion-webui\extensions\merge-json\merge.py"
#      返回 D:\stable-diffusion-webui\extensions\merge-json\localizations\zh_CN-AutoBuild.json

#outJSONPath = "D:\stable-diffusion-webui\localizations\zh_CN_AutoBuild.json"
outJSONPath = ""

isInsensitive = True
if os.path.normcase('A') == os.path.normcase('a'):
    # case insensitive
    isInsensitive= True
else:
    # case sensitive
    isInsensitive = False

#当前插件路径
#os.path.abspath(__file__)
currentDir = os.getcwd()

if isInsensitive == True:
    packExtension = packExtension.lower()

if len(packFolderPath) == 0:
    print("Error: packFolderPath null. Please check config.")
    exit

if len(outJSONPath) ==0:
    packFolderName = os.path.basename(packFolderPath)
    if len(defaultJSONPath) == 0:
        outJSONPath = currentDir + "\\localizations\\" + packFolderName + "-AutoBuild.json"
    else:
        jsonName = os.path.basename(os.path.splitext(defaultJSONPath)[0])
        outJSONPath = currentDir + "\\localizations\\" + jsonName + "-Merge-" + packFolderName +".json"

def GetFileFromThisRootDir(dir,ext = None,isSubDir = True):
    allfiles = []
    needExtFilter = (ext != None)
    if isSubDir == True:#遍历子文件夹
        for root,dirs,files in os.walk(dir):
            for filespath in files:
                filepath = os.path.join(root, filespath)
                extension = os.path.splitext(filepath)[1][1:]
                if isInsensitive == True:
                    extension = extension.lower()
                #if needExtFilter and extension in ext:
                if needExtFilter and (extension == ext):  # 空字符串用in 判别会有错误
                    allfiles.append(filepath)
                elif not needExtFilter:
                    allfiles.append(filepath)
    else:#不遍历子文件夹
        for files in os.listdir(dir):
            filepath = os.path.join(dir,files)
            if os.path.isfile(filepath):
                # print("是文件！")#如果是文件，则进行后缀提取，再判别
                extension = os.path.splitext(filepath)[1][1:]
                if isInsensitive == True:
                    extension = extension.lower()
                #if needExtFilter and extension in ext:
                if needExtFilter and (extension == ext):  # 空字符串用in 判别会有错误
                    allfiles.append(filepath)
                elif not needExtFilter:
                    allfiles.append(filepath)
            # else:
            #     print("不是文件")

    return allfiles

#合并词典
def merge_dict(d1, d2, isOverwrite, isTip, path):
    dd = defaultdict(list)
    print(path)
    for d in (d1, d2):
        for key, value in d.items():
            if len(key) > 0:
                if key in dd.keys():
                    if isTip:
                        isSame = str(dd[key]) == str(value)
                        print("Duplicate Key{0}{1}:\r\n[Key] {2}".format(" [Same]" if isSame else "", " [Overwrite]" if isOverwrite else " [Ignore]", key))
                        if not isSame:
                            print("[Old] {0}\r\n[New] {1}".format(dd[key], value))

                    if not isOverwrite:
                        continue

                dd[key] = value

    return dict(dd)

pack = {}
overwritePackList = {}
allPack = GetFileFromThisRootDir(packFolderPath, packExtension, True)

#读取原始语言包
if len(defaultJSONPath) > 0:
    if(os.path.exists(defaultJSONPath)):
        print("Loading json file:")
        try:
            with open(defaultJSONPath, "r", encoding="utf8") as file:
                data = file.read()
                pack = merge_dict(pack, json.loads(data), True, True, defaultJSONPath)
        except Exception as result:
            #print(result)
            print(f"Error loading json from {defaultJSONPath}:", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
    else:
        print("Error loading json from {defaultJSONPath}")

print("Updateing...\r\n")

#从pack模板中遍历各个翻译词条
pack["----pack new section----"] = "----以下内容Pack新部分----"
tmpPack = {}
print("Loading pack files:")
for fn in allPack:
    if (isInsensitive == True and fn.lower() == defaultJSONPath.lower()) or (isInsensitive == False and fn == defaultJSONPath):
        continue
    elif (isInsensitive == True and fn.lower().endswith("overwrite." + packExtension)) or (isInsensitive == False and fn.endswith("Overwrite." + packExtension)):
        overwritePackList[fn] = fn
        continue
    try:
        with open(fn, "r", encoding="utf8") as file:
            data = file.read()
            tmpPack = merge_dict(tmpPack, json.loads(data), True, True, fn)
    except Exception as result:
        #print(result)
        print(f"Error loading pack from {fn}:", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)

#覆盖已定义的词条
pack = merge_dict(pack, tmpPack, True, True, "Updateing...\r\n")

#读取强制覆盖语言包
pack["----pack overwrite new section----"] = "----以下内容Pack强制覆盖新部分----"
tmpOverwritePack = {}
print("Loading Overwrite files:")
for fn in overwritePackList:
    if fn is not None:
        try:
            with open(fn, "r", encoding="utf8") as file:
                data = file.read()
                tmpOverwritePack = merge_dict(tmpOverwritePack, json.loads(data), True, True, fn)
        except Exception:
            print(f"Error loading pack from {fn}:", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)

#覆盖已定义的词条
pack = merge_dict(pack, tmpOverwritePack, True, False, "Updateing...\r\n")

#保存
with open(outJSONPath, 'w', encoding='utf-8') as f:
    json.dump(pack, f, ensure_ascii=False, indent=0, sort_keys=False)

print("Finished...")
