#ZarFit parameters as function of control variables:

Linf = 10**(LinfCV/1000.)
Rinf = 10**(RinfCV/1000.)
Rh = 10**(RhCV/1000.)
Fh = 10**(FhCV/1000.)
Ph = PhCV/1000.
Rm = 10**(RmCV/1000.)
Fm = 10**(FmCV/1000.)
Pm = PmCV/1000.
Rl = 10**(RlCV/1000.)
Fl = 10**(FlCV/1000.)
Pl = PlCV/1000.
Re = 10**(ReCV/1000.)
Qe = 10**(value/1000.)
Pef = PefCV/1000.
Pei = PeiCV/1000.

Qh = 1./(Rh*(2*np.pi*Fh)**Ph)
Qm = 1./(Rm*(2*np.pi*Fm)**Pm)
Ql = 1./(Rl*(2*np.pi*Fl)**Pl)

R0   = Rinf + Rh + Rm + Rl
pRh  = Rinf * (Rinf + Rh) / Rh   
pRm  = (Rinf + Rh) * (Rinf + Rh + Rm) / Rm
pRl  = (Rinf + Rh + Rm) * (Rinf + Rh + Rm + Rl) / Rl

pQh  = Qh*(Rh/(Rinf+Rh))**2
pQm  = Qm*(Rm/(Rinf+Rh+Rm))**2
pQl  = Ql*(Rl/(Rinf+Rh+Rm+Rl))**2


#ZarFit control variables as function of parameters:

pS0 = 1./R0
pSl = 1/pRl
pSm = 1/pRm
pSh = 1/pRh

Rl = pSl / (pS0*(pS0 + pSl))
Rm = pSm / ((pS0 + pSl)*(pS0 + pSl + pSm))
Rh = pSh / ((pS0 + pSl + pSm)*(pS0 + pSl + pSm + pSh))
Rinf = 1/(pS0 + pSl + pSm + pSh)

Qh  = pQh*((Rinf+Rh)/Rh)**2
Qm  = pQm*((Rinf+Rh+Rm)/Rm)**2
Ql  = pQl*((Rinf+Rh+Rm+Rl)/Rl)**2

Fh = 1./(2*np.pi*(Rh*Qh)**(1/Ph))
Fm = 1./(2*np.pi*(Rm*Qm)**(1/Pm))
Fl = 1./(2*np.pi*(Rl*Ql)**(1/Pl))

LinfCV = np.log10(Linf)*1000.
RinfCV = np.log10(Rinf)*1000.
RhCV = np.log10(Rh)*1000.
FhCV = np.log10(Fh)*1000.
PhCV = Ph*1000
RmCV = np.log10(Rm)*1000.
FmCV = np.log10(Fm)*1000.
PmCV = Pm*1000
RlCV = np.log10(Rl)*1000.
FlCV = np.log10(Fl)*1000.
PlCV = Pl*1000
ReCV = np.log10(Qe)*1000.
QeCV = Pef*1000
PeiCV = Pei*1000
PefCV = Pef*1000
