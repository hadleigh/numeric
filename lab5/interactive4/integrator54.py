import numlabs.lab5.lab5_funs
from importlib import reload
reload(numlabs.lab5.lab5_funs)
from numlabs.lab5.lab5_funs import Integrator
from collections import namedtuple
import numpy as np


class Integ54(Integrator):

    def set_yinit(self):
        uservars = namedtuple(
            'uservars', 'albedo_white chi S0 L albedo_black R albedo_ground')
        self.uservars = uservars(**self.config['uservars'])
        initvars = namedtuple('initvars', 'whiteconc blackconc')
        self.initvars = initvars(**self.config['initvars'])
        self.yinit = np.array(
            [self.initvars.whiteconc, self.initvars.blackconc])
        self.nvars = len(self.yinit)
        return None

    def __init__(self, coeffFileName):
        super().__init__(coeffFileName)
        self.set_yinit()

    def find_temp(self, yvals):
        sigma = 5.67e-8  # Stefan Boltzman constant W/m^2/K^4
        u = self.uservars
        x = 1.0 - yvals[0] - yvals[1]
        albedo_p = x * u.albedo_ground + \
            yvals[0] * u.albedo_white + yvals[1] * u.albedo_black
        Te_4 = u.S0 / 4.0 * u.L * (1.0 - albedo_p) / sigma
        temp_e = Te_4**0.25
        eta = u.R * u.S0 / (4.0 * sigma)
        temp_b = (eta * (albedo_p - u.albedo_black) + Te_4)**0.25
        temp_w = (eta * (albedo_p - u.albedo_white) + Te_4)**0.25
        return (temp_w, temp_b, temp_e)

    def derivs5(self, y, t):
        """y[0]=fraction white daisies
           y[1]=fraction black daisies
           no feedback between daisies and
           albedo_p (set to ground albedo)
        """
        temp_w, temp_b , temp_e = self.find_temp(y)

        if(temp_b >= 277.5 and temp_b <= 312.5):
            beta_b = 1.0 - 0.003265 * (295.0 - temp_b)**2.0
        else:
            beta_b = 0.0

        if(temp_w >= 277.5 and temp_w <= 312.5):
            beta_w = 1.0 - 0.003265 * (295.0 - temp_w)**2.0
        else:
            beta_w = 0.0
        u = self.uservars
        x = 1.0 - y[0] - y[1]
        # create a 1 x 2 element vector to hold the derivitive
        f = np.empty_like(y)
        f[0] = y[0] * (beta_w * x - u.chi)
        f[1] = y[1] * (beta_b * x - u.chi)
        return f
