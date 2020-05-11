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
        fullCode = utility.codeParser(doc['assetCode'], doc['assetSubType'])
        utility.mergeScript(doc, fullCode, getPwd)
    except Exception:
        utility.printCollectUsage(traceback.format_exc())


def analysisMain(resDir = None):
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
                codeMap = getattr(codemapping, sysList['osType'].lower() + key.split('-')[0] + 'codeMap')
                code = codeMap[key][0][0]
                analyze = getattr(codeanalysisFunc, 'analysis' + code)(key, fileList, infoList[key], sysList, codeMap)
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
        parser = argparse.ArgumentParser(
            prog='avas.exe', usage='%(prog)s [ AVAS MOD ] [options]',
            description='Automated Vulnerability Analysis System',
        )

        parser.add_argument(
            'avas_mod',
            metavar='AVAS MOD',
            help='collect [ ... ] or analysis [ ... ]'
        )

        parser.add_argument(
            '--collect-conf', dest='coll_conf', metavar='File',
            help='avas.exe collect --collect-conf C:\\AVAS\\AVAS.yaml'
        )

        parser.add_argument(
            '--result-dir', dest='res_dir', metavar='Dir',
            help='avas.exe analysis --result-dir C:\\AVAS\\inputResult\\'
        )

        args = parser.parse_args()
        if args.avas_mod in 'collect':
            if args.coll_conf is not None:
                collectMain(args.coll_conf)
            else:
                collectMain()
        elif args.avas_mod in 'analysis':
            if args.res_dir is not None:
                analysisMain(args.res_dir)
            else:
                analysisMain()
        else:
            parser.print_help()

    except IndexError:
        utility.printMainUsage()
