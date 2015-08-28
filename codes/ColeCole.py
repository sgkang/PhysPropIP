class ModifiedColeCole(object):
	"""docstring for ModifiedColeCole"""
	data = None
	Rm = None
	Qm = None
	def __init__(self, data, **kwargs):
		self.data = data

	def ReadParams(self):
		self.Rm = data['Rm'].values 
		self.Qm = data['Qm'].values
		self.Pm = data['Pm'].values
		self.Rl = data['Rl'].values 
		self.Ql = data['Ql'].values
		self.Pl = data['Pl'].values

	def CPEfun(Rx, Qx, px, freq):
	    
	    out = np.zeros_like(freq, dtype=complex128)
	    out = (Rx*Qx*(1j*np.pi*2*freq)**px+1.)/Rx
	    out = 1./(1./Rx + 1j*Qx*(np.pi*2*freq)**px)

	    return out


		
