#!/usr/bin/env python3
from openpyxl import load_workbook
import datetime
import warnings
warnings.simplefilter("ignore", UserWarning)
import utility


def makeExcelReport(analysisRes, sysList, resultNum):
    wb = load_workbook(filename='default_report_template.xlsx')
    wsResDet = wb['진단 결과 상세']
    wsResSum = wb['진단 결과 요약']

    wsResDet['D2'] = "{}-{}".format(sysList['osType'], resultNum)
    wsResDet['D3'] = sysList['hostname']
    wsResDet['I3'] = "{} {}".format(sysList['osName'], sysList['osVersion'])
    wsResDet['I4'] = sysList['osType']

    for row in wsResDet['C6':'C80']:
        cellRes = wsResDet.cell(row=row[0].row, column=7)
        cellCon = wsResDet.cell(row=row[0].row, column=9)
        if cellRes.value is None and row[0].value is not None:
            cellRes.value = 'N/A'
        for i in range(0, len(analysisRes)):
            if row[0].value == analysisRes[i][0]:
                cellRes.value = analysisRes[i][1]
                cellCon.value = utility.mergeExeclData(analysisRes[i][2])

    for row in wsResSum['C5':'C79']:
        cellSum = wsResSum.cell(row=row[0].row, column=6)
        if cellSum.value is None and row[0].value is not None:
            cellSum.value = 'N/A'
        for i in range(0, len(analysisRes)):
            if row[0].value == analysisRes[i][0]:
                cellSum.value = analysisRes[i][1]

    dt = datetime.datetime.now()
    fileName = ''.join("result_report_{}_{}_{}.xlsx".format(sysList['osName'],
                                                            sysList['hostname'],
                                                            dt.strftime("%Y%m%d%H%M%S")))
    wb.save(filename=fileName)