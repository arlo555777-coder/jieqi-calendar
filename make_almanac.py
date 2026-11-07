# Build almanac.ics (黄历: 宜 / 忌 for every day) with lunar_python.
# Updated by hand: `python make_almanac.py [first_year last_year]` (default: this year and next year).
import datetime as dt
import os
import sys

from lunar_python import Solar

HERE = os.path.dirname(os.path.abspath(__file__))


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


def short(items, n):
    return ' '.join(items[:n]) + (' …' if len(items) > n else '')


def day_event(d):
    l = Solar.fromYmd(d.year, d.month, d.day).getLunar()
    yi, ji = l.getDayYi(), l.getDayJi()
    summary = '宜 %s · 忌 %s' % (short(yi, 4), short(ji, 3))
    desc = '\n'.join([
        '农历 %s年%s月%s（%s年）' % (l.getYearInGanZhi(), l.getMonthInChinese(), l.getDayInChinese(), l.getYearShengXiao()),
        '干支 %s年 %s月 %s日' % (l.getYearInGanZhi(), l.getMonthInGanZhi(), l.getDayInGanZhi()),
        '宜 ' + ' '.join(yi),
        '忌 ' + ' '.join(ji),
        '冲煞 冲%s 煞%s' % (l.getDayChongDesc(), l.getDaySha()),
        '值神 %s　建除 %s' % (l.getDayTianShen(), l.getZhiXing()),
    ])
    ymd = d.strftime('%Y%m%d')
    return ['BEGIN:VEVENT', 'UID:almanac-%s@arlo555777-coder' % ymd, 'DTSTAMP:%sT000000Z' % ymd,
            'DTSTART;VALUE=DATE:' + ymd, 'DTEND;VALUE=DATE:' + (d + dt.timedelta(days=1)).strftime('%Y%m%d'),
            'SUMMARY:' + ics_text(summary), 'DESCRIPTION:' + ics_text(desc), 'TRANSP:TRANSPARENT', 'END:VEVENT']


if __name__ == '__main__':
    year = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).year
    y0, y1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (year, year + 1)
    start, end = dt.date(y0, 1, 1), dt.date(y1, 12, 31)
    L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//arlo555777-coder//almanac//CN', 'CALSCALE:GREGORIAN',
         'METHOD:PUBLISH', 'X-WR-CALNAME:黄历', 'X-WR-TIMEZONE:Asia/Shanghai',
         'X-WR-CALDESC:每日宜忌、农历、干支、冲煞；按传统通书算法（lunar-python）计算，不同黄历版本可能略有出入',
         'REFRESH-INTERVAL;VALUE=DURATION:P1D', 'X-PUBLISHED-TTL:P1D']
    d, n = start, 0
    while d <= end:
        L += day_event(d)
        d += dt.timedelta(days=1)
        n += 1
    L.append('END:VCALENDAR')
    with open(os.path.join(HERE, 'almanac.ics'), 'w', encoding='utf-8', newline='') as f:
        f.write('\r\n'.join(fold(x) for x in L) + '\r\n')
    print('wrote %d days, %s .. %s' % (n, start, end))
