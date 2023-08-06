from scipy.optimize import curve_fit
from scipy.special import wofz as _wofz
#from scipy.special import erfc as _erfc

import numpy as _np
import warnings as _warnings
_warnings.simplefilter('ignore', _np.RankWarning)

####### list manipulation #######

def _reverse(data):
    return [data[i] for i in range(len(data)-1, -1, -1)]

####### statistical functions #######

def _variance(data, order = 0):
    if order == 0:
        return _np.var(data)
    else:
        return _np.var([data[i + order] + data[i - order] - 2 * data[i] for i in range(order, len(data) - order)]) / 6

def _standard_deviation(data, order = 0):
    return _np.sqrt(_variance(data, order))

####### curve functions #######

def poly(x, *args):
    pol = 0
    for i in range(len(args)):
        pol += args[i] * _np.power(x, i)
    return pol

_kg = 0.3989422804014327  # kg = (2 * _np.pi) ** (-1/2) = 0.398...
def gaussian(nu, g):
    if g == 0:
        return 1 * (nu == 0)
    return _kg * g ** -1 * _np.exp(- 0.5 * (nu / g) ** 2)

_kl = 0.3183098861837907 # kl = 1/ _np.pi = 0.318...
def lorentian(nu, l):
    if l == 0:
        #return 1 if nu == 0 else 0
        return 1 * (nu == 0)
    return _kl * l * (1 / (nu ** 2 + l ** 2))

_kv = 0.70710678118654746
def voigt(nu, g, l):
    if g == 0:
        return lorentian(nu, l)
    if l == 0:
        return gaussian(nu, g)
    z = _kv * (nu + 1j * l) / g
    w = _wofz(z)
    return _kg * w.real / g


#ef voigt2(nu, g, l):
#    z = kv * (nu + 1j * l) / g
#    w = _np.exp(- z ** 2) * erfc(-1j * z)
#    return kg * w.real / g

#diff = lambda g, l: 1. * (l - g)/(l + g)
#cl = lambda d: 0.68188 + 0.61293 * d - 0.18384 * d**2 - 0.11568 * d**3
#cg = lambda d: 0.32460 - 0.61825 * d + 0.17681 * d**2 + 0.12109 * d**3
#sigma_v = lambda g, l: 0.5 * (1.0692 * l + _np.sqrt(0.86639 * l**2 + 4 * g**2))

#def voigt_approximation(nu, g, l):
#    d = diff(g, l)
#    kl = cl(d)
#    kg = cg(d)
#    sv = sigma_v(g, l)
#    return kl * lorentian(nu, sv) + kg * gaussian(nu, sv)

####### averaging  #######

def _mean(data):
    return sum(data) / len(data)

def moving_average(data, window = 1, order = 1):
    l = len(data)
    data = _continuation(data, window, order)
    g = _np.array([1 for i in range(2 * window + 1)])
    return list(_np.convolve(data, g, mode = "same")[window: window + l] / (2 * window + 1))

def gaussian_average(data, sigma = 1, n = 3, order = 0):
    l = len(data)
    ns = n * sigma
    data = _continuation(data, ns, order)
    g = _np.array([gaussian(i, sigma) for i in range(-ns, ns + 1)])
    return list(_np.convolve(data, g, mode = "same")[ns: ns + l] / _np.sum(g))

####### data manipulation #######

def _closest(data, value):
    data = _np.array(data) - value
    data = _np.where(_np.diff(_np.sign(data)))[0]
    return list(data)

def _derivative(data, order = 1):
    if order == 0:
        return  data
    first = data[1] - data[0]
    last = data[-1] - data[-2]
    d = [first] + [(data[i + 1] - data[i - 1]) / 2 for i in range(1, len(data) - 1)] + [last]
    return derivative(d, order - 1)

def _continuation(data, n = 1, order = 1):
    if n == 0:
        return data
    l = len(data)
    n_new = n + order
    x1 = [i for i in range(len(data)) if i in range(0, n_new)]
    x2 = [i for i in range(len(data)) if i in list(range(l - n_new, l))]
    y1 = [data[i] for i in range(len(data)) if i in x1]
    y2 = [data[i] for i in range(len(data)) if i in x2]
    fit1 = _reverse(_np.polyfit(x1, y1, order))
    fit2 = _reverse(_np.polyfit(x2, y2, order))
    fit_data1 = [poly(i, *fit1) for i in range(-n, 0)]
    fit_data2 = [poly(i, *fit2) for i in range(l, l + n)]
    data =  fit_data1 + list(data) + fit_data2
    return data

def _detrend(data, order = 2, window = 1):
    if window == 0:
        return _detrend(data, 1, 1)
    l = len(data)
    pos = [i for i in range(l) if i < window or l - 1 - i < window]
    data_l = [data[i] for i in pos]
    fit_l = _reverse(_np.polyfit(pos, data_l, order))
    data_l = [poly(i, *fit_l) for i in range(l)]
    mean_l = _mean(data_l)
    data = [data[i] - data_l[i] for i in range(l)]
    return data

####### peak detection  #######

_c2 = 2 * _np.sqrt(2 * _np.log(2))
def _full_width(g, l): #fwhm
    g = _c2 * g
    l = 2 * l
    width = 0.5346 * l + _np.sqrt(0.2166 * l ** 2 + g ** 2)
    return width

def _peak_guess(data):
    m = max(data)
    p_center = round(int(_mean(_closest(data, m))))
    a = data[p_center]
    p_left = _closest(data[0 : p_center], m / 2)
    p_right = _closest(data[p_center : ], m / 2)
    if p_left != [] and p_right != []:
        p_left = p_left[-1]
        p_right = p_center + p_right[-1]
        return a, p_center, (p_right - p_left)
    else:
        print(_set_color("warning: initial guess not trusted", "orange"))
        return None, None, None

def _peak_detection(data, peak_ratio = 0.1):
    l = len(data)
    window = int(round(0.1 * l))
    data_d = _detrend(data, 3, window)
    sigma = int(round(peak_ratio * l / 8))
    data_g = gaussian_average(data_d, sigma, 2)
    
    a, c, width = _peak_guess(data_g)
    if a != None and width != None:
        if a < 2 * _standard_deviation(data, 1) or width > int(round(0.9 * l)):
            print(_set_color("warning: initial guess not trusted", "orange"))
            a, c, width = None, None, None
    if width != None:
        kg = voigt(0, width/(2 * _c2), width / (2 * 2))
        if width > _c2 * sigma:
            width = _np.sqrt(width ** 2 - (_c2 * sigma) ** 2)
        k = voigt(0, width/(2 * _c2), width / (2 * 2))
        a = a * k / kg
    return a, c, width

def fit_voigt(x, y, peak_ratio = 0.1, background = 1, a = None, p = None, g = None, l = None):   
    x, y = _np.array(x), _np.array(y)
    
    std = _standard_deviation(y, 1)
    a_min, a_max = 0, 2 * (max(y) - min(y))
    xc_min, xc_max = min(x), max(x)
    g_min, g_max = 0, 1 * (max(x) - min(x))
    l_min, l_max = g_min, g_max

    ai, ci, width = _peak_detection(y, peak_ratio)
    n = len(y)
    if ai == None:
        ai, ci, width = std, int(round(n / 2)), int(round(0.9 * n))
    xc = x[ci]
    width = (max(x) - min(x)) * width / n
    width_g = width / 2
    width_l = width / 2
    gi, li =  width_g / _c2, width_l / 2

    fit_l = []
    if background != None and background >= 0:
        left , right = ci - int(round(width / 2)), ci + int(round(width / 2))
        x_l = [x[i] for i in range(n) if  i < left or i > right]
        y_l = [y[i] for i in range(n) if  i < left or i > right]
        fit_l = _reverse(_np.polyfit(x_l, y_l, background))
        fit_l = [fit_l[i] * n ** i for i in range(background + 1)]

    voigt_model = lambda nu, a, nu_0, g, l, *args: a * voigt(nu - nu_0, g, l) / voigt(0, g, l) + poly(nu / n, *args)
    gh = _np.arange(0, len(y), len(y) / 30)
    
    iniz = [ai, xc, gi, li] + fit_l
    lb = [a_min, xc_min, g_min , l_min]  # lower bounds
    ub = [a_max, xc_max, g_max, l_max]  # upper bounds
    lb += [-_np.inf] * (len(iniz) - 4)
    ub += [_np.inf] * (len(iniz) - 4)

    var = _np.array([a, p, g, l] + [None] * (len(iniz) - 4))
    iniz = _np.array(iniz)[var == None]
    lb = _np.array(lb)[var == None]
    ub = _np.array(ub)[var == None]
    bounds = (tuple(lb), tuple(ub))

    fit_model = lambda nu, *args: voigt_model(nu, *_old_var(args, var))
    
    try:
        fit, cov = curve_fit(fit_model, x, y, p0 = iniz, maxfev = 5 * 10 ** 4, method = "trf", bounds = bounds)
        err = _np.sqrt(_np.diag(cov))
    except:
        print(_set_color("warning: fit failed", "red"))
        fit = iniz
        err = _np.array(ub) - _np.array(lb)
    fit, err = list(fit), list(err)
    y_f = [fit_model(nu, *fit) for nu in x]

    iniz = _old_var(iniz, var)
    fit = _old_var(fit, var)
    err = _old_var(err, [el if el == None else 0 for el in var])

    err_f = _np.sqrt(_mean([(y[i] - y_f[i]) ** 2 for i in range(n)]))
    snr = fit[0] / err_f
    #snr = snr * (std / err_f) ** (std / err_f)

    _print_fit(fit, err, iniz)
    _print_snr(snr)
    #print(round((err_f / err[0]) ** 2, 2))
    
    return fit, err, snr, y_f

def _old_var(new_var, var): #where var is None, old_
    old = [0] * len(var)
    j = 0
    for i in range(len(var)):
        if var[i] == None:
            old[i] = new_var[j]
            j += 1
        else:
            old[i] = var[i]
    return _np.array(old)
    
fit_gaussian = lambda x, y, peak_ratio = 0.1, background = 1, a = None, p = None, g = None: fit_voigt(x, y, peak_ratio, background, a = a, p = p, g = g, l = 0)

fit_lorentian = lambda x, y, peak_ratio = 0.1, background = 1, a = None, p = None, l = None: fit_voigt(x, y, peak_ratio, background, a = a, p = p, g = 0, l = l)

def _print_fit(fit, err, iniz):
    l = len(iniz)
    header = ["amplitude", "position", "gaussian", "lorentian"]
    header += ["background" + str(i) for i in range(0, l - 4)]
    header = _list_to_string(header, "right")
    
    per = [100 * abs(err[i] / fit[i]) if fit[i] != 0 else _np.inf for i in range(l)]
    per = [el if el <= 100 else ">100" for el in per]

    fit = _list_to_string(fit, "left", dec = 1)
    err = _list_to_string(err, "left", dec = 2)
    per = _list_to_string(per, "right", dec = 1)
    iniz = _list_to_string(iniz, "left", dec = 1)

    for i in range(len(header)):
        print(header[i] + " " + fit[i] + " ± " + err[i] + " (" + per[i] + " %) [initial guess:" + iniz[i] + "]")
        if i == 3:
            pass
            #print()
    #print()

####### string manipulation #######

def _add_spaces(string, length = 1, where = "left"):
    spaces = " " * (length - len(string))
    if where == "left":
        string = spaces + string
    elif where == "right":
        string += spaces
    return string

def _round_list(data, dec = 1):
    data = list(data)
    for i in range(len(data)):
        t = str(type(data[i]))
        if "float" in t or "int" in t:
            data[i] = round(float(data[i]), dec)
    return data

def _list_to_string(data, where = "left", dec = 1):
    data = _round_list(data, dec)
    data = list(map(str, data))
    spaces = max(map(len, data)) + 1
    return [_add_spaces(el, spaces, where) for el in data]

_colors = ['norm', 'black', 'gray', 'red', 'green', 'yellow', 'orange', 'blue', 'violet', 'cyan', 'bold']
_color_codes = [0, 30, 2, 91, 92, 93, 33, 94, 95, 96, 1]
    
# it applies the proper color codes to a string
def _set_color(text = "", color = "norm"):
    code = '\033['
    if type(color) == str:
        for c in range(len(_colors)):
            if color == _colors[c]:
                code += str(_color_codes[c])
    code += 'm'
    return code + text + '\033[0m'

def _print_snr(snr):
    string = "fit snr: " + str(round(snr, 1))
    if snr < 10:
        print(_set_color(string, "red"))
    elif snr < 30:
        print(_set_color(string, "orange"))
    else:
        print(_set_color(string, "green"))

def run_test():
    n = 1000
    std = 0.01
    a, p0, g, l = 1, n / 2, (n / 5) / (2 * _c2), (n / 5) / (2 * 2)
    v0 = voigt(0, g, l)
    yv = [a * voigt(n - p0, g, l) / v0  for n in range(0, n)]
    coeff = [1, - 1 / n,  0 / n ** 2]
    yp = [poly(el, *coeff) for el in range(n)]
    yn = _np.random.randn(n) * std
    y = _np.sum([yv, yp, yn], axis = 0)
    yf = fit_voigt(range(n), y, peak_ratio = 1/5, background = 1)[-1]

#    import matplotlib.pyplot as plt
#    plt.clf()
#    plt.plot(y , c = "gray", zorder = 0)
#    plt.plot(yf, c = "tab:blue", zorder = 1)
#    plt.show(block = 0)

fit_voigt.__doc__ = """It fits the data to a single voigt profile with polynomial background. The data should contain a single peak, not larger then the data set. Here is a basic example:

   \x1b[92mimport peaky\x1b[0m
   \x1b[92mpeaky.fit_voigt(x, y)\x1b[0m

where x and y are respectively the independent and dependent variable. Here are all other parameters: 

\x1b[94mbackground\x1b[0m
It sets the order of the polynomial to helps the fit adapt to a possible background signal. A value of 0 means constant background, a value of 1 means linear background etc. If None is provided, no background is added. The dafault value is 1. 

\x1b[94ma\x1b[0m
It sets the amplitude of the voigt peak to the value provided. In this context, amplitude means literally the amplitude of the signal at peak position. If None is provided (as by default) the best amplitude is found by the fit. 

\x1b[94mp\x1b[0m
It sets the peak position to the value provided. If None is provided (as by default) the best peak position is found by the fit. 

\x1b[94mg\x1b[0m
It sets the voigt gaussian width to the value provided. If None is provided (as by default) the best gaussian width is found by the fit. 

\x1b[94ml\x1b[0m
It sets the voigt lorentian width to the value provided. If None is provided (as by default) the best lorentian width is found by the fit. 

\x1b[94mpeak_ratio\x1b[0m
This parameters helps the process find the best initial values for the fit. For example, a value of 0.3 means then the peak occupies roughly 1 / 3 of the data set width (estimated by eye). If a lower value is provided, the noise may ruin the peak detection, while a higher value may average away the signal. 

\nThese are the outputs of the fit:

\x1b[33mfit\x1b[0m
The optimal values of the fit parameters in this order: amplitude, peak position, gaussian and lorentian width. After it follows the list of polynomial coefficients used for the background signal from lower to higher order. Note that each background coefficient (being very small for higher orders) is multiplied by the n ** i where, n is the length of the signal and i is the order of the coefficient. 

\x1b[33merr\x1b[0m
The errors for each of the previous parameters obtained from the fit.

\x1b[33msnr\x1b[0m
The fit signal to noise measured as the ratio between the signal amplitude (obtained from fit) and the fit data noise. This parameter may help decide whatever or not a fit is reliable. 

\x1b[33myf\x1b[0m
The list of fitted data values that can be used, for example, for a plot.

\nAll measured parameters are printed directly on terminal together with their error bars and guessed initial values. A color coded fit signal to noise ratio may help decide if a fit is reliable. Red means unreliable, orange means not optimal, while green means reliable. 

"""


fit_gaussian.__doc__ = """It is equivalent to the fit_voigt function with lorentian width parameter l fixed to 0. Access the fit_voigt function doc string for full documentation. """

fit_lorentian.__doc__ = """It is equivalent to the fit_voigt function with gaussian width parameter g fixed to 0. Access the fit_voigt function doc string for full documentation. """
