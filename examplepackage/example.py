import time

## write your code as always...
class MyClass:

    def shortComputation(self):
        return 1 + 1

    def longComputation(self):
        time.sleep(3)
        return 6 * 7

### Module testing ###
import testing

class Test(testing.AutoTest):
    """Example Test"""

    TAGS = [ testing.LONG ]

    def test_longComputation( self ):
        """example.longComputation test"""

        self.m = MyClass()
        self.result = self.m.longComputation()

        if self.local:   ## only if the module is executed directly
            print('long computation result: %r' % self.result) 

        self.assertEqual( self.result, 42, 'unexpected result' )


    def test_shortComputation(self):
        """example.shortComputation test"""

        self.m = MyClass()
        self.result_short = self.m.shortComputation()

        if self.local:   ## only if the module is executed directly
            print('short computation result: %r' % self.result_short) 

        self.assertEqual( self.result_short, 2, 'unexpected result' )
        
    
if __name__ == '__main__':

    ## run Test and push self.* fields into global namespace
    testing.localTest( )

    ## works thanks to some namespace magic in localTest
    print('The last result of the last test was\n %r' % result)  
