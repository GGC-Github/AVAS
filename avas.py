#!/usr/bin/env python3

import os
import argparse
import traceback
import utility
import codemapping
import codeanalysisFunc
import excelutility


def collectMain(getFile = None):
    print('[Start Collect Module]')
    getPwd = os.getcwd()
    if getFile is None:
        fileName = 'AVAS.yaml'
        fullPath = os.path.join(getPwd, fileName)
    else:
        fullPath = getFile
    try:
        print('\nConfiguratin File Path : ' + fullPath)
        doc = utility.readConfig(fullPath)
        fullCode = utility.codeParser(doc['assetCode'])
        utility.mergeScript(doc, fullCode, getPwd)
    except Exception:
        utility.printCollectUsage(traceback.format_exc())


def analysisMain(resDir):
    try:
        print('[ Start Analysis Module ]\n')
        if resDir is None:
            fullPath = os.path.join(os.getcwd(), 'inputResult')
        else:
            fullPath = resDir

        print('Input Result Collection XML File Directory : ' + fullPath + '\n')
        fullFileList = os.listdir(fullPath)
        print('[ Result File List ]\n')
        resultNum = 1
        for resultFile in fullFileList:
            if 'README.md' == resultFile:
                continue
            fileList, infoList, sysList = utility.xmlResultFileParser(
                os.path.join(fullPath, resultFile))
            print('##### Result xml File Parsing Success!')
            analysisRes = []
            for key in sorted(infoList.keys()):
                codeMap = getattr(codemapping, sysList['osType'].lower() + key[0]
                                  + 'codeMap')
                code = codeMap[key][0]
                analyze = getattr(codeanalysisFunc, 'analysis' + code)(key, fileList,
                                                                 infoList[key], sysList)
                analysisRes.append(analyze.analysisFunc())

            print('##### Total Item Analysis Success!')
            excelutility.makeExcelReport(analysisRes, sysList, resultNum)

            print('##### Final Result Report Successfully Created!\n')
            resultNum += 1

        print('[ End Analysis Module ]')

    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Automated Vulnerability Analysis System',
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('AVAS MOD',
                            help='사용하고자 하는 모드를 선택하세요\n'
                                 'Usage - avas.exe collect ...\n'
                                 '        avas.exe analysis ...')

        parser.add_argument('--collect-conf', dest='coll_conf', metavar='Collect config file',
                            help='수집 설정 파일 위치를 절대 경로로 지정하세요\n'
                                 'Usage - avas.exe collect --collect-conf D:\\AVAS\\AVAS.yaml\n'
                                 'Default : 현재 디렉터리 위치/AVAS.yaml')
        parser.add_argument('--result-dir', dest='res_dir', metavar='Directory containing result xml file',
                            help='수집 결과 xml 파일 전체를 넣어놓은 디렉터리의 절대 경로로 지정하세요\n'
                                 'Usage - avas.exe analysis --result-dir D:\\AVAS\\inputResult\n'
                                 'Default : 현재 디렉터리 위치\\inputResult\\ \n')

        args = parser.parse_args()
        if args.mod in 'collect':
            if args.coll_conf is not None:
                collectMain(args.coll_conf)
            else:
                collectMain()
        elif args.mod in 'analysis':
            if args.res_dir is not None:
                analysisMain(args.res_dir)
            else:
                analysisMain()

    except IndexError:
        utility.printMainUsage()