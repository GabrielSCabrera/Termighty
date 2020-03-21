import sys
import io

class Tester:

    def __init__(self, category):
        '''
            PURPOSE
            To run a series of tests efficiently, with colorful display that
            improves readability of results
        '''
        self.test_N = 0
        self.passed_N = 0
        self.failed_N = 0
        self.category = category.upper()
        print(f'\n\033[4;1mBEGIN TESTS FOR <{self.category}>\033[m\n')

    def start(self, description = None):
        '''
            PURPOSE
            Run this method to initiate the testing sequence
        '''
        self.test_N += 1

        self.out = '\t{} TEST {} {:>04d}'
        self.description = description.lower()
        if self.description is not None:
            self.out += f' \033[3m{self.description}\033[m'
        status = '\033[1;34;40mINIT\033[m'
        print(self.out.format(status, self.category, self.test_N), end = '')
        sys.stdout.flush()

        # Suppress printing to terminal
        sys.stdout = io.StringIO()

    def passed(self):
        '''
            PURPOSE
            Run this method when a test has passed
        '''
        # Restore printing to terminal
        sys.stdout = sys.__stdout__
        status = '\033[1;32;40mPASS\033[m'
        print('\r' + self.out.format(status, self.category, self.test_N))
        self.passed_N += 1

    def failed(self, traceback = None):
        '''
            PURPOSE
            Run this method when a test has failed
        '''
        # Restore printing to terminal
        sys.stdout = sys.__stdout__
        status = '\033[1;31;40mFAIL\033[m'
        if traceback is not None:
            self.out += (f'\n\n\t     \033[7;31;47mTRACEBACK\033[m\n\t     '
                         f'{traceback}\n')
        print('\r' + self.out.format(status, self.category, self.test_N))
        self.failed_N += 1

    def end(self):
        '''
            PURPOSE
            Run this method when the testing has concluded
        '''
        out = (f'\n\t\033[1mRESULTS FOR <{self.category}>\033[m\n\n\t'
               f'TESTS PASSED \033[32;40m{self.passed_N:>04d}\033[m\n\t'
               f'TESTS FAILED \033[31;40m{self.failed_N:>04d}\033[m')
        print(out)
