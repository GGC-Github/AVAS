from openpyxl.styles import Font, colors, Alignment, Border, Side


centeralign = Alignment(horizontal='center')

normalfont = Font(name='맑은 고딕', size=10, color=colors.BLACK)
greenfont = Font(name='맑은 고딕', size=10, color='009900')
redfont = Font(name='맑은 고딕', size=10, color=colors.RED)
bluefont = Font(name='맑은 고딕', size=10, color=colors.BLUE)
headredfont = Font(name='맑은 고딕', size=16, color=colors.RED, bold=True)

thinborder = Border(left=Side(border_style="thin", color='FF000000'),
                    right=Side(border_style="thin", color='FF000000'),
                    bottom=Side(border_style="thin", color='FF000000'))
