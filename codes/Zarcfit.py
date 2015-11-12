import numpy as np

def RplusCPEfun(Rx, Qx, px, frequency):
	out = np.zeros_like(frequency, dtype=np.complex128)
	out = Rx + 1./(Qx*(np.pi*2*frequency*1j)**px)
	return out	

def Zarcfun(Rx, Qx, px, frequency):
	out = np.zeros_like(frequency, dtype=np.complex128)
	out = 1./(1./Rx + Qx*(np.pi*2*frequency*1j)**px)
	return out


class Zarcfit(object):
	"""docstring for Zarcfit"""

	obs = None
	predSeries = None
	predParallel = None

	# Series circuit parameters
	Linf = None
	Rinf = None 
	Rh = None 
	Fh = None
	Qh = None
	Ph = None	
	Rm = None 
	Fm = None
	Qm = None
	Pm = None
	Rl = None
	Ql = None
	Fl = None
	Pl = None
	Re = None
	Qe = None
	Pef = None	
	Pei = None	

	# Parallel circuit parameters
	R0  = None
	pRh = None
	pQh = None
	pRm = None
	pQm = None
	pRl = None
	pQl = None

	def __init__(self, obs, frequency, **kwargs):
		self.obs = obs
		self.pred = np.zeros_like(obs)
		self.frequency = frequency

	def SetParametersSeries(self, Linf, Rinf, Rh, Fh, Ph, Rl, Fl, Pl, Rm, Fm, Pm, Re, Qe, Pef, Pei):
		self.Linf = Linf
		self.Rinf = Rinf
		self.Rh   = Rh   
		self.Fh   = Fh   
		self.Ph   = Ph   
		self.Rm   = Rm   
		self.Fm   = Fm   
		self.Pm   = Pm   		
		self.Rl   = Rl   
		self.Fl   = Fl   
		self.Pl   = Pl   
		self.Re   = Re   
		self.Qe   = Qe   
		self.Pef  = Pef
		self.Pei  = Pei
		
		#Compute Qh, Qm, Ql
		self.Qh = 1./(self.Rh*(2*np.pi*self.Fh)**self.Ph)
		self.Qm = 1./(self.Rm*(2*np.pi*self.Fm)**self.Pm)
		self.Ql = 1./(self.Rl*(2*np.pi*self.Fl)**self.Pl)

		self.SetParametersParallelfromSeries()

		return

	def SetParametersParallelfromSeries(self):
		self.R0   = self.Rinf + self.Rh + self.Rm + self.Rl
		self.pRh  = self.Rinf / (self.Rinf + self.Rh) / self.Rh   
		self.pQh  = self.Qh*(self.Rh/(self.Rinf+self.Rh))**2
		self.pRm  = (self.Rinf + self.Rh) * (self.Rinf + self.Rh + self.Rm) / self.Rm
		self.pQm  = self.Qm*(self.Rm/(self.Rinf+self.Rh+self.Rm))**2
		self.pRl  = (self.Rinf + self.Rh + self.Rm) * (self.Rinf + self.Rh + self.Rm + self.Rl) / self.Rl
		self.pQl  = self.Ql*(self.Rl/(self.Rinf+self.Rh+self.Rm+self.Rl))**2
		return self.R0, self.pRh, self.pRm, self.pQm, self.pRl, self.pQl	

	def ZarcElecfun(self, frequency):
		out = np.zeros_like(frequency, dtype=np.complex128)
		out = 1./(1./self.Re + self.Qe*(1j)**self.Pei*(np.pi*2*frequency)**self.Pef)
		return out

	def Zseries(self, frequency):
		self.Zinf = self.Rinf + 1j*2*np.pi*self.Linf*frequency
		self.Zh = Zarcfun(self.Rh, self.Qh, self.Ph, frequency)
		self.Zm = Zarcfun(self.Rm, self.Qm, self.Pm, frequency)
		self.Zl = Zarcfun(self.Rl, self.Ql, self.Pl, frequency)
		self.Ze = self.ZarcElecfun(self.frequency)
		self.predSeries = self.Zinf + self.Zh + self.Zm + self.Zl + self.Ze
		return self.predSeries

	def Zparallel(self, frequency):
		self.pZh = RplusCPEfun(self.pRh, self.pQh, self.Ph, frequency)
		self.pZm = RplusCPEfun(self.pRm, self.pQm, self.Pm, frequency)
		self.pZl = RplusCPEfun(self.pRl, self.pQl, self.Pl, frequency)
		self.Ze = self.ZarcElecfun(self.frequency)
		self.predParallel = 1j*2*np.pi*self.Linf + 1./(1./self.R0 + 1./self.pZh + 1./self.pZm + 1./self.pZl) + self.Ze
		return  self.predParallel

	# def CalculateImpedance(self, frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei):
	# 	Zh = Zarc(Rh, Qh, Ph, frequency)
	# 	Zl = Zarc(Rl, Ql, Pl, frequency)
	# 	Ze = ZarcElectrode(Re, Qe, Pef, Pei, frequency)
	# 	Z = Rinf + Zh + Zl + Ze
	# 	return Z


		
