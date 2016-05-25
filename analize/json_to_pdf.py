import json
import os
import reportlab

from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, PageBreak,\
    Spacer, Frame, PageTemplate, NextPageTemplate, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
arial = os.path.join(folder, 'arial.ttf')
arial_b = os.path.join(folder, 'arialbd.ttf')
pdfmetrics.registerFont(TTFont("Arial", arial))
pdfmetrics.registerFont(TTFont("Arial-Bold", arial_b))

with open('result-2002.json') as f:
    data = f.read()
    json_data = json.loads(data)

doc = SimpleDocTemplate("table.pdf", rightMargin=10, leftMargin=30, topMargin=15, bottomMargin=10, pagesize=(A4[1], A4[0]))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', font='Arial', size=9))
table_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('FONT', (0, 0), (-1, 0), 'Arial-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ])
spacer = (0.5, 7.5)
parts = []
column_gap = 1


FOMC_Y_POSITION = doc.bottomMargin + 31
FOMC_WIDTH = doc.width / 4 - 10
FOMC_HEIGHT = 75

BR = '<br />'

doc.addPageTemplates(
    [
        PageTemplate(
            id='FourCol',
            frames=[
                Frame(
                    30,
                    doc.bottomMargin + 540,
                    90,
                    35,
                    id='header',
                    showBoundary=0
                ),
                Frame(
                    30,
                    doc.bottomMargin + 390,
                    762,
                    162,
                    id='img',
                    showBoundary=0
                ),
                Frame(
                    30,
                    doc.bottomMargin + 350,
                    750,
                    55,
                    id='trade',
                    showBoundary=0
                ),
                Frame(
                    30,
                    doc.bottomMargin + 270,
                    750,
                    90,
                    id='ind_entry',
                    showBoundary=0
                ),
                Frame(
                    30,
                    doc.bottomMargin + 175,
                    doc.width / 4 - 10,
                    doc.height / 6 + 10,
                    id='1',
                    showBoundary=0  # set to 1 for debugging
                ),
                Frame(
                    doc.leftMargin + doc.width / 4 - 7,
                    doc.bottomMargin + 175,
                    doc.width / 4 - 10,
                    doc.height / 6 + 10,
                    id='2',
                    showBoundary=0
                ),
                Frame(
                    doc.leftMargin + doc.width / 2 - 14,
                    doc.bottomMargin + 175,
                    doc.width / 4 - 10,
                    doc.height / 6 + 10,
                    id='3',
                    showBoundary=0
                ),
                Frame(
                    doc.leftMargin + 3 * doc.width / 4 - 21,
                    doc.bottomMargin + 175,
                    doc.width / 4 - 10,
                    doc.height / 6 + 10,
                    id='4',
                    showBoundary=0
                ),
                Frame(
                    30,
                    doc.bottomMargin + 95,
                    750,
                    90,
                    id='ind_exit',
                    showBoundary=0
                ),
                Frame(
                    30,
                    FOMC_Y_POSITION,
                    FOMC_WIDTH,
                    FOMC_HEIGHT,
                    id='fomc_column1',
                    showBoundary=0
                ),
                Frame(
                    30 + doc.width / 4 - 7,
                    FOMC_Y_POSITION,
                    FOMC_WIDTH,
                    FOMC_HEIGHT,
                    id='fomc_column2',
                    showBoundary=0
                ),
                Frame(
                    30 + 2 * doc.width / 4 - 14,
                    FOMC_Y_POSITION,
                    FOMC_WIDTH,
                    FOMC_HEIGHT,
                    id='fomc_column3',
                    showBoundary=0
                ),
                Frame(
                    30 + 3 * doc.width / 4 - 21,
                    FOMC_Y_POSITION,
                    FOMC_WIDTH,
                    FOMC_HEIGHT,
                    id='fomc_column4',
                    showBoundary=0
                ),
                Frame(
                    30,
                    doc.bottomMargin - 5,
                    doc.width,
                    30,
                    id='next_fomc',
                    showBoundary=0
                )
            ],
        )
    ]
)


def fill_spaces(rendered_data, count):
    # used for filling frames with spaces
    if len(rendered_data) < count:
        rendered_data += '<font size=7 color=white>'
        while len(rendered_data) < count:
            rendered_data += '_'
        rendered_data += '</font>'
    return rendered_data


def render_trade_data_to_table(trade_data):
    rendered_data = [['Trade data:'],
                     ['entry', 'exit', 'time', 'netgain', 'netgain per hour', 'Max. Loss', 'MAE', 'MAE bottom',
                      'MAE peak', 'netgain/MAE', 'MFE', 'MFE/MAE', 'percentile(elapsed year) netgain/MAE'],
                     ]
    row_data = [trade_data['entry'], trade_data['exit'], trade_data['time'], trade_data['netgain'],
                trade_data['netgain per hour'], trade_data['Max. Loss'], trade_data['MAE'], trade_data['MAE bottom'],
                trade_data['MAE peak'], trade_data['netgain/MAE'], trade_data['MFE'], trade_data['MFE/MAE'],
                trade_data['percentile(elapsed year) netgain/MAE']]
    rendered_data.append(row_data)

    table = Table(rendered_data, rowHeights=9, hAlign='LEFT', colWidths=(70, 70, 40, 40, 60, 40, 40, 70, 70, 70, 40, 40, 70))

    table.setStyle(table_style)

    return table


def render_indicators_to_table(indicators, table_name):
    rendered_data = [[table_name],
                     ['datetime', 'event name', 'Surv(M)', 'Actual', 'Prior', 'Revised', 'Surprise',
                      'Std Dev', 'percentile', 'Importance', 'Category'],
                     ]
    for entry in sorted(indicators):
        row_data = [indicators[entry]['datetime'], indicators[entry]['event name'],
                    indicators[entry]['Surv(M)'], indicators[entry]['Actual'],
                    indicators[entry]['Prior'], indicators[entry]['Revised'],
                    indicators[entry]['Surprise'], indicators[entry]['Std Dev'],
                    indicators[entry]['percentile'], indicators[entry]['Importance'], indicators[entry]['category']]
        if len(rendered_data) < 8:
            rendered_data.append(row_data)
    while len(rendered_data) < 8:
        rendered_data.append([''])

    table = Table(rendered_data, rowHeights=8, hAlign='LEFT', colWidths=(80, 150, 40, 40, 40, 40, 40, 40, 40, 45, 40))

    table.setStyle(table_style)
    return table


def render_news_item_to_paragraph(news):
    local_parts = []
    rendered_data = '<font size=7 fontname=Arial>'
    if news:
        for news_date in sorted(news):
            if len(rendered_data) < 1000:
                rendered_data += '<font fontname=Arial-Bold>News ' + news_date + ':</font><br />'
                for news_data in sorted(news[news_date], key=lambda x: int(x[8:])):
                    row_data = u'&lt;{}&gt; {}: {} '.format(news[news_date][news_data]['source'],
                                                     news[news_date][news_data]['section'],
                                                     news[news_date][news_data]['title']).strip()
                    rendered_data += row_data + '<br />'
                rendered_data += '<br />'

    rendered_data = fill_spaces(rendered_data, 1450)
    rendered_data += '</font>'

    style = ParagraphStyle(
        name='Normal',
        leading=9,
    )
    local_parts.append(Paragraph(rendered_data, style))
    # we should be in frame #4, force break frame
    local_parts.append(FrameBreak())

    # parts.append(Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1'))
    return local_parts


def render_fomc_to_paragraph(fomc1, fomc2):
    local_parts = []
    style = ParagraphStyle(
        name='Normal',
        leading=9,
    )

    fomc1_title = 'Previous FOMC Meeting 1: ' + fomc1['date'][:10]
    fomc2_title = 'Previous FOMC Meeting 2: ' + fomc2['date'][:10]
    # import ipdb; ipdb.set_trace()
    fomc1_resume = fomc1['Summary'].strip().split('; ')
    fomc2_resume = fomc2['Summary'].strip().split('; ')

    rendered_data = '<font size=7 fontname=Arial>'
    rendered_data += '<font fontname=Arial-Bold>' + fomc2_title + ':</font>' + BR

    for entry in fomc2_resume:
        rendered_data += entry + BR
    rendered_data += BR

    rendered_data = fill_spaces(rendered_data, 380)
    rendered_data += '</font>'
    local_parts.append(Paragraph(rendered_data, style))
    local_parts.append(FrameBreak())

    rendered_data = '<font size=7 fontname=Arial>'
    rendered_data += '<font fontname=Arial-Bold>' + fomc1_title + ':</font>' + BR
    for entry in fomc1_resume:
        # old logic skip Y2K bug. If - just in case - you need to return this behaviour -- uncomment
        # if entry == 'Y2K bug':
        #     continue
        rendered_data += entry + BR
    rendered_data += BR

    rendered_data = fill_spaces(rendered_data, 380)
    rendered_data += '</font>'
    local_parts.append(Paragraph(rendered_data, style))
    local_parts.append(FrameBreak())

    return local_parts

for trade in sorted(json_data, key=lambda x: int(x[5:])):
    # title
    month_year = json_data[trade]['month-year']
    parts.append(Paragraph('<font fontname=Arial-Bold>' + month_year + '</font>', styles["Normal"]))
    parts.append(Spacer(spacer[0], spacer[1]))

    # image
    chart_image = json_data[trade]['chart image']
    parts.append(Image(chart_image, 750, 150, hAlign='LEFT'))
    parts.append(Spacer(spacer[0], spacer[1]))

    # trade data
    rendered_trade_data_table = render_trade_data_to_table(json_data[trade]['trade data'])
    parts.append(rendered_trade_data_table)
    parts.append(Spacer(spacer[0], spacer[1]))

    # indicators on entry
    rendered_indicator_on_entry = render_indicators_to_table(json_data[trade]['indicator_on_entry'],
                                                             'Indicators on entry:')
    parts.append(rendered_indicator_on_entry)
    # parts.append(Spacer(spacer[0], spacer[1]))

    # news
    # rendered_news_items already list
    rendered_news_items = render_news_item_to_paragraph(json_data[trade]['news_items'])
    parts.extend(rendered_news_items)
    parts.append(Spacer(spacer[0], spacer[1]))

    # indicators on exit
    rendered_indicator_on_exit = render_indicators_to_table(json_data[trade]['indicator_on_exit'],
                                                            'Indicators on exit:')
    parts.append(rendered_indicator_on_exit)
    # parts.append(Spacer(spacer[0], spacer[1]))

    # FOMC
    rendered_FOMC = render_fomc_to_paragraph(json_data[trade]['previous_FOMC1'],
                                             json_data[trade]['previous_FOMC2'])
    parts.extend(rendered_FOMC)
    parts.append(Spacer(spacer[0], spacer[1]))

    # Next FOMC
    next_date = json_data[trade]['next_FOMC']['date'][:10]
    rendered_data = [['Next FOMC Meeting: ' + next_date],
                     ]
    next_table = Table(rendered_data, hAlign='LEFT', rowHeights=9)
    next_table.setStyle(table_style)
    parts.append(next_table)

    parts.append(NextPageTemplate('FourCol'))
    parts.append(PageBreak())

doc.build(parts)
