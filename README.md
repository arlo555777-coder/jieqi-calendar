# 中国节假日 / 二十四节气 日历订阅

两个独立的订阅日历，可以分别设置颜色。iPhone：日历 → 添加日历 → 添加订阅日历，粘贴下面的地址。

| 日历 | 订阅地址 | 内容 |
|---|---|---|
| 中国节假日 | `webcal://cdn.jsdelivr.net/gh/arlo555777-coder/jieqi-calendar@main/holiday.ics` | 每天一条「假期」或「补班」，近三年 + 已公布的下一年 |
| 二十四节气 | `webcal://cdn.jsdelivr.net/gh/arlo555777-coder/jieqi-calendar@main/jieqi.ics` | 24 个节气，2026–2049 |

- 节假日每天北京时间 09:00 由 GitHub Actions 自动更新（`make_holiday.py`），数据来自 [NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn)（每天抓取国务院通知）。
- 节气用 lunar_python 计算，已与苹果「中国大陆节假日」（2026–2029）和香港天文台数据（2026–2049）逐个核对一致。
