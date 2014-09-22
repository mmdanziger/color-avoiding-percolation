from pylab import *



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
    results2=0.*values
    err1=0.*values
    err2=0.*values
    counts=0.*values
    for i in arange(len(a[:,0])):
        hv=arange(len(values))[values==a[i,0]]
        #print(hv,a[i,0])
        results1[hv]+=a[i,1]
        err1[hv]+=a[i,1]**2
        results2[hv]+=a[i,2]
        err2[hv]+=a[i,2]**2
        counts[hv]+=1
    xerr=2.*sqrt((err1/counts-(results1/counts)**2)/counts)
    yerr=2.*sqrt((err2/counts-(results2/counts)**2)/counts)
    print(fname)
    print(counts.mean())
    return (results1/counts,results2/counts,xerr,yerr)



### Scale free graphs
fig_=figure(1)
fig_.set_size_inches(5,4)
sub=fig_.add_subplot(111)

alpha=2.3
nr_sam=100
fname='../data_new/S_color_degree_dependent_analyt_a%1.4f_n%d.dat'%(alpha,nr_sam)
(x,y,xerr,yerr)=get_data(fname)
plot(x,y,'-',color='k',label=r'$\alpha=2.3$')
#errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o--',color='k')
N=10000
fname='../data_new/S_color_degree_dependent_num_a%1.4f_N%d.dat'%(alpha,N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o--',label=r'$N=%d$'%N)
N=50000
fname='../data_new/S_color_degree_dependent_num_a%1.4f_N%d.dat'%(alpha,N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='s--',label=r'$N=%d$'%N)
N=200000
fname='../data_new/S_color_degree_dependent_num_a%1.4f_N%d.dat'%(alpha,N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='d--',label=r'$N=%d$'%N)

alpha=2.5
nr_sam=100
fname='../data_new/S_color_degree_dependent_analyt_a%1.4f_n%d.dat'%(alpha,nr_sam)
(x,y,xerr,yerr)=get_data(fname)
plot(x,y,'-',color='r',label=r'$\alpha=2.5$')
#errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o--',color='r')
N=10000
fname='../data_new/S_color_degree_dependent_num_a%1.4f_N%d.dat'%(alpha,N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o--',color='b')

sub.set_xticks([0,0.005,0.01,0.015])
xlim(0,0.017)
ylim(0,0.127)
xlabel(r'$\gamma$')
ylabel(r'$S_{\rm color}$')
legend()
tight_layout(pad=0.4)
savefig('S_color_degree_dependent_broad.pdf')




### Poisson graphs
fig_=figure(2)
fig_.set_size_inches(5,4)

k_av=6.
nr_sam=100
fname='../data_new/S_color_degree_dependent_poisson_analyt_k%2.4f_n%d.dat'%(k_av,nr_sam)
(x,y,xerr,yerr)=get_data(fname)
plot(x,y,'-',color='k',label=r'${\bar k} = 6$')
N=10000
fname='../data_new/S_color_degree_dependent_poisson_num_k%2.4f_N%d.dat'%(k_av,N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o--',color='r',label=r'$N=%d$'%N)

xlim(0,0.57)
ylim(0,0.9)
xlabel(r'$\gamma$')
ylabel(r'$S_{\rm color}$')
legend()
tight_layout(pad=0.4)
savefig('S_color_degree_dependent_poisson.pdf')




### Autonomous systems
fig_=figure(3)
fig_.set_size_inches(5,4)

N=10000
fname='../data/S_color_degree_dependent_data_num_N%d.dat'%(N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='o--',color='r',label='data')
fname='../data/S_color_degree_dependent_data_rewirecorr__num_N%d.dat'%(N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='s--',color='g',label=r'shuffled (corr)')
nr_sam=100
fname='../data_new/S_color_degree_dependent_data_analyt_nomodel_n%d.dat'%(nr_sam)
(x,y,xerr,yerr)=get_data(fname)
plot(x,y,'-',color='k',label=r'analytical')
fname='../data/S_color_degree_dependent_data_rewireuncorr__num_N%d.dat'%(N)
(x,y,xerr,yerr)=get_data(fname)
errorbar(x,y,xerr=xerr,yerr=yerr,fmt='d--',color='b',label=r'shuffled (uncorr)')

xlim(0,0.029)
ylim(0,0.38)
xlabel(r'$\gamma$')
ylabel(r'$S_{\rm color}$')
legend()
tight_layout(pad=0.4)
savefig('S_color_degree_dependent_data.pdf')




show()