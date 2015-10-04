import numlabs.lab5.lab5_funs
from importlib import reload
reload(numlabs.lab5.lab5_funs)
import integrator54
reload(integrator54)
from integrator54 import Integ54

if __name__=="__main__":
    import matplotlib.pyplot as plt
    import pandas as pd
 
    theSolver=Integ54('daisy4.yaml')
    timevals,yvals,errorlist = theSolver.timeloop5Err()
    out=[theSolver.find_temp(y) for y in list(yvals)]
    daisies = pd.DataFrame(yvals,columns = ['white', 'black'])
    temp = pd.DataFrame(out,columns=['white','black','avg'])
    thefig,theAx=plt.subplots(1,1)
    line1,=theAx.plot(timevals,daisies['white'])
    line2,=theAx.plot(timevals,daisies['black'])
    line1.set(linestyle = '--',color='r',label='white')
    line2.set(linestyle = '--',color='k',label='black')
    theAx.set_title('lab 5 interactive 4')
    theAx.set_xlabel('time')
    theAx.set_ylabel('fractional coverage')
    theAx.legend(loc='center right')
    thefig,theAx=plt.subplots(1,1)
    line1,=theAx.plot(timevals,temp['white'])
    line2,=theAx.plot(timevals,temp['black'])
    line3,=theAx.plot(timevals,temp['avg'])
    line1.set(linestyle = '--',color='r',label='white')
    line2.set(linestyle = '--',color='k',label='black')
    line3.set(linestyle = '--',color='b',label='avg')
    theAx.set(title = 'temperatures', xlabel = 'time', ylabel = 'temperatures (K)')
    plt.show()
    
