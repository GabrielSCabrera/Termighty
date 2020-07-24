import numpy as np
import argparse

import Termighty as tm

def parse_args():
    '''
        PURPOSE
        To parse and return command-line arguments

        RETURNS
        Instance of <class 'argparse.Namespace'>
    '''
    argparse_desc = ('Runs various aspects of the rock fracture analysis '
                     'depending on the sequence of included command-line '
                     'arguments.')

    parser = argparse.ArgumentParser(description = argparse_desc)

    help_test = 'Runs all automatic unit tests'
    help_calibrate = 'Runs all display tests that require visual inspection'
    help_logo = 'Displays the Termighty logo'
    help_plot = 'Allows the user to create & display a plot interactively'
    help_run = 'Runs the main script'

    parser.add_argument('--test', action = 'store_true', help = help_test)
    parser.add_argument('--calibrate', action = 'store_true',
                        help = help_calibrate)
    parser.add_argument('--logo', action = 'store_true', help = help_logo)
    parser.add_argument('--plot', action = 'store_true', help = help_plot)
    parser.add_argument('--run', action = 'store_true', help = help_run)

    return parser.parse_args()

def procedure_test():
    '''
        PURPOSE
        Runs all unit tests
    '''
    results = {}
    results['Color'] = tm.tests.test_Color()
    results['Style'] = tm.tests.test_Style()
    results['Pixel'] = tm.tests.test_Pixel()
    results['Grid']  = tm.tests.test_Grid()
    results['Term']  = tm.tests.test_Term()
    results['Series']  = tm.tests.test_Series()
    results['Window']  = tm.tests.test_Window()
    results['Color_Map']  = tm.tests.test_Color_Map()
    results['Gradient']  = tm.tests.test_Gradient()

    final_tally = {'passed':0, 'failed':0}
    for key, value in results.items():
        final_tally['passed'] += value['passed']
        final_tally['failed'] += value['failed']

    out = '\n\033[1;4mFINAL TALLY\033[m\n'
    out += tm.tests.Tester.results(final_tally['passed'], final_tally['failed'])

    print(out)

def procedure_calibrate():
    '''
        PURPOSE
        Runs all display tests that require manual inspection
    '''
    tm.tests.calibrate_Color()
    tm.tests.calibrate_Style()
    tm.tests.calibrate_Pixel()
    tm.tests.calibrate_Grid()
    msg = 'PRESS ENTER TO BEGIN TERMINAL AND WINDOW CALIBRATION'
    input(f'\n\033[30;47;4m{msg}\033[m')
    tm.tests.calibrate_Term()
    tm.tests.calibrate_Window()

def procedure_logo():
    tm.samples.logo()

def procedure_plot():
    msg = 'Enter a real-valued number for x_minimum\n> '
    x_min = float(input(msg))
    msg = 'Enter a real-valued number for x_maximum\n> '
    x_max = float(input(msg))
    msg = 'Enter a real-valued number for y_minimum\n> '
    y_min = float(input(msg))
    msg = 'Enter a real-valued number for y_maximum\n> '
    y_max = float(input(msg))
    msg = 'Enter a mathematically evaluatable function of \'x\' and \'y\'\n> '
    fxn = input(msg)
    if fxn.lower() == 'franke':

        def frankes_function(x,y):
            term1 = 0.75*np.exp(-(0.25*(9*x-2)**2) - 0.25*((9*y-2)**2))
            term2 = 0.75*np.exp(-((9*x+1)**2)/49.0 - 0.1*(9*y+1))
            term3 = 0.5*np.exp(-(9*x-7)**2/4.0 - 0.25*((9*y-3)**2))
            term4 = -0.2*np.exp(-(9*x-4)**2 - (9*y-7)**2)
            return term1 + term2 + term3 + term4

        class Plot(tm.Gradient):
            def __call__(self, x, y, t):
                return frankes_function(x,y)

    elif fxn.lower() == 'ripple':

        def ripple(x,y):
            return np.sin(10*(x**2 + y**2))

        class Plot(tm.Gradient):
            def __call__(self, x, y, t):
                return ripple(x,y)
    else:

        class Plot(tm.Gradient):
            def __call__(self, x, y, t):
                return eval(fxn)

    color_map = tm.Linear_Map('black', 'blue')
    plot = Plot((24,80), (x_min, x_max), (y_min, y_max), color_map)
    print(plot.__str__() + '\033[m')

def procedure_main():
    '''
        PURPOSE
        Contains the main program code
    '''
    pass

cmdline_args = parse_args()

if cmdline_args.test is True:
    procedure_test()
if cmdline_args.calibrate is True:
    procedure_calibrate()
if cmdline_args.logo is True:
    procedure_logo()
if cmdline_args.plot is True:
    procedure_plot()
if cmdline_args.run is True:
    procedure_main()
