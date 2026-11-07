# Build the 黄历 calendars with lunar_python: almanac-yi.ics (宜) and almanac-ji.ics (忌), one all-day event per day.
# 宜 and 忌 are two calendars so iPhone can give them two colors (iOS colors by calendar, not by event).
# The iPhone month view shows only ~3 characters, so the title is just the list of items (first item visible),
# without a 宜 / 忌 prefix - the calendar color tells them apart. The notes carry the full almanac.
# Updated by hand: `python make_almanac.py [first_year last_year]` (default: this year and next year).
import datetime as dt
import os
import sys

from lunar_python import Solar

HERE = os.path.dirname(os.path.abspath(__file__))
CALS = [  # file, uid tag, calendar name, which list, suggested default color (Apple hex, RFC 7986 CSS name)
    ('almanac-yi.ics', 'yi', '黄历·宜', 'yi', '#FFCC00', 'gold'),
    ('almanac-ji.ics', 'ji', '黄历·忌', 'ji', '#8E8E93', 'gray'),
]


def ics_text(s):
    return s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\n', '\\n')


def fold(line):
    # RFC 5545: lines longer than 75 octets are folded with CRLF + space
    out, cur = [], b''
    for ch in line:
        b = ch.encode('utf-8')
        if len(cur) + len(b) > 75:
            out.append(cur.decode('utf-8'))
            cur = b' '
        cur += b
    out.append(cur.decode('utf-8'))
    return '\r\n'.join(out)


def day_info(d):
    l = Solar.fromYmd(d.year, d.month, d.day).getLunar()
    yi, ji = l.getDayYi(), l.getDayJi()
    desc = '\n'.join([
        '农历 %s年%s月%s（%s年）' % (l.getYearInGanZhi(), l.getMonthInChinese(), l.getDayInChinese(), l.getYearShengXiao()),
        '干支 %s年 %s月 %s日' % (l.getYearInGanZhi(), l.getMonthInGanZhi(), l.getDayInGanZhi()),
        '宜 ' + ' '.join(yi),
        '忌 ' + ' '.join(ji),
        '冲煞 冲%s 煞%s' % (l.getDayChongDesc(), l.getDaySha()),
        '值神 %s　建除 %s' % (l.getDayTianShen(), l.getZhiXing()),
    ])
    return {'yi': yi, 'ji': ji}, desc


def event(d, tag, items, desc):
    ymd = d.strftime('%Y%m%d')
    return ['BEGIN:VEVENT', 'UID:almanac-%s-%s@arlo555777-coder' % (tag, ymd), 'DTSTAMP:%sT000000Z' % ymd,
            'DTSTART;VALUE=DATE:' + ymd, 'DTEND;VALUE=DATE:' + (d + dt.timedelta(days=1)).strftime('%Y%m%d'),
            'SUMMARY:' + ics_text(' '.join(items)), 'DESCRIPTION:' + ics_text(desc),
            'TRANSP:TRANSPARENT', 'END:VEVENT']


if __name__ == '__main__':
    year = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).year
    y0, y1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (year, year + 1)
    start, end = dt.date(y0, 1, 1), dt.date(y1, 12, 31)
    days = []
    d = start
    while d <= end:
        days.append((d,) + day_info(d))
        d += dt.timedelta(days=1)
    for fname, tag, name, key, apple_color, css_color in CALS:
        L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//arlo555777-coder//almanac-%s//CN' % tag, 'CALSCALE:GREGORIAN',
             'METHOD:PUBLISH', 'X-WR-CALNAME:' + name, 'X-WR-TIMEZONE:Asia/Shanghai',
             'X-APPLE-CALENDAR-COLOR:' + apple_color, 'COLOR:' + css_color,
             'X-WR-CALDESC:每日%s；按传统通书算法（lunar-python）计算，不同黄历版本可能略有出入' % name[-1],
             'REFRESH-INTERVAL;VALUE=DURATION:P1D', 'X-PUBLISHED-TTL:P1D']
        for day, lists, desc in days:
            L += event(day, tag, lists[key], desc)
        L.append('END:VCALENDAR')
        with open(os.path.join(HERE, fname), 'w', encoding='utf-8', newline='') as f:
            f.write('\r\n'.join(fold(x) for x in L) + '\r\n')
        print('%s: %d days, %s .. %s' % (fname, len(days), start, end))
