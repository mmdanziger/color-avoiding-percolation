from pylab import *
import matplotlib.patches as mpatches



### figure preparation
fig=figure(1)
fig.set_size_inches(6,4)


### choose the mode, deciding which subsets are chosen, and put text
###     0      1     2       3         4          5            6         
modes=['all','no_gc','c2','gc_no_2','no_2_gc','no_2_gc_no','gc_no_gc_no_2']

for iii in arange(7):
    clf()
    ax=axes()
    ax.set_xticks([])
    ax.set_yticks([])
    mode=modes[iii]
    (l1,l2,l3,l4,l5)=(False,False,False,False,False)
    white=True
    if mode=='all':
        (L,notL)=(True,True)
        (c1,c2,c3)=(True,True,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        l5=True
        text(1.3,0.93,r'$1$ link',color='k',fontsize=18)
    if mode=='no_gc':
        (L,notL)=(False,True)
        (c1,c2,c3)=(True,True,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        l4=True
        text(1.3,0.93,r"$1$ link",color='k',fontsize=18)
    if mode=='c2':
        (L,notL)=(True,True)
        (c1,c2,c3)=(False,True,False)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        l3=True
        text(1.3,0.93,r"$1$ link",color='k',fontsize=18)
    if mode=='gc_no_2':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,False,True)
        (not1,not2,not3)=(False,False,False)
        (Lnot1,Lnot2,Lnot3)=(False,True,False)
        l2=True
        text(1.3,0.93,r"$1$ link",color='k',fontsize=18)
    if mode=='no_2_gc':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,False,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,True,True)
        l2=True
        text(1.3,0.93,r"$1$ link",color='k',fontsize=18)
    if mode=='no_2_gc_no':
        (L,notL)=(True,False)
        (c1,c2,c3)=(True,False,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,False,True)
        l1=True
        text(1.3,0.93,r"$1$ link",color='k',fontsize=18)
    if mode=='gc_no_gc_no_2':
        (L,notL)=(True,True)
        (c1,c2,c3)=(True,True,True)
        (not1,not2,not3)=(True,True,True)
        (Lnot1,Lnot2,Lnot3)=(True,False,True)
        l3=True
        text(1.3,0.93,r"$1$ link",color='k',fontsize=18)

    
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
                text(-.42,.3,r'$G_{\bar{\rm g}}$',color='w',fontsize=23)
                #text(-.6,.23,r'$G$',color='w',fontsize=23)
            elif white:
                w=mpatches.Wedge((r*cos(2.*pi/3),r*sin(2.*pi/3)),r,120,300,fill=True,edgecolor='w',facecolor='w')
                ax.add_patch(w)
            if Lnot3:
                w=mpatches.Wedge((r*cos(2.*pi/3),-r*sin(2.*pi/3)),r,60,240,fill=(not not1),edgecolor='w',facecolor='r')
                ax.add_patch(w)
                #c=mpatches.Circle((-.47,-.2),.3,fill=(not not1),edgecolor='w',facecolor='r')
                #ax.add_patch(c)
                text(-.47,-.37,r'$G_{\bar{\rm b}}$',color='w',fontsize=23)
                #text(-.6,-.35,r'$G$',color='w',fontsize=23)
        if c2:
            if not2:
                w=mpatches.Wedge((0,0),1,240,360,facecolor='g',edgecolor='w')
                ax.add_patch(w)
            if Lnot1:
                w=mpatches.Wedge((r,0.),r,180,360,fill=(not not2),edgecolor='w',facecolor='g')
                ax.add_patch(w)
                text(.35,-.18,r'$G_{\bar{\rm r}}$',color='w',fontsize=23)
                #text(.35,-.3,r'$G$',color='w',fontsize=23)
            if Lnot3:
                w=mpatches.Wedge((r*cos(2.*pi/3),-r*sin(2.*pi/3)),r,240,60,fill=(not not2),edgecolor='w',facecolor='g')
                ax.add_patch(w)
                text(-.22,-.52,r'$G_{\bar{\rm b}}$',color='w',fontsize=23)
                #text(-.2,-.55,r'$G$',color='w',fontsize=23)
        if c3:
            if not3:
                w=mpatches.Wedge((0,0),1,0,120,facecolor='b',edgecolor='w')
                ax.add_patch(w)
            if Lnot1:
                w=mpatches.Wedge((r,0.),r,0,180,fill=(not not3),edgecolor='w',facecolor='b')
                ax.add_patch(w)
                text(.35,.08,r'$G_{\bar{\rm r}}$',color='w',fontsize=23)
                #text(.35,.2,r'$G$',color='w',fontsize=23)
            if Lnot2:
                w=mpatches.Wedge((r*cos(2.*pi/3),r*sin(2.*pi/3)),r,300,120,fill=(not not3),edgecolor='w',facecolor='b')
                ax.add_patch(w)
                text(-.22,.43,r'$G_{\bar{\rm g}}$',color='w',fontsize=23)
                #text(-.2,.45,r'$G$',color='w',fontsize=23)
            elif white:
                w=mpatches.Wedge((r*cos(2.*pi/3),r*sin(2.*pi/3)),r,300,120,fill=True,edgecolor='w',facecolor='w')
                ax.add_patch(w)

    ### plot the chosen parts outside giant component
    if notL:
        if c1:
            w=mpatches.Wedge((1.7,-0.5),.4,120,240,facecolor='r',edgecolor='w')
            ax.add_patch(w)
        if c2:
            w=mpatches.Wedge((1.7,-0.5),.4,240,360,facecolor='g',edgecolor='w')
            ax.add_patch(w)
        if c3:
            w=mpatches.Wedge((1.7,-0.5),.4,0,120,facecolor='b',edgecolor='w')
            ax.add_patch(w)




    ### plot the links and node
    if l1:plot([1.14,1.6],[.83,.8],color='k',lw=2)
    if l2:plot([1.14,1.6],[.67,.8],color='k',lw=2)
    if l3:plot([1.2,1.6],[.5,.8],color='k',lw=2)
    if l4:plot([1.55,1.6],[.4,.8],color='k',lw=2)
    if l5:plot([1.45,1.6],[.45,.8],color='k',lw=2)
    c=mpatches.Circle((1.6,.8),.05,color='k',zorder=10)
    ax.add_patch(c)


    ### complete figure and save
    xlim(-1.1,2.2)
    ylim(-1.03,1.17)
    tight_layout(pad=0.05)
    savefig('sets_1_%s.pdf'%mode)


show()


