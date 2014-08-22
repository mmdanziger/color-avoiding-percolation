import graph_tool.all as gt
from pylab import *
import sys
from math import factorial
from scipy.misc import comb
import scipy.optimize as opt
import os
from scipy.stats import poisson
from scipy.stats import binom
from scipy.stats import zipf



### Generating function
def gen(z,p_k):
    return sum(p_k*z**arange(len(p_k)))

### Right hand side of self consistency equation
def self_consistency(z,q_k,phi):
    return 1.-gen(1.,q_k[:-1]*phi[1:])+gen(z,q_k[:-1]*phi[1:])






### Analytical result for S_color, 
###   for degree distribution p_k, colors r_c[c,k]
def analytics(p_k,r_c,nr_sam):
    # some needed quantities
    k=sum(arange(len(p_k))*p_k)
    q_k=0.*p_k
    q_k[:-1]=arange(len(p_k))[1:]*p_k[1:]/k
    C=len(r_c[:,0])
    # calculate giant component
    phi=1.*ones(len(p_k))
    u0=opt.fixed_point(self_consistency,0.5,args=[q_k,phi])
    # ... and calculate color avoiding components
    u_c=0.*zeros(C)
    U_c=0.*zeros(C)
    r_c_av_over_link=0.*zeros(C)
    for c_ in arange(C):
        phi = 1. - r_c[c_,:]
        r_c_av_over_link[c_]=sum(arange(len(r_c[c_,:]))*r_c[c_,:]*p_k)/k
        phi_av_over_link = 1. - r_c_av_over_link[c_]
        u_c[c_]=opt.fixed_point(self_consistency,0.5,args=[q_k,phi])
        U_c[c_] = 1. - (1.-u_c[c_])/((1.-u0)*phi_av_over_link)
    # S1 = gen(1.,p_k*phi) - gen(u_c[c_],p_k*phi)
    ### calculate component size
    S_color_analyt=0.
    ### ... by averaging over degree distribution
    for k1 in arange(100)+2:
        # ... sample the links according to gc and colors
        for i_rand in arange(nr_sam):
            color_vector=0.*zeros(k1)
            for k_ in arange(k1):
                color_vector[k_]=C-sum(1*(random()<cumsum(r_c_av_over_link)))
            no_gc=random(k1)
            color_vector=color_vector*(no_gc<(1.-u0))-1*(no_gc>=(1.-u0))
            k0=sum(color_vector==-1)
            # ... calculate the product over colors of successful links
            p_success=1.
            for c_ in arange(C):
                k_c=sum(color_vector==c_)
                p_success*=(1. - U_c[c_]**(k1 - k_c - k0))
            S_color_analyt+=p_k[k1]*p_success/nr_sam
    return S_color_analyt


### S_grenz and giant component, means topology part independent of colors
def S_grenz(p_k):
    # Some needed quantities
    k=sum(arange(len(p_k))*p_k)
    q_k=0.*p_k
    q_k[:-1]=arange(len(p_k))[1:]*p_k[1:]/k
    # calculate giant component
    phi=1.
    u0=opt.fixed_point(self_consistency,0.5,args=[q_k,phi])
    S0=1.-g_0(u0,p_k)
    du=1e-5
    S_grenz = S0- (1.-u0)*(g_0(u0,p_k)-g_0(u0-du,p_k))/du
    return (S_grenz,S0)



### Numerical result of S_color, for graph g with colors c 
def numerics(g,c):
    # some needed numbers
    C=c.a.max()+1
    N=g.num_vertices()
    # label color avoiding components
    in_largest={}
    for i_c in arange(C):
        in_largest[i_c]=g.new_vertex_property('bool')
        u = gt.GraphView(g,vfilt=(c.a!=i_c))
        component = gt.label_largest_component(u)
        in_largest[i_c].a = (component.a==1)
    ### count S_color
    have_all=0
    for i_n in arange(N):
        v=g.vertex(i_n)
        has_all=True
        for i_c in arange(C):
            has_this=False
            for i_out in v.out_neighbours():
                if in_largest[i_c][i_out]:has_this=True
            if not has_this:has_all=False
        if has_all:have_all+=1  
    return 1.*have_all/N




### Function for color distribution
def r_c_func(k,k_step):
    r_1 = 0.5*(k<k_step) + 1.*(k>=k_step)
    return array([r_1, 1.-r_1])


### Parameters and file preparation
alpha=2.3
k_steps=array([1000,100,65,50,40,30,26,23,20,18,17,16,15])
C=2
runs=100

analytical=True
if analytical:
    nr_sam=100
    k_max=100000
    p_k=zipf.pmf(arange(k_max),alpha)
    fname='../data_new/S_color_degree_dependent_analyt_a%1.4f_n%d.dat'%(alpha,nr_sam)
else:
    N=10000
    fname='../data_new/S_color_degree_dependent_num_a%1.4f_N%d.dat'%(alpha,N)

file_=open(fname,'a')
file_.write('# k_step gamma S_color\n')
file_.close()
    




### Start calculations
#for alpha in linspace(2.5,3.5,5):
for i in arange(runs):
    print()
    print(fname)
    print('################ run',i,'#############')
    for k_step in k_steps:
        ### analytics
        if analytical:
            gamma=1.-sum(p_k[:k_step])
            print('k_step, gamma',k_step,gamma)
            ### color distribution
            r_c=.5*ones((2,len(p_k)))
            r_c[0,:]=0.5*(arange(k_max)<k_step)+1.*(arange(k_max)>=k_step)
            r_c[1,:]=1.-r_c[0,:]
            ### analytics
            analyt=analytics(p_k,r_c,nr_sam)
            print('analytics:',analyt)
            ### write to file
            file_=open(fname,'a')
            file_.write('%d %e %e\n'%(k_step,gamma,analyt))
            file_.close()
        ### numerics
        if not analytical:
            ### prepare graphs
            g = gt.random_graph(N, lambda: zipf.rvs(alpha), directed=False)
            c = g.new_vertex_property('int')
            degs=g.degree_property_map('out').a
            for n_ in arange(N):
                c.a[n_]=C-sum(1*(random()<cumsum(r_c_func(degs[n_],k_step))))
            ### count component
            numer_=numerics(g,c)
            gamma_=sum(1*(degs>=k_step))/N
            print('gamma numerics:',gamma_,numer_)
            ### save to file
            file_=open(fname,'a')
            file_.write('%d %e %e\n'%(k_step,gamma_,numer_))
            file_.close()





