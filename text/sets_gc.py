from pylab import *
import matplotlib.patches as mpatches



### figure preparation
fig=figure(1)
width=2.6
height=2.6
fig.set_size_inches(4,4.*height/width)


### choose the mode, deciding which subsets are chosen, and put text
###       0     1      2     3         4          5         6         7
modes=['allk','all1','gck','no1']

for iii in arange(4):
    clf()
    ax=axes()
    ax.set_xticks([])
    ax.set_yticks([])
    mode=modes[iii]
    links=[]
    white=True
    if mode=='allk':
        (L,notL)=(True,True)
        links=[1.1,1.2,1.3,1.45]
        text(-0.08,1.05,r'$G$',color='k',fontsize=25)
        text(0.9,1.3,r'$k$ links',color='k',fontsize=20)
    if mode=='all1':
        (L,notL)=(True,True)
        links=[1.4]
        text(-0.08,1.05,r'$G$',color='k',fontsize=25)
        text(0.9,1.3,r'$1$ link',color='k',fontsize=20)
    if mode=='gck':
        (L,notL)=(True,False)
        links=[1.1,1.2]
        text(-0.08,1.05,r'$G$',color='k',fontsize=25)
        text(0.7,1.3,r'$>0$ linkss',color='k',fontsize=20)
    if mode=='no1':
        (L,notL)=(False,True)
        links=[1.45]
        text(0.9,1.3,r'$1$ link',color='k',fontsize=20)



    
    ### Plot the chosen parts within the giant component
    r=.4
    if L:
        w=mpatches.Circle((0,0),1,facecolor=(.4,.4,.4),edgecolor='w')
        ax.add_patch(w)

    ### plot the chosen parts outside giant component
    if notL:
        w=mpatches.Wedge((1.2,-0.7),.3,120,170,facecolor=(.4,.4,.4),edgecolor='w')
        ax.add_patch(w)
        w=mpatches.Wedge((1.2,-0.7),.3,180,230,facecolor=(.4,.4,.4),edgecolor='w')
        ax.add_patch(w)
        w=mpatches.Wedge((1.2,-0.7),.3,240,290,facecolor=(.4,.4,.4),edgecolor='w')
        ax.add_patch(w)
        w=mpatches.Wedge((1.2,-0.7),.3,300,350,facecolor=(.4,.4,.4),edgecolor='w')
        ax.add_patch(w)
        w=mpatches.Wedge((1.2,-0.7),.3,0,50,facecolor=(.4,.4,.4),edgecolor='w')
        ax.add_patch(w)
        w=mpatches.Wedge((1.2,-0.7),.3,60,110,facecolor=(.4,.4,.4),edgecolor='w')
        ax.add_patch(w)




    ### plot the links and node
    c=mpatches.Circle((1.35,1.15),.05,color='k',zorder=10)
    ax.add_patch(c)
    for angle in links:
        plot([1.35,1.35+.4*cos(pi*angle)],[1.15,1.15+.4*sin(pi*angle)],color='k',lw=2)


    ### complete figure and save
    xlim(-1.05,-1.05+width)
    ylim(-1.05,-1.05+height)
    tight_layout(pad=0.05)
    savefig('sets_gc_%s.pdf'%mode)


show()


