from calendar import HTMLCalendar
from main_calendar.models import CalendarOrder



class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	def formatday(self, day, orders):
		orders_per_day = orders.filter(start_time__day=day)
		d = ''
		for order in orders_per_day:
			d += f'<li> {order.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	def formatweek(self, theweek, orders):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, orders)
		return f'<tr> {week} </tr>'

	def formatmonth(self, withyear=True):
		orders = CalendarOrder.objects.filter(start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, orders)}\n'
		return cal