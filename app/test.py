from datetime import datetime
import time

x = 1000000000

print(type(time.time()))
def lastSeen(last):

	current = int(time.time())

	t = current-last

	if t/60<1:

		message = 'few seconds ago'

	elif t/3600<1:

		message = '{} mins ago'.format(t//60)

	elif t/86400<1:

		message = '{} hours ago'.format(t//3600)

	elif t/604800<1:

		message = '{} days ago'.format(t//86400)

	elif t/2592000<1:

		message = '{} weeks ago'.format(t//604800)

	elif t/31104000<1:

		message = '{} months ago'.format(t//259200)

	else:

		message = '{} years ago'.format(t//31104000)
	
	return message

lastSeen(x)


# def last_seen(last):

# 	current = str(datetime.now()).split()

# 	year_current = int(current[0].split('-')[0])

# 	year_last = int(last[0].split('-')[0])

# 	month_current = int(current[0].split('-')[1])

# 	month_last = int(last[0].split('-')[1])

# 	date_current = int(current[0].split('-')[2])

# 	date_last = int(last[0].split('-')[2])

# 	hour_current = int(current[1].split(':')[0])

# 	hour_last = int(last[1].split(':')[0])

# 	minute_current = int(current[1].split(':')[1])

# 	minute_last = int(last[1].split(':')[1])



# 	if year_current - year_last!=0:
		
# 		return (year_current-year_last, 'year')

# 	elif month_current-month_last!=0:

# 		return (month_current-month_last, 'month')

# 	elif date_current-date_last!=0:

# 		return  (date_current-date_last, 'date')

# 	elif hour_current-hour_last!=0:

# 		return (hour_current-hour_last, 'hour')

# 	elif minute_current-minute_last!=0:

# 		return (minute_current-minute_last, 'minute')

# 	else:

# 		return (0, 'seconds')


# print(last_seen(y))