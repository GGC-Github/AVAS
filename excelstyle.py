from openpyxl.styles import Font, colors, Alignment, Border, Side
from openpyxl.styles import PatternFill, Color

centerwrapalign = Alignment(horizontal='center', vertical='center', wrap_text=True)
leftwrapalign = Alignment(horizontal='left', vertical='top', wrap_text=True)
centeralign = Alignment(horizontal='center', vertical='center')
leftalign = Alignment(horizontal='left', vertical='top')
fillalign = Alignment(horizontal='fill', vertical='top')

normalfont = Font(name='맑은 고딕', size=10, color=colors.BLACK)
whiteboldfont = Font(name='맑은 고딕', size=10, color=colors.WHITE, bold=True)
greenfont = Font(name='맑은 고딕', size=10, color='009900')
redfont = Font(name='맑은 고딕', size=10, color=colors.RED)
bluefont = Font(name='맑은 고딕', size=10, color=colors.BLUE)
headredfont = Font(name='맑은 고딕', size=16, color=colors.RED, bold=True)

cellbgfill = PatternFill(patternType='solid', fgColor=Color('3F575F'))

thinborder = Border(
    left=Side(border_style="thin", color='FF000000'),
    right=Side(border_style="thin", color='FF000000'),
    bottom=Side(border_style="thin", color='FF000000'),
    top=Side(border_style="thin", color='FF000000')
)
