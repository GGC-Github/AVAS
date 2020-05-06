#!/usr/bin/env python3
import excelstyle
from openpyxl import load_workbook
import datetime
import warnings
warnings.simplefilter("ignore", UserWarning)


def makeExcelReport(analysisRes, sysList, resultNum):
    dt = datetime.datetime.now()
    wb = load_workbook(filename='default_report_template.xlsx')
    wsResSum = wb['진단 결과 요약']
    totalcnt = 0
    resultcnt = 0

#   자산 정보
    wsResSum['D6'] = sysList['osType']
    wsResSum['D7'] = "{} {}".format(sysList['osName'], sysList['osVersion'])
    wsResSum['D8'] = sysList['hostname']
    wsResSum['D9'] = dt.strftime("%Y-%m-%d %H:%M:%S")

#   진단 현황 분포표 및 그래프
    impdict = {}
    impdict.update({'양호': [int(data[3][3]) for data in analysisRes if data[1] in '양호']})
    impdict.update({'취약': [int(data[3][3]) for data in analysisRes if data[1] in '취약']})
    impdict.update({'리뷰': [int(data[3][3]) for data in analysisRes if data[1] in '리뷰']})

    # 상태 별 결과 분포표
    for cnt, val in zip(range(0, 4), [len(analysisRes), len(impdict['양호']), len(impdict['취약']), len(impdict['리뷰'])]):
        wsResSum.cell(row=19, column=10 + cnt).font = excelstyle.normalfont
        wsResSum.cell(row=19, column=10 + cnt).value = val

    # 중요도 별 결과 분포표
    for colcnt, chkval in zip(range(0, 3), ['양호', '취약', '리뷰']):
        for rowcnt in range(0, 3):
            valcnt = impdict[chkval].count(rowcnt + 1)
            wsResSum.cell(row=29 + rowcnt, column=11 + colcnt).font = excelstyle.normalfont
            wsResSum.cell(row=29 + rowcnt, column=11 + colcnt).value = valcnt
            totalcnt += wsResSum.cell(row=29 + rowcnt, column=10).value * valcnt
            if colcnt == 0:
                resultcnt += wsResSum.cell(row=29 + rowcnt, column=10).value * valcnt
            elif colcnt == 2:
                resultcnt += wsResSum.cell(row=29 + rowcnt, column=10).value * valcnt * 0.5

    # 보안 점수 결과
    wsResSum['D2'] = resultcnt / totalcnt * 100
    wsResSum['D2'].font = excelstyle.headredfont

#   진단 결과 내역
    analysisRes.sort(key=lambda x: x[3][0])
    for cnt in range(0, len(analysisRes)):
        inputdata = [analysisRes[cnt][3][0], analysisRes[cnt][0], analysisRes[cnt][3][1],
                     int(analysisRes[cnt][3][3]), analysisRes[cnt][1]]
        for num, idx in zip([0, 2, 3, 10, 11], range(0, len(inputdata))):
            wsResSum.cell(row=36 + cnt, column=2 + num).font = excelstyle.normalfont
            if num == 10 or num == 11:
                wsResSum.cell(row=36 + cnt, column=2 + num).alignment = excelstyle.centeralign

            if num == 11:
                if inputdata[idx] == '양호':
                    wsResSum.cell(row=36 + cnt, column=2 + num).font = excelstyle.greenfont
                elif inputdata[idx] == '리뷰':
                    wsResSum.cell(row=36 + cnt, column=2 + num).font = excelstyle.bluefont
                elif inputdata[idx] == '취약':
                    wsResSum.cell(row=36 + cnt, column=2 + num).font = excelstyle.redfont

            wsResSum.cell(row=36 + cnt, column=2 + num).border = excelstyle.thinborder
            wsResSum.cell(row=36 + cnt, column=2 + num).value = inputdata[idx]
            if num == 3:
                wsResSum.merge_cells(start_row=36 + cnt, start_column=2 + num, end_row=36 + cnt, end_column=2 + num + 6)
            elif num == 0:
                wsResSum.merge_cells(start_row=36 + cnt, start_column=2 + num, end_row=36 + cnt, end_column=2 + num + 1)

    wsResSum = wb['진단 결과 요약']

    fileName = ''.join("result_report_{}_{}_{}.xlsx".format(sysList['osName'],
                                                            sysList['hostname'],
                                                            dt.strftime("%Y%m%d%H%M%S")))

    wb.save(filename=fileName)
