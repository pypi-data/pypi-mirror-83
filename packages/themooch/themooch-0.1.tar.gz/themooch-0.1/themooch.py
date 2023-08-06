'''Takes in two datetime objects, returns the length of time in scaramuccis'''
__version__ = "0.1"

def scaramuccis(first, second, roundto=100):
    diff = (second - first)
    seconds = diff.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    scaramuccis = days/10
    return round(scaramuccis, roundto)
