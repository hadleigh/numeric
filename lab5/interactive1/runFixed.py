import numlabs.lab5.lab5_funs
from importlib import reload
reload(numlabs.lab5.lab5_funs)
from numlabs.lab5.lab5_funs import Integrator
from collections import namedtuple


class Integ51(Integrator):

    def set_yinit(self):
        initvars = namedtuple('initvars', 'whiteconc blackconc')
        self.initvars = initvars(**self.config['initvars'])
        self.yinit = np.array(
            [self.initvars.whiteconc, self.initvars.blackconc])
        self.nvars = len(self.yinit)
        return None

    def __init__(self, coeffFileName):
        super().__init__(coeffFileName)
        self.set_yinit()

    def derivs5(self, y, t):
        """y[0]=fraction white daisies
           y[1]=fraction black daisies
        """
        u = self.uservars
        x = 1.0 - y[0] - y[1]

        # growth rates don't depend on temperature
        beta_b = 0.1  # growth rate for black daisies
        beta_w = 0.7  # growth rate for white daisies

        # create a 1 x 2 element vector to hold the derivitive
        f = np.empty([self.nvars], 'float')
        f[0] = y[0] * (beta_w * x - u.chi)
        f[1] = y[1] * (beta_b * x - u.chi)
        return f


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    theSolver = Integ51('fixed.yaml')
    theSolver.set_yinit()
    print('theSolver: debug: ', theSolver.yinit)
    timeVals, yVals, errorList = theSolver.timeloop5fixed()

    thefig = plt.figure(1)
    thefig.clf()
    theAx = thefig.add_subplot(111)
    theLines = theAx.plot(timeVals, yVals)
    theLines[0].set_marker('+')
    theLines[1].set_linestyle('--')
    theLines[1].set_color('k')
    theLines[1].set_marker('*')
    theAx.set_title('lab 5 interactive 1 fixed')
    theAx.set_xlabel('time')
    theAx.set_ylabel('fractional coverage')
    theAx.legend(theLines, ('white daisies', 'black daisies'), loc='best')

    thefig = plt.figure(2)
    thefig.clf()
    theAx = thefig.add_subplot(111)
    theLines = theAx.plot(timeVals, errorList)
    theLines[0].set_marker('+')
    theLines[1].set_linestyle('--')
    theLines[1].set_color('k')
    theLines[1].set_marker('*')
    theAx.set_title('lab 5 interactive 1 fixed errors')
    theAx.set_xlabel('time')
    theAx.set_ylabel('fractional coverage')
    theAx.legend(theLines, ('white errors', 'black errors'), loc='best')

    plt.show()
