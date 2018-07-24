# autotesting

This is a low-footprint, fully self-contained extension to the standard PyUnit testing 
framework. The main features are:

  * fully automatic collection of test cases from a package
  * filtering and grouping of test cases by 'tags' and sub-packages
  * test execution automatically kicks in if a module is run stand-alone
  * test variables are pushed into global name space for interactive debugging
  * the test module doubles as script for running the tests

Originally, our testing code was simply in the `__main__` section of each
module where we could execute it directly from emacs (or with `python
-i`) for interactive debugging. By comparison, unittest test fixtures
are less easy to execute stand-alone and intermediate variables remain
hidden within the test instance. 

The `localTest()` method removes this hurdle and runs the test code of a
single module as if it would be executed directly in `__main__`. Simply putting
the `localTest()` function without parameters into the `__main__` section of your
module is enough. Your `Test.test_*` methods should assign intermediate and
final results to `self.|something|` variables `localTest` will then push all
`self.*` fields into the global namespace for interactive debugging.

To get started, every module in your package should contain one or more classes
derrived from `AutoTest` (conventionally called `Test`) that
each contains one or more `test_*` functions. `AutoTestLoader` then
automatically extracts all `AutoTest` child classes from the whole
package and bundles them into a `FilteredTestSuite`. Note, `AutoTest` is 
derrived from the standard `unittest.TestCase` -- refer to the Python 
documentation for details on test writing.

Setup
=====

1. Copy `testing.py` into your own python package.
2. Adapt the module-level parameter `DEFAULT_PACKAGES`

   E.g. if the name of your package (folder) is `superpy` and it also contains a sub-package (sub-folder) `superpy.tools`::
   
       DEFAULT_PACKAGES = ['superpy', 'superpy.tools']

3. Define Unittest classes derived from `testing.AutoTest` in your code.
4. Add the `localTest()` method in the `__main__` block of your modules -- see details below

Adapting your code
==================

  By way of example, a Test case for MyModule would look like this:
```python
    class MyClass:
        ...

    ### Module testing ###
    import testing

    class Test(testing.AutoTest):
        """Test MyModule"""

        TAGS = [ testing.LONG ]

        def test_veryLongComputation( self ):
            """MyModule.veryLongComputation test"""

            self.m = MyClass()
            self.result = self.m.veryLongComputation()

            if self.local:   ## only if the module is executed directly
                print(self.result) 
                
            self.assertEqual( self.result, 42, 'unexpected result' )


    if __name__ == '__main__':

        ## run Test and push self.* fields into global namespace
        testing.localTest( )

        print(result)  ## works thanks to some namespace magic in localTest
```

Note:

  - If TAG is not given, the test will have the default `NORMAL` tag.
  - Names of test functions **must** start with `test_`.
  - The doc string of `test_*` will be reported as id of this test.

Running Tests
=============

The module also acts as the script to collect and run the tests. Run it without
arguments for help. In the simplest case, the following will execute all the tests
found in any module of your package and sub-package, except any tests tagged as 'OLD':

    ./testing.py -e old

The following command will execute all the tests from a single sub-package:

    ./testing.py -p superpy.tools

Run `./testing.py` without arguments to see the complete help::

    Run unittest tests for the whole package.

        testing.py [-i |include tag1 tag2..| -e |exclude tag1 tag2..|
                    -p |package1 package2..|
                    -v |verbosity| -log |log-file| -nox ]

        i    - include tags, only run tests with at least one of these tags   [All]
        e    - exclude tags, do not run tests labeled with one of these tags  [old]
             valid tags are:
                 long   - long running test case
                 pvm    - depends on PVM
                 exe    - depends on external application
                 old    - is obsolete
             (If no tags are given to -i this means all tests are included)

        p    - packages to test, e.g. mypackage mypackage.parser           [All]
        v    - int, verbosity level, 3 switches on several graphical plots      [2]
        log  - path to logfile (overriden); empty -log means STDOUT        [STDOUT]
        nox  - suppress test plots                                          [False]
        dry  - do not actually run the test but just collect tests          [False]

    Examples:

        * Run all but long or obsolete tests from mypackage and mypackage.parser:
        ./testing.py -e old long -p mypackage mypackage.parser

        * Run only PVM-dependent tests of the mypackage.calc sub-package:
        ./testing.py -i pvm -p mypackage.calc

