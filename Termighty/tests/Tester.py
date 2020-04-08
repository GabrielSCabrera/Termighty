import inspect
import sys
import io

class Tester:

    def __init__(self, category, dev = False):
        '''
            PURPOSE
            To run a series of tests efficiently, with colorful display that
            improves readability of results.

            PARAMETERS
            category        <str>
        '''
        self.test_N = 0
        self.passed_N = 0
        self.failed_N = 0
        self.dev = dev
        self.category = category.upper()
        print(f'\n\033[4;1mBEGIN TESTS FOR <{self.category}>\033[m\n')

    def start(self, description = None):
        '''
            PURPOSE
            Run this method to initiate the testing sequence.

            PARAMETERS
            description     <str>
        '''
        self.test_N += 1

        self.out = '\t{} TEST \033[3m{}\033[m \033[2m[{:>04d}]\033[m'
        self.description = description
        if self.description is not None:
            self.out += f' \033[3m{self.description}\033[m'
        status = '\033[1;34;40mINIT\033[m'
        print(self.out.format(status, self.category, self.test_N), end = '')
        sys.stdout.flush()

        # Suppress printing to terminal
        if not self.dev:
            sys.stdout = io.StringIO()

    def passed(self):
        '''
            PURPOSE
            Run this method when a test has passed
        '''
        # Restore printing to terminal
        if not self.dev:
            sys.stdout = sys.__stdout__
        status = '\033[1;32;40mPASS\033[m'
        print('\r' + self.out.format(status, self.category, self.test_N))
        self.passed_N += 1

    def failed(self, traceback = None):
        '''
            PURPOSE
            Run this method when a test has failed

            PARAMETERS
            traceback       <str>
        '''
        # Getting line where issue arises
        frameinfo = inspect.getframeinfo(inspect.currentframe().f_back)
        # Restore printing to terminal
        if not self.dev:
            sys.stdout = sys.__stdout__
        status = '\033[1;31;40mFAIL\033[m'
        self.out += (f' \033[1;31;40mline:{frameinfo.lineno}\033[m in '
                     f'file \033[1;31;40m{frameinfo.filename}\033[m')
        if traceback is not None:
            self.out += (f'\n\n\t     \033[7;31;47mTRACEBACK\033[m\n\t     '
                         f'{traceback}\n')
        print('\r' + self.out.format(status, self.category, self.test_N))
        self.failed_N += 1

    def end(self):
        '''
            PURPOSE
            Run this method when the testing has concluded

            RETURNS
            results         <dict>
        '''

        print(self.results(self.passed_N, self.failed_N, self.category))

        results = {
                   'passed'     :   self.passed_N,
                   'failed'     :   self.failed_N
                  }

        return results

    @classmethod
    def results(cls, passed, failed, name = None):
        '''
            PURPOSE
            To display the results of the testing

            PARAMETERS
            passed          <int>
            failed          <int>
            name            <str>

            RETURNS
            out             <str>
        '''

        if name is None:
            out = f'\n\t\033[1mRESULTS\033[m\n\n\t'
        else:
            out = f'\n\t\033[1mRESULTS FOR <{name}>\033[m\n\n\t'

        out +=  (f'TESTS PASSED \033[32;40m{passed:>04d}\033[m\n\t'
                 f'TESTS FAILED \033[31;40m{failed:>04d}\033[m')

        return out
