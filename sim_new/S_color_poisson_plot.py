from pylab import *
import scipy.optimize as opt



### Extract data from file and calculate mean and errors
def get_data(fname):
    a=loadtxt(fname)
    values_=1*a[:,0]
    values_.sort()
    values=values_[0:1]
    for hv in values_:
        if hv>values.max():
            values=append(values,hv)
    results1=0.*values
    err1=0.*values
    counts=0.*values
    for i in arange(len(a[:,0])):
        hv=arange(len(values))[values==a[i,0]]
        #print(hv,a[i,0])
        results1[hv]+=a[i,1]
        err1[hv]+=a[i,1]**2
        counts[hv]+=1
    yerr=2.*sqrt((err1/counts-(results1/counts)**2)/counts)
    print(fname)
    print(counts.mean())
    return (values,results1/counts,yerr)


### Generating function
def gen(z,k):
    return exp(-k*(1.-z))

### Calculate S
def S(ks):
    S0=0.*ks
    for hv in arange(len(ks)):
        u0=opt.fixed_point(gen,0.5,args=[ks[hv]])
        S0[hv]=1.-gen(u0,ks[hv])
    return S0


def u(ks):
    u0=0.*ks
    for hv in arange(len(ks)):
        u0[hv]=opt.fixed_point(gen,0.5,args=[ks[hv]])
    return u0






fig_=figure(2)
fig_.set_size_inches(5,4)

nr_sam=100
C=2
fname='../data_new/S_color_poisson_analyt_C%d_n%d.dat'%(C,nr_sam)
(x,y,yerr)=get_data(fname)
plot(x,y,'-',color='g',label=r'${\bar k} = 6$')
N=1000
fname='../data_new/S_color_poisson_num_C%d_N%d.dat'%(C,N)
(x,y,yerr)=get_data(fname)
errorbar(x,y,yerr=yerr,fmt='o',color='g',label=r'$N=%d$'%N)


nr_sam=100
C=10
fname='../data_new/S_color_poisson_analyt_C%d_n%d.dat'%(C,nr_sam)
(x,y,yerr)=get_data(fname)
plot(x,y,'-',color='b',label=r'${\bar k} = 6$')
N=1000
fname='../data_new/S_color_poisson_num_C%d_N%d.dat'%(C,N)
(x,y,yerr)=get_data(fname)
errorbar(x,y,yerr=yerr,fmt='s',color='b',label=r'$N=%d$'%N)


#nr_sam=100
#C=100
#fname='../data_new/S_color_poisson_analyt_C%d_n%d.dat'%(C,nr_sam)
#(x,y,yerr)=get_data(fname)
#errorbar(x,y,yerr=yerr,fmt='-',color='y',label=r'${\bar k} = 6$')
#N=1000
#fname='../data_new/S_color_poisson_num_C%d_N%d.dat'%(C,N)
#(x,y,yerr)=get_data(fname)
#errorbar(x,y,yerr=yerr,fmt='d',color='k',label=r'$N=%d$'%N)

#############################
### homogene color distribuion gives higher S_color:
#############################
#nr_sam=100
#C=4
#fname='../data_new/S_color_poisson_analyt_C%d_n%d.dat'%(C,nr_sam)
#(x,y,yerr)=get_data(fname)
#plot(x,y,'-',color='g',label=r'${\bar k} = 6$')
#fname='../data_new/S_color_poisson_analyt_C4_kc01.4000_ndeg1_n100.dat'
#(x,y,yerr)=get_data(fname)
#plot(x,y,'-',color='r',label=r'${\bar k} = 6$')





ks=linspace(0.,10.,200)#append(linspace(0.98,1.7,100),linspace(1.7,10.0,100))
S0=S(ks)
plot(ks,S0,'--',color='k',label=r'${\bar k} = 6$')
plot(ks,S0-ks*S0*(1.-S0),':',color='r',label=r'${\bar k} = 6$')
### additionally accounting for two links with same color
#plot(ks,S0-ks*S0*(1.-S0)-ks**2/2*S0**2*(1.-S0)*.1,':',color='b',label=r'${\bar k} = 6$')
### this is exactly the result for C=2, why? not working for larger C
#plot(ks/.5,S0**2,':',color='r',label=r'${\bar k} = 6$')






xlim(0.9,8)
ylim(0,1)
xlabel(r'$\bar k$')
ylabel(r'$S_{\rm color}$')
#legend()
tight_layout(pad=0.4)
savefig('S_color_poisson.pdf')








show()