import datetime
from exerTools import RabinKarp
import matplotlib.pyplot as plt
import numpy as np

f = open('DigitsOfPi', 'r')
strPi = f.read()
f.close()

start_date = datetime.date(year=1996, month=1, day=1)
end_date = datetime.date(year=1996, month=12, day=31)

current_date = start_date

dates = []
datescounter = []

while (current_date <= end_date):
    dates.append(str(current_date)[5:7] + str(current_date)[8:10])
    current_date = current_date + datetime.timedelta(1)

for date in dates:
    number = len(RabinKarp(strPi, date))
    datescounter.append(number)

plt.figure()
plt.stem(dates, datescounter)
plt.show()

maxvalue = max(datescounter)
maxindex = datescounter.index(maxvalue)
print("In 1996, the date with the most occurrences in the first 100000 digits of Pi is %s , it occurs %i times." % (str(start_date + datetime.timedelta(maxindex)),maxvalue)
      )
