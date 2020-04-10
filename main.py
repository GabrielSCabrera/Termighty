import Termighty as tm
import argparse

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
    help_run = 'Runs the main script'

    parser.add_argument('--test', action = 'store_true', help = help_test)
    parser.add_argument('--calibrate', action = 'store_true',
                        help = help_calibrate)
    parser.add_argument('--logo', action = 'store_true', help = help_logo)
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
    results['color_maps']  = tm.tests.test_color_maps()
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
    tm.samples.logo()
if cmdline_args.run is True:
    procedure_main()
