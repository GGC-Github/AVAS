#!/usr/bin/env python3
import os
import datetime
import base64
import yaml
import xml.etree.ElementTree as useXmlParser
import codemapping
import re
import operator
import stat

LIBDIR = os.path.join(os.getcwd(), 'lib_script')
SCRIPTDIR = os.path.join(os.getcwd(), 'code_script')

OPS = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt
}


def base64Decode(setString):
    return str(base64.b64decode(setString), encoding='utf-8')


def xmlResultFileParser(resultFile):
    print(resultFile)
    doc = useXmlParser.parse(resultFile)
    root = doc.getroot()
    sysInfo = {
        info.tag: base64Decode(info.text) if info.tag in ['ipList', 'processInfo', 'portInfo', 'serviceInfo']
        else info.text for info in root.find("sysInfo")
    }

    infoCollectList = {}
    fileCollectList = {}

    infoElementList = root.findall("infoElement")
    for infoElement in infoElementList:
        infoCollectList.update({infoElement.attrib['code']:
                                    {data.attrib['name']: base64Decode(data.text)
                                     for data in infoElement if data.tag in 'command'}})

    fileList = root.findall("fileList/fileInfo")
    for fileElement in fileList:
        fileCollectList.update({fileElement.find('filePath').text:
                                    {data.tag: base64Decode(data.text)
                                        if data.tag == 'fileData' else data.text
                                     for data in fileElement
                                     if data.tag != 'filePath'}})

    return fileCollectList, infoCollectList, sysInfo


def readConfig(name):
    document = yaml.load(open(name, 'r', encoding='UTF-8'), Loader=yaml.SafeLoader)
    doc = document['assetInfo']
    print("""
***** Current Configration File Settings *****

TYPE : {}
SUBTYPE : {}
ENV : {}
CODE : {}

**********************************************
""".format(doc['assetType'], doc['assetSubType'], doc['assetEnv'], doc['assetCode']))
    return doc


def codeParser(codeList, subType):
    totalList = []
    for code in codeList:
        reg = re.findall(r'(\w+)-(\w+)', code)
        if len(reg) == 0 or (len(reg) == 1 and '~' in code):
            return None

        if len(reg) == 2:
            listTmp = ["{}-{:02}".format(reg[0][0], x) for x in range(int(reg[0][1]),
                                                                      int(reg[1][1]) + 1)]
            totalList.extend(listTmp)
        elif len(reg) == 1 and reg[0][1].lower() == 'all':
            codemap = getattr(codemapping, subType[0].lower() + reg[0][0] + 'codeMap')
            codecnt = 2 if reg[0][0] == 'U' else 3
            totalList += ["{}-{:0{}}".format(reg[0][0], int(x.split('-')[1]), codecnt) for x in codemap.keys()]
        else:
            if isinstance(code, list):
                totalList.extend(code)
            else:
                totalList.append(code)
    totalList = list(set(totalList))
    totalList.sort()
    return totalList


def readScript(baseFileList, baseDir, codeMap=None):
    fullString = ''
    for baseFile in baseFileList:
        if codeMap is None:
            fullFilePath = os.path.join(baseDir, baseFile)
        else:
            fullFilePath = os.path.join(baseDir, codeMap[baseFile][0][0])
        with open(fullFilePath, 'r', encoding='UTF-8') as f:
            data = ''.join([line for line in f.readlines() if line[0] != '#'])
            fullString += data

    return fullString


def mergeScript(document, code, getPwd):
    dt = datetime.datetime.now()
    assetType = document['assetType'][0]
    assetSubType = document['assetSubType'][0].lower()
    assetEnv = None
    if document['assetEnv'][0] is not None:
        assetEnv = document['assetEnv'][0].lower()
    CODEDIR = os.path.join(SCRIPTDIR, assetType, assetSubType)
    codedeli = list(set([val.split('-')[0] for val in code]))
    codelist = []
    codefunclist = []
    liblist = {
        'windows': ['@echo off\n', 'bat', ['lib_batch_preprocess.inc'], None, ['lib_batch_postprocess.inc']],
        'linux': [
            '#!/bin/sh\n', 'sh', ['lib_shell_preprocess.inc', 'lib_shell_xml.inc', 'lib_shell_encode.inc'],
            ['lib_shell_autostruct.inc'], ['lib_shell_postprocess.inc']
        ]
    }

    for val in codedeli:
        codeMap = getattr(codemapping, assetSubType + val + 'codeMap')
        codedivi = [item for item in code if val in item]
        for key in codedivi:
            codelist.append(codeMap[key][0][0])
            codefunclist.append(codeMap[key][0][1])
    codelist = list(set(codelist))
    codelist.sort()

    if assetSubType == 'windows' or assetEnv == 'windows':
        assetname = 'windows'
    else:
        assetname = 'linux'

    fileheader = liblist[assetname][0]
    fileext = liblist[assetname][1]
    LIBPREFILES = liblist[assetname][2]
    LIBAUTOFILES = liblist[assetname][3]
    LIBPOSTFILE = liblist[assetname][4]

    codeScript = readScript(codelist, CODEDIR)
    libPre = readScript(LIBPREFILES, LIBDIR)
    libPost = readScript(LIBPOSTFILE, LIBDIR)
    libAutoStruct = None
    if LIBAUTOFILES is not None:
        libAutoStruct = readScript(LIBAUTOFILES, LIBDIR)

    scriptFileName = os.path.join(getPwd, "{}_{}.{}".format(document["assetSubType"][0], dt.strftime("%Y%m%d%H%M%S"),
                                                            fileext))
    with open(scriptFileName, 'w', encoding='UTF-8', newline='\n') as newFile:
        newFile.write(fileheader)
        newFile.write(libPre)
        newFile.write(codeScript)
        if LIBAUTOFILES is not None:
            newFile.write(libAutoStruct)
            for funclist in codefunclist:
                newFile.write(funclist + '\n')
        newFile.write(libPost)
    os.chmod(scriptFileName, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


def printCollectUsage(strVal):
    print("""
{}
[Usage]
====================
assetInfo:
    assetType:
        - OS
    assetSubType:
        - LINUX
    assetCode:
        - U-01 ~ U-10
        - U-11 ~ U-20
        - U-21 ~ U-30
""".format(strVal))


def printMainUsage():
    print("""
[Usage]
====================

1. Collect Module Start Options
- avas.exe --collect

2. Analysis Module Start Options
- avas.exe --analysis

====================
""")


def fileStatSetup(setString):
    data = "[ 권한 = {}({}), 소유자 = {}({}), 소유그룹 = {}({}) ]".format(
        setString[0], setString[1], setString[5], setString[6],
        setString[7], setString[8])
    return data


def mergeExeclData(setString):
    fullString = ''
    for key, value in setString.items():
        if '_PS' in key:
            data = ''.join("[ {} 프로세스 상태 ]\n\n".format(key.split('_')[0]))
            data += value
        elif '_PORT' in key:
            data = ''.join("[ {} 포트 상태 ]\n\n".format(key.split('_')[0]))
            data += value
        elif '_SYS' in key:
            data = ''.join("[ {} 서비스 데몬 상태 ]\n\n".format(key.split('_')[0]))
            data += value
        elif 'FILEPERM:' in key:
            data = ''.join("파일명 : {}\n{}".format(key.split('FILEPERM:')[1], value))
        elif 'FILEDATA:' in key:
            data = ''.join("[ 파일명 : {} ]\n\n".format(key.split('FILEDATA:')[1]))
            data += value
        elif 'OS_VERSION' in key:
            data = ''.join("[ {} ]\n\n".format('OS 버전'))
            data += value
        elif 'OS_KERNEL_VERSION' in key:
            data = ''.join("[ {} ]\n\n".format('OS 커널 버전'))
            data += value
        else:
            data = ''.join("{}\n".format(value))

        data += '\n'
        fullString += data

    return fullString
