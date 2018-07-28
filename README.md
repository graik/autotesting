# autotesting

This is a very low-footprint extension to the standard PyUnit testing
framework. Simply copy the `testing.py` file from the `examplepackage` folder
into your own python package, adapt the `DEFAULT_PACKAGES` variable and your are
ready to rock.

The main features are:

  * fully automatic discovery of test cases from your package (without registration)
  * filtering and grouping of test cases by 'tags' and sub-packages
  * run all or selected tests using `testing.py` as a script or ...
  * ... execute tests of a given module by simply executing this module
  * test variables are pushed into global name space for interactive debugging
  * other tools supporting standard unittest will still work (e.g. WingIDE still
    identifies and runs `testing.AutoTest` classes as `unittest` instances)

This testing module was originally developed for the biskit python library
(https://github.com/graik/biskit) where we have been happily using and improving
it for the last 15 or such years. autotest is a only slightly modified
stand-alone version of the original `biskit.test.py` without any dependencies so
that it can be more easily transferred into new packages.

Run the example::
===============

    git clone https://github.com/graik/autotesting.git
    cd autotesting
    python examplepackage/testing.py -i

`testing.py` assumes that it is is located in the root of your python package
and it needs to be able to import this parent package. That means, your package
*must* be in the PYTHONPATH. However, you can run the example tests without
installing `examplepackage` into your python environment: simply call the script
from the parent folder, as shown above. (This works because Python automatically
adds the current working directory into the $PYTHONPATH.)

Setup for your python project
=============================

1. Copy `testing.py` into the root of your own python package.

2. Adapt the module-level parameter `DEFAULT_PACKAGES` in `testing.py`

   E.g. if the name of your package (folder) is `superpy` and it also contains a
   sub-package (sub-folder) `superpy/tools`:

   ```python
   DEFAULT_PACKAGES = ['superpy', 'superpy.tools']
   ```

3. Define Unittest classes derived from `testing.AutoTest` in the python modules
   of your package (see `example.py` for, well, an example).

4. Add the following lines to the end of any python module that contains test
   cases:

   ```python
   if __name__ == '__main__':
       testing.localTest()
   ```

Running Tests
=============

The module also acts as the script to collect and run the tests. In the simplest
case, the following will execute all the tests found in any module of your
registered package and sub-packages:

    ./testing.py -i

The following command will execute all the tests from a single sub-package,
except the ones that are tagged 'LONG'::

    ./testing.py -p superpy.tools -e long

Run `./testing.py` without arguments to see the complete help::

    Run unittest tests for the whole package.

        testing.py [-i |include tag1 tag2..| -e |exclude tag1 tag2..|
                    -p |package1 package2..|
                    -v |verbosity| -log |log-file| -nox -dry]

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
        dry  - do not actually run the but only collect tests               [False]

    Examples:

        * Run all but long or obsolete tests from mypackage and mypackage.parser:
        ./testing.py -e old long -p mypackage mypackage.subpackage

        * Run only PVM-dependent tests of the mypackage.calc sub-package:
        ./testing.py -i pvm -p mypackage.calc

Adapting your code
==================

Simply follow the example in the unimaginatively named file `example.py`. 


Background & Motivation
=======================

autotest tries to recover the convenience of good old times, when testing
code was simply dumped into the `__main__` section of a module where it could be
executed and interactively debuged directly from emacs or ipython. The
introduction of unittests and test fixtures, despite many advantages, lost a lot
of this convenience: Tests where less convenient to execute (typically
requiring seperate test fixtures or third-party testing frameworks); testing
code tended to get separated from the module that it is supposed to test;
and intermediate variables remain hidden within the test instances.

autotest adds a thin layer on top of the unittest framework to address these
issues. When called as a script, `testing.py` will automatically extract and run
all `AutoTest`-derived test instances from all modules of your package and
registered sub-packages. Tests are run without individual output and can be
filtered by tags.

On the other hand, you can also execute the tests of only one particular python
module, by simply executing this module. Again there is no need to register your
tests. Simply place the `testing.localTest()` method into the `__main__` body of
your module. `localTest()` will automatically discover any `AutoTest` instances
in your module and execute them. In this case, your tests can report detailed
information (plots, detailed progress bars, etc). Moreover, any variables
assigned to the test instance (`self.*`) will be pushed to the global python
namespace for interactive inspection after your tests have run or failed.

The main philosophy behind this little module is to keep things simple but
practical and to minimize the code that deals with the management of your
testing infrastructure. Contrary to the opinion of serious experts, we very much
prefer to have our testing routines right next to and in the same file as the
code being tested. That's the scenario autotest is particularly good for but it
could, of course, also be used for tests that are collected in seperate files
and folders (but, unless your test files are bundled in their own sub-package,
testing.py will report many modules with missing test cases).