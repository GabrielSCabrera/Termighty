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

    help_test = 'Runs all unit tests'
    help_logo = 'Displays the Termighty logo'
    help_run = 'Runs the main script'

    parser.add_argument('--test', action = 'store_true', help = help_test)
    parser.add_argument('--logo', action = 'store_true', help = help_logo)
    parser.add_argument('--run', action = 'store_true', help = help_run)

    return parser.parse_args()

cmdline_args = parse_args()

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

    final_tally = {'passed':0, 'failed':0}
    for key, value in results.items():
        final_tally['passed'] += value['passed']
        final_tally['failed'] += value['failed']

    out = '\n\033[1;4mFINAL TALLY\033[m\n'
    out += tm.tests.Tester.results(final_tally['passed'], final_tally['failed'])

    print(out)

def procedure_main():
    '''
        PURPOSE
        Contains the main program code
    '''
    pass

if cmdline_args.test is True:
    procedure_test()
if cmdline_args.logo is True:
    tm.samples.logo()
if cmdline_args.run is True:
    procedure_main()
