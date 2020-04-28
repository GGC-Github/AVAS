#!/usr/bin/env python3
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, colors, Border, Side
import datetime
import warnings
warnings.simplefilter("ignore", UserWarning)


def makeExcelReport(analysisRes, sysList, resultNum):
    wb = load_workbook(filename='default_report_template.xlsx')
    wsResDet = wb['진단 결과 상세']
    wsResSum = wb['진단 결과 요약']
    wsResSum.font = Font(name='맑은 고딕', size=10)
    wsResDet.font = Font(name='맑은 고딕', size=10)
    alignment = Alignment(horizontal='center')
    inbox = Border(left=Side(border_style="thin", color='FF000000'),
                   right=Side(border_style="thin", color='FF000000'),
                   bottom=Side(border_style="thin", color='FF000000'))
    loutbox = Border(left=Side(border_style="thick", color='FF000000'),
                     right=Side(border_style="thin", color='FF000000'),
                     bottom=Side(border_style="thin", color='FF000000'))
    routbox = Border(left=Side(border_style="thick", color='FF000000'),
                     right=Side(border_style="thick", color='FF000000'),
                     bottom=Side(border_style="thin", color='FF000000'))

    analysisRes.sort(key=lambda x: x[3][0])
    for cnt in range(0, len(analysisRes)):
        if cnt == len(analysisRes) - 1:
            inbox = Border(left=Side(border_style="thin", color='FF000000'),
                           right=Side(border_style="thin", color='FF000000'),
                           bottom=Side(border_style="thick", color='FF000000'))
            loutbox = Border(left=Side(border_style="thick", color='FF000000'),
                             right=Side(border_style="thin", color='FF000000'),
                             bottom=Side(border_style="thick", color='FF000000'))
            routbox = Border(left=Side(border_style="thick", color='FF000000'),
                             right=Side(border_style="thick", color='FF000000'),
                             bottom=Side(border_style="thick", color='FF000000'))

        wsResSum.cell(row=5 + cnt, column=2).value = analysisRes[cnt][3][0]
        wsResSum.cell(row=5 + cnt, column=2).border = loutbox

        wsResSum.cell(row=5 + cnt, column=3).value = analysisRes[cnt][0]
        wsResSum.cell(row=5 + cnt, column=3).border = inbox

        wsResSum.cell(row=5 + cnt, column=4).value = analysisRes[cnt][3][1]
        wsResSum.cell(row=5 + cnt, column=4).border = inbox

        wsResSum.cell(row=5 + cnt, column=5).alignment = alignment
        wsResSum.cell(row=5 + cnt, column=5).value = int(analysisRes[cnt][3][3])
        wsResSum.cell(row=5 + cnt, column=5).border = inbox

        wsResSum.cell(row=5 + cnt, column=6).alignment = alignment
        if analysisRes[cnt][1] == 'O':
            wsResSum.cell(row=5 + cnt, column=6).value = '양호'
            wsResSum.cell(row=5 + cnt, column=6).font = Font(color='009900')
        elif analysisRes[cnt][1] == 'R':
            wsResSum.cell(row=5 + cnt, column=6).value = '리뷰'
            wsResSum.cell(row=5 + cnt, column=6).font = Font(color=colors.BLUE)
        elif analysisRes[cnt][1] == 'X':
            wsResSum.cell(row=5 + cnt, column=6).value = '취약'
            wsResSum.cell(row=5 + cnt, column=6).font = Font(color=colors.RED)
        wsResSum.cell(row=5 + cnt, column=6).border = routbox

    dt = datetime.datetime.now()
    fileName = ''.join("result_report_{}_{}_{}.xlsx".format(sysList['osName'],
                                                            sysList['hostname'],
                                                            dt.strftime("%Y%m%d%H%M%S")))

    wb.save(filename=fileName)
