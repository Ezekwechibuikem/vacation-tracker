import "locale";

var d3_locale_zhCN = d3.locale({
  decimal: ".",
  thousands: ",",
  grouping: [3],
  currency: ["¥", ""],
  dateTime: "%x %A %X",
  date: "%Y年%-m月%-d日",
  time: "%H:%M:%S",
  periods: ["上午", "下午"],
  days: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
  shortDays: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
  months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
  shortMonths: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
});
