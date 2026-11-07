# Build holiday.ics (中国节假日: 假期 / 补班, one all-day event per day) from NateScarlet/holiday-cn,
# which scrapes the State Council notices every day. Runs in GitHub Actions; standard library only.
import datetime as dt
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = ['https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/{}.json',
           'https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{}.json']


def fetch(year):
    for url in SOURCES:
        try:
            with urllib.request.urlopen(url.format(year), timeout=30) as r:
                return json.load(r)
        except Exception:
            continue
    return None


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


def build(years):
    events = []
    for y in years:
        data = fetch(y)
        if not data:
            continue
        paper = (data.get('papers') or [''])[0]
        days = sorted(data['days'], key=lambda d: d['date'])
        # number the days of each holiday: off days and make-up work days counted separately
        groups = {}
        for d in days:
            groups.setdefault((d['name'], d['isOffDay']), []).append(d['date'])
        for d in days:
            same = groups[(d['name'], d['isOffDay'])]
            kind = '假期' if d['isOffDay'] else '补班'
            summary = '%s %s 第%d天/共%d天' % (d['name'], kind, same.index(d['date']) + 1, len(same))
            events.append((d['date'], summary, paper, d['isOffDay']))
    return events


def write(events, path):
    L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//arlo555777-coder//china-holiday//CN', 'CALSCALE:GREGORIAN',
         'METHOD:PUBLISH', 'X-WR-CALNAME:中国节假日', 'X-WR-TIMEZONE:Asia/Shanghai',
         'X-WR-CALDESC:中国法定节假日放假和补班安排，每天自动同步国务院通知',
         'REFRESH-INTERVAL;VALUE=DURATION:P1D', 'X-PUBLISHED-TTL:P1D']
    for date, summary, paper, off in events:
        d = dt.date.fromisoformat(date)
        ymd = d.strftime('%Y%m%d')
        L += ['BEGIN:VEVENT', 'UID:holiday-%s@arlo555777-coder' % ymd,
              'DTSTAMP:%sT000000Z' % ymd,                      # fixed, so the file only changes when the data does
              'DTSTART;VALUE=DATE:' + ymd,
              'DTEND;VALUE=DATE:' + (d + dt.timedelta(days=1)).strftime('%Y%m%d'),
              'SUMMARY:' + ics_text(summary)]
        if paper:
            L.append('DESCRIPTION:' + ics_text('放假通知：' + paper))
        L += ['TRANSP:TRANSPARENT', 'END:VEVENT']          # never mark the day as busy
    L.append('END:VCALENDAR')
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write('\r\n'.join(fold(l) for l in L) + '\r\n')


if __name__ == '__main__':
    this_year = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).year
    ev = build(range(this_year - 2, this_year + 2))
    if not ev:
        raise SystemExit('no data fetched - keep the old file')
    write(ev, os.path.join(HERE, 'holiday.ics'))
    print('wrote %d days, %s .. %s' % (len(ev), ev[0][0], ev[-1][0]))
