"""
Copyright (c) 2010 Ed Blake <kitsu.eb@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest, sys, re
from py2scad.base import *
from py2scad.transforms import Translate
from py2scad.primitives import Cube, Cylinder

class Test_SCAD_Prog(unittest.TestCase):
    """Test the program object."""

    def setUp(self):
        # Create a minimal program containing a single unit cube
        self.prog = SCAD_Prog()
        self.prog.add(Cube())

    def test_add(self):
        """Verify added objects appear in output."""
        self.prog.add(Cylinder())
        self.assertTrue('cylinder' in str(self.prog).lower(),
                        "Added object does not appear in output!")

    def test_str(self):
        """Verify prog produces a valid program."""
        # This is a tricky thing to check, especially allowing for format cahnges
        # I guess I will check for keywords and matching brackets for now
        output = str(self.prog)
        # Naive bracket check
        self.assertEqual(output.count('('), output.count(')'),
                         "Non-matching parentheses!")
        self.assertEqual(output.count('['), output.count(']'),
                         "Non-matching square brackets!")
        self.assertEqual(output.count('{'), output.count('}'),
                         "Non-matching braces!")
        # Find cube in output
        self.assertTrue('cube' in output.lower(),
                      "Missing entity definition!")
        # Maybe this could use regex to match: command, paren, args, paren, semicolon?


class Test_SCAD_Object(unittest.TestCase):
    """Test the object base class."""
    # This class is somewhat abstract...

    def setUp(self):
        self.obj = SCAD_Object()

    def test_facets(self):
        """Verify facet setting strings."""
        self.assertEqual(self.obj.facets(), '',
                         "Facets should be empty by default!")
        # Notice these are not format tolerant!
        self.obj.fa = 5
        f = self.obj.facets().lower()
        self.assertTrue('$fa=5' in f,
                        "fa setting missing from output: {0}".format(f))
        self.obj.fs = 5
        f = self.obj.facets().lower()
        self.assertTrue('$fs=5' in self.obj.facets().lower(),
                        "fs setting missing from output: {0}".format(f))
        self.obj.fn = 5
        f = self.obj.facets().lower()
        self.assertEqual(', $fn=5', self.obj.facets().lower(),
                        "problem with fn setting in output: {0}".format(f))

    def test_center_str(self):
        """Verify valid center string."""
        # Silly test for a silly function
        center = self.obj.center_str()
        self.assertTrue(center in ('true', 'false'),
                        "Invalid value for centering: {0}".format(center))

    def test_str(self):
        """Verify object output."""
        # Another parser type test...
        self.obj.comment = "This is a test."
        output = str(self.obj)
        # Not much to test in an empty object...
        self.assertTrue(len(output.split('\n'))==2,
                        "Command on same line as comment?")
        self.assertEqual(output[:2], '//',
                         "Comment line is missing?")

    def test_translate(self):
        """Verify valid translate added to object."""
        self.obj.translate = [5, 5, 5]
        output = str(self.obj)
        lines = output.split('\n')
        # Big ugly regular expression that checks for "translate([#,#,#]){" ignoring white space
        d = r"\d+\.\d*" # decimal digit
        self.assertTrue(re.search( # Varify the search expression appears
            r'translate\s*\(\s*\['+d+r',\s*'+d+r',\s*'+d+r'\s*\]\s*\)\s*\{',
            lines[0]),
            "Badly formed translate block?\n{0}".format(lines[0])
        )
        self.assertTrue('}' in lines[-1],
                        "No closing brace?")

class Test_SCAD_CMP_Object(unittest.TestCase):
    """Test the compound object base class."""
    # This class is somewhat abstract too...

    def setUp(self):
        self.obj = SCAD_CMP_Object()


if __name__ == "__main__":
    # Assemble test suites
    prog_suite = unittest.TestLoader().loadTestsFromTestCase(Test_SCAD_Prog)
    obj_suite = unittest.TestLoader().loadTestsFromTestCase(Test_SCAD_Object)
    all_tests = unittest.TestSuite([prog_suite, obj_suite])
    # Run tests
    unittest.TextTestRunner(verbosity=2).run(all_tests)
