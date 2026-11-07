# 中国节假日 / 二十四节气 / 黄历 日历订阅

三个独立的订阅日历，可以分别设置颜色。地址用 GitHub Pages（国内手机实测能连；jsDelivr 在国内手机上连不上）。iPhone：日历 → 添加日历 → 添加订阅日历，粘贴下面的地址。

| 日历 | 订阅地址 | 内容 |
|---|---|---|
| 中国节假日 | `webcal://arlo555777-coder.github.io/jieqi-calendar/holiday.ics` | 每天一条「假期」或「补班」，2024–2027 |
| 二十四节气 | `webcal://arlo555777-coder.github.io/jieqi-calendar/jieqi.ics` | 24 个节气，2026–2049 |
| 黄历 | `webcal://arlo555777-coder.github.io/jieqi-calendar/almanac.ics` | 每日宜忌、农历、干支、冲煞，2026–2028 |

- 节假日（`make_holiday.py`）数据来自 [NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn)（抓取国务院通知），当前覆盖 2024–2027；黄历（`make_almanac.py`）用 lunar_python 按传统通书算法计算，当前覆盖 2026–2028，不同黄历版本的宜忌可能略有出入。
- 手动更新（每年 11 月国务院发布下一年安排后）：运行 `python make_holiday.py` 和 `python make_almanac.py`，把生成的 holiday.ics、almanac.ics 提交到仓库，等 GitHub Pages 重新发布（约 1 分钟）。下次：2027 年 11 月。
- 节气用 lunar_python 计算，已与苹果「中国大陆节假日」（2026–2029）和香港天文台数据（2026–2049）逐个核对一致。
