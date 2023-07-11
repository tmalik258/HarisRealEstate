from django import template

register = template.Library()

@register.filter
def int_word (value):
	if value >= 1000000000:
		return f'{round(value/1000000000, 2)} arab'

	elif value >= 10000000:
		# if value < 10000000:
		return f'{round(value/10000000, 2)} crore'
		# else:
		# 	return f'{round(value/1000000, 2)} crores'

	elif value >= 100000:
		# if value < 1000000:
		return f'{round(value/100000, 2)} lakh'
		# else:
		# 	return f'{round(value/100000, 2)} lakhs'

	elif value >= 10000:
		return f'{round(value/10000, 2)} thousand'

	else:
		return value