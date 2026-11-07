# 中国节假日 / 二十四节气 / 黄历 日历订阅

四个独立的订阅日历，可以分别设置颜色（iPhone 只能按日历设颜色，所以宜、忌分成两个）。地址用 GitHub Pages（国内手机实测能连；jsDelivr 在国内手机上连不上）。iPhone：日历 → 添加日历 → 添加订阅日历，粘贴下面的地址。

| 日历 | 订阅地址 | 内容 |
|---|---|---|
| 中国节假日 | `webcal://arlo555777-coder.github.io/jieqi-calendar/holiday.ics` | 每天一条「休 春节」或「班 春节」，2024–2027 |
| 二十四节气 | `webcal://arlo555777-coder.github.io/jieqi-calendar/jieqi.ics` | 24 个节气，2026–2049 |
| 黄历·宜 | `webcal://arlo555777-coder.github.io/jieqi-calendar/almanac-yi.ics` | 每天宜做的事，备注里有农历、干支、冲煞，2026–2028 |
| 黄历·忌 | `webcal://arlo555777-coder.github.io/jieqi-calendar/almanac-ji.ics` | 每天忌做的事，备注同上，2026–2028 |

- iPhone 月视图每条只露出两三个字，所以标题把要紧的放最前面：节假日以「休」「班」开头；宜、忌直接写事项，不带「宜」「忌」字，靠日历颜色区分。
- 节假日（`make_holiday.py`）数据来自 [NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn)（抓取国务院通知），当前覆盖 2024–2027；宜忌（`make_almanac.py`）用 lunar_python 按传统通书算法计算，当前覆盖 2026–2028，不同黄历版本的宜忌可能略有出入。
- `almanac.ics` 是宜忌合在一起的旧版，不再更新。
- 手动更新（每年 11 月国务院发布下一年安排后）：运行 `python make_holiday.py` 和 `python make_almanac.py`，把生成的 holiday.ics、almanac-yi.ics、almanac-ji.ics 提交到仓库，等 GitHub Pages 重新发布（约 1 分钟）。下次：2027 年 11 月。
- 节气用 lunar_python 计算，已与苹果「中国大陆节假日」（2026–2029）和香港天文台数据（2026–2049）逐个核对一致。
