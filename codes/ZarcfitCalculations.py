import numpy as np

def RplusCPEfun(Rx, Qx, px, frequency):
	out = np.zeros_like(frequency, dtype=np.complex128)
	out = Rx + 1./(Qx*(np.pi*2*frequency*1j)**px)
	return out	
    
def Zarcfun(Rx, Qx, px, frequency):
	out = np.zeros_like(frequency, dtype=np.complex128)
	out = 1./(1./Rx + Qx*(np.pi*2*frequency*1j)**px)
	return out

def SetDefaultParameters():    
    Linf = 1.E-4
    Rinf = 1.E4
    Rh = 1.E5
    Fh = 1e5
    Ph = 0.8
    Rm = 1e-1
    Fm = 1e-1
    Pm = 0.5        
    Rl = 1.E4
    Fl = 1.e1
    Pl = 0.5    
    Re = 1.E10
    Qe = 1.E-4
    Pef = 0.5
    Pei = 0.05    
    return  Linf, Rinf, Rh, Fh, Ph, Rl, Fl, Pl, Rm, Fm, Pm, Re, Qe, Pef, Pei


class ZarcfitCalculations(object):
	"""docstring for ZarcfitCalculations"""

	obs = None
	predSeries = None
	predParallel = None

	# Series circuit parameters
	Linf = 1e-4
	Rinf = 1e4
	Rh = 1.E5
	Fh = 1e5
	Ph = 0.8
	Rm = 1e-1
	Fm = 1e-1
	Pm = 0.5        
	Rl = 1.E4
	Fl = 1.e1
	Pl = 0.5    
	Re = 1.e10
	Qe = 1.e-4
	Pef = 0.5
	Pei = 0.05    
	Qh = None
	Qm = None
	Ql = None

	Zinf = None
	Zh   = None
	Zm   = None
	Zl   = None
	Ze   = None	

	# Parallel circuit parameters
	R0  = None
	pRh = None
	pQh = None
	pRm = None
	pQm = None
	pRl = None
	pQl = None

	pZh = None
	pZm = None
	pZl = None

	# Sensitivity
	J = None

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
		self.pRh  = self.Rinf * (self.Rinf + self.Rh) / self.Rh   
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
     		#Compute Qh, Qm, Ql
		self.Qh = 1./(self.Rh*(2*np.pi*self.Fh)**self.Ph)
		self.Qm = 1./(self.Rm*(2*np.pi*self.Fm)**self.Pm)
		self.Ql = 1./(self.Rl*(2*np.pi*self.Fl)**self.Pl)

		self.Zinf = self.Rinf + 1j*2*np.pi*self.Linf*frequency
		self.Zh = Zarcfun(self.Rh, self.Qh, self.Ph, frequency)
		self.Zm = Zarcfun(self.Rm, self.Qm, self.Pm, frequency)
		self.Zl = Zarcfun(self.Rl, self.Ql, self.Pl, frequency)
		self.Ze = self.ZarcElecfun(frequency)
		self.predSeries = self.Zinf + self.Zh + self.Zm + self.Zl + self.Ze
		return self.predSeries

	def Zparallel(self, frequency):
     		#Compute Qh, Qm, Ql
		self.Qh = 1./(self.Rh*(2*np.pi*self.Fh)**self.Ph)
		self.Qm = 1./(self.Rm*(2*np.pi*self.Fm)**self.Pm)
		self.Ql = 1./(self.Rl*(2*np.pi*self.Fl)**self.Pl)
		self.SetParametersParallelfromSeries()
  
		self.pZh = RplusCPEfun(self.pRh, self.pQh, self.Ph, frequency)
		self.pZm = RplusCPEfun(self.pRm, self.pQm, self.Pm, frequency)
		self.pZl = RplusCPEfun(self.pRl, self.pQl, self.Pl, frequency)
		self.Ze = self.ZarcElecfun(frequency)
		self.predParallel = 1j*2*np.pi*self.Linf*frequency + 1./(1./self.R0 + 1./self.pZh + 1./self.pZm + 1./self.pZl) + self.Ze
		return  self.predParallel

	def SetModel(self, model):
		self.Linf = np.exp(model[0])      if ~np.isnan(model[0])  else self.Linf 
		self.Rinf = np.exp(model[1]) 	  if ~np.isnan(model[1])  else self.Rinf        
		self.Rh   = np.exp(model[2])      if ~np.isnan(model[2])  else self.Rh    
		self.Fh   = np.exp(model[3])      if ~np.isnan(model[3])  else self.Fh    
		self.Ph   = model[4]      		  if ~np.isnan(model[4])  else self.Ph    
		self.Rl   = np.exp(model[5])      if ~np.isnan(model[5])  else self.Rl    
		self.Fl   = np.exp(model[6])      if ~np.isnan(model[6])  else self.Fl    
		self.Pl   = model[7]      		  if ~np.isnan(model[7])  else self.Pl    
		self.Rm   = np.exp(model[8])      if ~np.isnan(model[8])  else self.Rm    
		self.Fm   = np.exp(model[9])      if ~np.isnan(model[9])  else self.Fm    
		self.Pm   = model[10]     		  if ~np.isnan(model[10]) else self.Pm     
		self.Re   = np.exp(model[11])     if ~np.isnan(model[11]) else self.Re     
		self.Qe   = np.exp(model[12])     if ~np.isnan(model[12]) else self.Qe     
		self.Pef  = model[13]     		  if ~np.isnan(model[13]) else self.Pef     
		self.Pei  = model[14]     		  if ~np.isnan(model[14]) else self.Pei     

	def GetDefaultmodel(self):
		model = np.ones(15)*np.nan
		model[0]  = np.log(1e-4)        #Linf          
		model[1]  = np.log(1e4)      #Rinf        
		model[2]  = np.log(1.E5)     #Rh           
		model[3]  = np.log(1e5)      #Fh          
		model[4]  = 0.8              #Ph          
		model[5]  = np.log(1.E4)           #Rl           
		model[6]  = np.log(1.e1)           #Fl           
		model[7]  = 0.5     		 #Pl                  
		model[8]  = 1e-1    #Rm           
		model[9]  = np.log(1.e3)     #Fm           
		model[10] = 0.5              #Pm              
		model[11] = np.log(1e10)     #Re            
		model[12] = np.log(1e-4)      #Qe            
		model[13] = 0.5  		     #Pef         
		model[14] = 0.05			 #Pei 	              
		return model

	Re = 1.e10
	Qe = 1.e-4
	Pef = 0.5
	Pei = 0.05    

	def dpred(self, model):
		self.SetModel(model)
		#Compute Qh, Qm, Ql
		self.Qh = 1./(self.Rh*(2*np.pi*self.Fh)**self.Ph)
		self.Qm = 1./(self.Rm*(2*np.pi*self.Fm)**self.Pm)
		self.Ql = 1./(self.Rl*(2*np.pi*self.Fl)**self.Pl)
		self.SetParametersParallelfromSeries()
		out = self.Zseries(self.frequency)
		return np.r_[out.real, out.imag]

	def getJ(self, model, perc = 1e-4):
		inactive = np.isnan(model)
		nmod = (~inactive).sum()
		nfreq = self.frequency.size
		self.J = np.zeros((nfreq*2, nmod))
		icount = 0		
		#Use Central difference to compute sensitivity function
		for i, mi in enumerate(model):
			if ~np.isnan(mi):
				modtempa = model.copy()
				modtempb = model.copy()
				dmi = perc*mi
				modtempa[i] = model[i]+dmi
				modtempb[i] = model[i]-dmi
				self.J[:,icount] = (self.dpred(modtempa)-self.dpred(modtempb)) / (2*dmi)
				icount+=1

		return self.J

	def GN(self, m0, uncert, maxiter=10, maxiterLs=20):
		inactive = np.isnan(m0)
		m = m0[~inactive]
		mall = m0.copy()
		mtempall = m0.copy()

		dobs = np.r_[self.obs.real, self.obs.imag]
		Wd = np.diag(1./uncert)
		targetmisfit = dobs.size
		iteration = 0
		while True:
			dpred = self.dpred(mall)
			r = dpred-dobs
			misfit0 = 0.5*np.linalg.norm(np.dot(Wd, r))**2
			J = self.getJ(mall)
			Jtemp = np.dot(Wd, J)
			H =  np.dot(Jtemp.T, Jtemp) + np.diag(np.ones_like(m))*1e-3
			g = np.dot(Jtemp.T, r)
			dm = np.linalg.solve(H, -g)
			iterationLs=0
			while True:
				mtemp = m+dm
				mtempall[~inactive] = mtemp
				dpred = self.dpred(mtempall)
				r = dpred-dobs
				misfit1 = 0.5*np.linalg.norm(np.dot(Wd, r))**2
				if misfit1 < misfit0:
					print ("misfit:", misfit0, misfit1)
					break
				elif iterationLs > maxiterLs:
					break
				dm = dm*0.5
				iterationLs+=1

			mall = mtempall.copy()
			m = mall[~inactive]
			
			if misfit1 < targetmisfit:
				break
			elif iteration > maxiter:
				break

			print (iteration, misfit1) 
			iteration += 1
			
		return mall

	def Jvec(self, model, vec):
		J = self.getJ(model)
		return np.dot(J, vec)





	# def CalculateImpedance(self, frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei):
	# 	Zh = Zarc(Rh, Qh, Ph, frequency)
	# 	Zl = Zarc(Rl, Ql, Pl, frequency)
	# 	Ze = ZarcElectrode(Re, Qe, Pef, Pei, frequency)
	# 	Z = Rinf + Zh + Zl + Ze
	# 	return Z


		
