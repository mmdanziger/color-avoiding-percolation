from pylab import *
import matplotlib.patches as mpatches



### figure preparation
fig=figure(1)
width=2.6
height=2.6
fig.set_size_inches(4,4.*height/width)


### choose the mode, deciding which subsets are chosen, and put text
###     0    1      2         3         4          5         6         7
modes=['all','gc','no_1_gc','gc_no_1','no_2_gc','gc_no_2','no_3_gc','gc_no_3']

for iii in arange(8):
    clf()
    ax=axes()
    ax.set_xticks([])
    ax.set_yticks([])
    mode=modes[iii]
    links=[]
    white=True
    if mode=='all':
        (L,notL)=(True,True)
        (c1,c2,c3)=(True,True,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        links=[1.1,1.2,1.3,1.45]
        text(-0.08,1.05,r'$G$',color='k',fontsize=25)
        text(0.9,1.3,r'$k$ links',color='k',fontsize=20)
    if mode=='gc':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,True,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        links=[1.1,1.2,1.3]
        text(-0.08,1.05,r'$G$',color='k',fontsize=25)
        text(0.9,1.3,r"$k'$ links",color='k',fontsize=20)
    if mode=='no_1_gc':
        (L,notL)=(True,False)
        (c1,c2,c3)=(False,True,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        links=[1.15,1.3]
        text(0.6,1.3,r"$k'-\kappa_{\rm r}$ links",color='k',fontsize=20)
    if mode=='no_2_gc':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,False,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        links=[1.1,1.2]
        text(0.6,1.3,r"$k'-\kappa_{\rm g}$ links",color='k',fontsize=20)
    if mode=='no_3_gc':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,True,False)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        links=[1.1,1.25]
        text(0.6,1.3,r"$k'-\kappa_{\rm b}$ links",color='k',fontsize=20)
    if mode=='gc_no_1':
        (L,notL)=(True,False)
        (c1,c2,c3)=(False,True,True)
        (not1,not2,not3)=(False,False,False)
        (Lnot1,Lnot2,Lnot3)=(True,False,False)
        links=[1.25]
        text(0.7,1.3,r"$>0$ links",color='k',fontsize=20)
        white=False
    if mode=='gc_no_2':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,False,True)
        (not1,not2,not3)=(False,False,False)
        (Lnot1,Lnot2,Lnot3)=(False,True,False)
        links=[1.15]
        text(0.7,1.3,r"$>0$ links",color='k',fontsize=20)
    if mode=='gc_no_3':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,True,False)
        (not1,not2,not3)=(False,False,False)
        (Lnot1,Lnot2,Lnot3)=(False,False,True)
        links=[1.25]
        text(0.7,1.3,r"$>0$ links",color='k',fontsize=20)



    
    ### Plot the chosen parts within the giant component
    r=.4
    if L:
        if c1:
            if not1:
                w=mpatches.Wedge((0,0),1,120,240,facecolor='r',edgecolor='w')
                ax.add_patch(w)
            if Lnot2:
                w=mpatches.Wedge((r*cos(2.*pi/3),r*sin(2.*pi/3)),r,120,300,fill=(not not1),edgecolor='w',facecolor='r')
                ax.add_patch(w)
                text(-.47,.25,r'$G_{\bar{\rm g}}$',color='w',fontsize=25)
                #text(-.6,.23,r'$G$',color='w',fontsize=23)
            elif white:
                w=mpatches.Wedge((r*cos(2.*pi/3),r*sin(2.*pi/3)),r,120,300,fill=True,edgecolor='w',facecolor='w')
                ax.add_patch(w)
            if Lnot3:
                w=mpatches.Wedge((r*cos(2.*pi/3),-r*sin(2.*pi/3)),r,60,240,fill=(not not1),edgecolor='w',facecolor='r')
                ax.add_patch(w)
                #c=mpatches.Circle((-.47,-.2),.3,fill=(not not1),edgecolor='w',facecolor='r')
                #ax.add_patch(c)
                text(-.49,-.32,r'$G_{\bar{\rm b}}$',color='w',fontsize=25)
                #text(-.6,-.35,r'$G$',color='w',fontsize=23)
        if c2:
            if not2:
                w=mpatches.Wedge((0,0),1,240,360,facecolor='g',edgecolor='w')
                ax.add_patch(w)
            if Lnot1:
                w=mpatches.Wedge((r,0.),r,180,360,fill=(not not2),edgecolor='w',facecolor='g')
                ax.add_patch(w)
                text(.3,-.23,r'$G_{\bar{\rm r}}$',color='w',fontsize=25)
                #text(.35,-.3,r'$G$',color='w',fontsize=23)
            if Lnot3:
                w=mpatches.Wedge((r*cos(2.*pi/3),-r*sin(2.*pi/3)),r,240,60,fill=(not not2),edgecolor='w',facecolor='g')
                ax.add_patch(w)
                text(-.2,-.5,r'$G_{\bar{\rm b}}$',color='w',fontsize=25)
                #text(-.2,-.55,r'$G$',color='w',fontsize=23)
        if c3:
            if not3:
                w=mpatches.Wedge((0,0),1,0,120,facecolor='b',edgecolor='w')
                ax.add_patch(w)
            if Lnot1:
                w=mpatches.Wedge((r,0.),r,0,180,fill=(not not3),edgecolor='w',facecolor='b')
                ax.add_patch(w)
                text(.3,.12,r'$G_{\bar{\rm r}}$',color='w',fontsize=25)
                #text(.35,.2,r'$G$',color='w',fontsize=23)
            if Lnot2:
                w=mpatches.Wedge((r*cos(2.*pi/3),r*sin(2.*pi/3)),r,300,120,fill=(not not3),edgecolor='w',facecolor='b')
                ax.add_patch(w)
                text(-.20,.41,r'$G_{\bar{\rm g}}$',color='w',fontsize=25)
                #text(-.2,.45,r'$G$',color='w',fontsize=23)
            elif white:
                w=mpatches.Wedge((r*cos(2.*pi/3),r*sin(2.*pi/3)),r,300,120,fill=True,edgecolor='w',facecolor='w')
                ax.add_patch(w)

    ### plot the chosen parts outside giant component
    if notL:
        if c1:
            w=mpatches.Wedge((1.2,-0.7),.3,120,170,facecolor='r',edgecolor='w')
            ax.add_patch(w)
            w=mpatches.Wedge((1.2,-0.7),.3,180,230,facecolor='r',edgecolor='w')
            ax.add_patch(w)
        if c2:
            w=mpatches.Wedge((1.2,-0.7),.3,240,290,facecolor='g',edgecolor='w')
            ax.add_patch(w)
            w=mpatches.Wedge((1.2,-0.7),.3,300,350,facecolor='g',edgecolor='w')
            ax.add_patch(w)
        if c3:
            w=mpatches.Wedge((1.2,-0.7),.3,0,50,facecolor='b',edgecolor='w')
            ax.add_patch(w)
            w=mpatches.Wedge((1.2,-0.7),.3,60,110,facecolor='b',edgecolor='w')
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
    savefig('sets_k_%s.pdf'%mode)


show()


