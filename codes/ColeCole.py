class Zarcfit(object):
	"""docstring for Zarcfit"""

	data = None
	Linf = None
	R0 = None 
	Rh = None 
	Qh = None
	Ph = None	
	Rm = None 
	Qm = None
	Pm = None
	Rl = None
	Ql = None
	Pl = None
	Re = None
	Qe = None
	Pef = None	
	Pei = None	

	def __init__(self, data, **kwargs):
		self.data = data
	# def ReadParams(self):
	# 	self.LabID = data['LabID'].values 
	# 	self.Rm = data['Rm'].values 
	# 	self.Qm = data['Qm'].values
	# 	self.Pm = data['Pm'].values
	# 	self.Rl = data['Rl'].values 
	# 	self.Ql = data['Ql'].values
	# 	self.Pl = data['Pl'].values

	def CPEfun(Rx, Qx, px, freq):
	    out = np.zeros_like(freq, dtype=complex128)
	    out = 1./(1./Rx + Qx*(np.pi*2*freq*1j)**px)
	    return out

	def CPEfunElec(Rx, Qx, pex, pix, freq):
	    out = np.zeros_like(freq, dtype=complex128)
	    out = 1./(1./Rx + (1j)**pix*Qx*(np.pi*2*freq)**pex)
	    return out

	def CPEfunSeries(Rx, Qx, px, freq):
	    out = np.zeros_like(freq, dtype=complex128)
	    out = Rx + 1./(Qx*(np.pi*2*freq*1j)**px)
	    return out


		
