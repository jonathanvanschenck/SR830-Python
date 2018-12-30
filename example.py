import sr830

sr = sr830.SR830()
sr.setIT("10s")#or sr.setIT(i=11)
sr.setSens("1mV")#or sr.setSens(i=17)
sr.time.sleep(10)#Allow time for lock-in signal to stablize after changing IT
print("Finding Signal at: {}Hz".format(sr.getFreq))
for i in range(10):
  res=sr.getRTh()
  print("Signal RMS: {0}V with phase {1} deg".format(res[0],int(res[1])))
  sr.time.sleep(sr.it)
sr.close()
