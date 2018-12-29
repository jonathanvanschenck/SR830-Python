import visa, time
import numpy as np
rm = visa.ResourceManager()

class SR830:
	def __init__(self,resourceLoc="GPIB0::8::INSTR"):
		self.inst = rm.open_resource(resourceLoc)
		print("Connected to: ")
		print(self.inst.query("*IDN?"))
		self.sens = {"2nV":"0","5nV":"1","10nV":"2",
					 "20nV":"3","50nV":"4","100nV":"5",
					 "200nV":"6","500nV":"7","1uV":"8",
					 "2uV":"9","5uV":"10","10uV":"11",
					 "20uV":"12","50uV":"13","100uV":"14",
					 "200uV":"15","500uV":"16","1mV":"17",
					 "2mV":"18","5mV":"19","10mV":"20",
					 "20mV":"21","50mV":"22","100mV":"23",
					 "200mV":"24","500mV":"25","1V":"26"}
		self.volt = [0.000000002,0.000000005,0.00000001,
					 0.00000002, 0.00000005, 0.0000001,
					 0.0000002, 0.0000005, 0.000001,
					 0.000002, 0.000005, 0.00001,
					 0.00002, 0.00005, 0.0001,
					 0.0002, 0.0005, 0.001,
					 0.002, 0.005, 0.01,
					 0.02, 0.05, 0.1,
					 0.2, 0.5, 1.0]
		self.rmod = {"High Reserve":"0","Normal":"1","Low Noise":"2"}
		self.oflt = {"10us":"0","30us":"1","100us":"2",
					 "300us":"3","1ms":"4","3ms":"5",
					 "10ms":"6","30ms":"7","100ms":"8",
					 "300ms":"9","1s":"10","3s":"11",
					 "10s":"12","30s":"13","100s":"14",
					 "300s":"15","1ks":"16","3ks":"17",
					 "10ks":"18","30ks":"19"}
		self.time = [0.00001,0.00003,0.0001,0.0003,
					 0.001,0.003,0.01,0.03,0.1,0.3,
					 1.0,3.0,10.0,30.0,100.0,300.0,
					 1000.0,3000.0,10000.0,30000.0]
		#self.setIT()
		#self.setSens()
		self.setSync()
		self.it = self.time[int(self.inst.query("OFLT ?")[:-1])]
		self.v = self.volt[int(self.inst.query("SENS ?")[:-1])]
		
	def setIT(self,name=None,i=10):
		"""
		Integration times are as follows:
		{"10us":"0","30us":"1","100us":"2",
		"300us":"3","1ms":"4","3ms":"5",
		"10ms":"6","30ms":"7","100ms":"8",
		"300ms":"9","1s":"10","3s":"11",
		"10s":"12","30s":"13","100s":"14",
		"300s":"15","1ks":"16","3ks":"17",
		"10ks":"18","30ks":"19"}
		"""
		if name!=None:
			self.inst.write("OFLT "+self.oflt[name])
			time.sleep(0.1)
			self.it = self.time[int(self.inst.query("OFLT ?")[:-1])]
		else:
			self.inst.write("OFLT "+str(int(i)))
			time.sleep(0.1)
			self.it = self.time[i]
	def getIT(self):
		return(list(self.oflt.keys())[int(self.inst.query("OFLT ?")[:-1])])
			
	def setSens(self,name=None,i=11):
		"""
		Sensitivities are as follows:
		{"2nV":"0","5nV":"1","10nV":"2",
		"20nV":"3","50nV":"4","100nV":"5",
		"200nV":"6","500nV":"7","1uV":"8",
		"2uV":"9","5uV":"10","10uV":"11",
		"20uV":"12","50uV":"13","100uV":"14",
		"200uV":"15","500uV":"16","1mV":"17",
		"2mV":"18","5mV":"19","10mV":"20",
		"20mV":"21","50mV":"22","100mV":"23",
		"200mV":"24","500mV":"25","1V":"26"}
		"""
		if name!=None:
			self.inst.write("SENS "+self.sens[name])
			time.sleep(0.1)
			self.v = self.volt[int(self.inst.query("SENS ?")[:-1])]
		else:
			self.inst.write("SENS "+str(int(i)))
			time.sleep(0.1)
			self.v = self.volt[i]
	def getSens(self):
		return(list(self.sens.keys())[int(self.inst.query("SENS ?")[:-1])])
		
	def setSync(self,i=1):
		"""
		Only turn on if frequency is below 200Hz
		0->OFF
		1->ON
		"""
		self.inst.write("SYNC "+str(int(i)))
		time.sleep(0.1)
		if self.getFreq()>200 and int(i)==1:
			print("Synchronous Filter should only be used below 200Hz")
	def getSync(self):
		return(["ON","OFF"][int(self.inst.query("SYNC ?")[:-1])])
	
	def getFreq(self):
		return(float(self.inst.query("FREQ ?")))
		
	def getOut(self,i=3):
		"""
		i=     1     2      3     4
		val=  X(V)  Y(V)    R(V)  phase(Deg)
		"""
		assert i<5 and i>0
		return(float(self.inst.query("OUTP? "+str(i))))
	def getRTh(self):
		return(np.array([float(self.inst.query("OUTP? "+str(3))),float(self.inst.query("OUTP? "+str(4)))]))		
	def getXY(self):
		return(np.array([float(self.inst.query("OUTP? "+str(1))),float(self.inst.query("OUTP? "+str(2)))]))
	
	
	def close(self):
		self.inst.close()
