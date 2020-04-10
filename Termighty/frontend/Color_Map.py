class Color_Map:

    def __init__(self):
        '''
            PURPOSE
            A superclass that can be inherited in order to create a color map,
            which is a set of colors that are mapped to numerical values
        '''

    def __call__(self, x):
        '''
            PURPOSE
            Not implemented for 'Color_Map', which is an abstract superclass.
            Should be implemented in subclasses of 'Color_Map' with the same
            parameters as above.

            When implemented, accepts a set of N numbers from zero up to and
            including one, and returns a set of N RGB values in an (N,3) array.

            PARAMETERS
            x           array of N floats in range [0,1]

            RETURNS
            rgb         <ndarray> of shape (N,3) of dtype <np.uint8>
        '''
        msg = ('\nClass \'Color_Map\' is an abstract class that must be '
               'inherited.  Create a subclass with a \'__call__\' method and '
               'use that instead.')
        raise NotImplementedError(msg)
