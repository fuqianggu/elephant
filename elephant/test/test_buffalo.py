# -*- coding: utf-8 -*-
"""
Unit tests for the Buffalo analysis objects.

:copyright: Copyright 2014-2016 by the Elephant team, see `doc/authors.rst`.
:license: Modified BSD, see LICENSE.txt for details.
"""

from __future__ import print_function, unicode_literals

import unittest
import elephant.buffalo as buf


# #####################################################################################################################
# We create local Analysis subclasses for testing the superclass basic behaviors
#######################################################################################################################

class BasicClass(buf.base.Analysis):
    """
    This class only sets the required class attributes such as `name`, `description` and `_process` function,
    to avoid code redundancy in the following classes supporting the tests.
    In actual Buffalo objects, every inherited class should always set these attributes. They should never be inherited.
    See class `BasicClassExample` below.
    """

    _name = "Base class"
    _description = "Base class for testing Buffalo superclasses"

    def _process(self, *args, **kwargs):
        pass   # dummy process


class BasicClassNoProcess(buf.base.Analysis):
    """Should throw NotImplementedError since `name` and `description` are present, but no `_process` function"""

    _name = "Base class without function"
    _description = "Base class without `_process` for testing Buffalo superclasses"


class BasicClassBehavior(BasicClass):
    _required_params = ['low_cutoff', 'high_cutoff']

    _required_types = {'low_cutoff': (int, float),
                       'high_cutoff': (int, float),
                       'method': (str,)               # optional parameter
                       }


class BasicNoParameters(BasicClass):
    pass


class BasicClassWrongRequiredParams(BasicClass):
    _required_params = None


class BasicClassWrongRequiredParamsItems(BasicClass):
    _required_params = [1, 2]


class BasicClassWrongRequiredTypes(BasicClass):
    _required_types = None


class BasicClassWrongRequiredTypesItems(BasicClass):
    # no commas. Values are going to be evaluated as int or str directly, not tuple
    _required_types = {'low_cutoff': (int),
                       'high_cutoff': (int),
                       'method': (str)
                       }


class BasicClassNoRequiredTypes(BasicClass):
    _required_params = ['low_cutoff', 'high_cutoff']


class BasicClassNoRequiredParams(BasicClass):
    _required_types = {'low_cutoff': (int,)}


class BasicClassNoAttributes(buf.base.Analysis):
    _required_params = ['low_cutoff', 'high_cutoff']

    _required_types = {'low_cutoff': (int, float),
                       'high_cutoff': (int, float),
                       'method': (str,)               # optional parameter
                       }

    def _process(self, *args, **kwargs):
        pass  # dummy process


TEST_NAME = "Standard Buffalo analysis"
TEST_DESCRIPTION = "The structure that a working Buffalo object should have"


class BasicClassExample(buf.base.Analysis):
    _name = TEST_NAME
    _description = TEST_DESCRIPTION

    _required_params = ['low_cutoff', 'high_cutoff']

    _required_types = {'low_cutoff': (int, float),
                       'high_cutoff': (int, float),
                       'method': (str,)               # optional parameter
                       }

    def _process(self, *args, **kwargs):
        pass  # dummy process


########################################################################################################################
# Test cases
########################################################################################################################

class AnalysisBaseClassTestCase(unittest.TestCase):

    def test_input_parameter_checks(self):
        print("Input validation check")

        # Params is not a dict, should throw exception
        with self.assertRaises(buf.exceptions.BuffaloWrongParametersDictionary):
            BasicClassBehavior(params=True)

        # Params is empty dict, should throw exception
        with self.assertRaises(buf.exceptions.BuffaloMissingRequiredParameters):
            BasicClassBehavior()

        # Params has only non-required items, should throw exception
        missing_analysis_params = {'cutoff': 10}
        with self.assertRaises(buf.exceptions.BuffaloMissingRequiredParameters):
            BasicClassBehavior(params=missing_analysis_params)

        # Params has only one required item, should throw exception
        only_one_required_analysis_params = {'high_cutoff': 20,
                                             'extra': "raw"}
        with self.assertRaises(buf.exceptions.BuffaloMissingRequiredParameters):
            BasicClassBehavior(params=only_one_required_analysis_params)

        # Params has all required items and a non-validated item, should pass
        extra_non_validated_analysis_params = {'low_cutoff': 10,
                                               'high_cutoff': 20,
                                               'extra_non_validated': "raw"}
        extra_non_validated = BasicClassBehavior(params=extra_non_validated_analysis_params)
        self.assertIsInstance(extra_non_validated, BasicClassBehavior)

        # Creating the next two objects with either of these parameters types should work
        analysis_1_params = {'low_cutoff': 10,
                             'high_cutoff': 20}

        analysis_2_params = {'low_cutoff': 10.5,
                             'high_cutoff': 20.5}

        analysis_1 = BasicClassBehavior(params=analysis_1_params)
        analysis_2 = BasicClassBehavior(params=analysis_2_params)
        self.assertIsInstance(analysis_1, BasicClassBehavior)
        self.assertIsInstance(analysis_2, BasicClassBehavior)

        # One of the required parameters has wrong type, should throw exception
        wrong_required_type_analysis_params = {'low_cutoff': '10',
                                               'high_cutoff': 20}
        with self.assertRaises(buf.exceptions.BuffaloWrongParameterType):
            BasicClassBehavior(params=wrong_required_type_analysis_params)

        # All required parameters, one non-required but validated parameter with the right type. Should pass
        extra_analysis_params = {'low_cutoff': 10,
                                 'high_cutoff': 20.0,
                                 'method': "raw"}
        extra_analysis = BasicClassBehavior(params=extra_analysis_params)
        self.assertIsInstance(extra_analysis, BasicClassBehavior)

        # All required parameters, one non-required but validated parameter has the wrong type. Should throw exception
        error_extra_analysis_params = {'low_cutoff': 10,
                                       'high_cutoff': 20.0,
                                       'method': 1}
        with self.assertRaises(buf.exceptions.BuffaloWrongParameterType):
            BasicClassBehavior(params=error_extra_analysis_params)

    def test_inheritance_errors(self):
        print("Inheritance check")

        analysis_params = {'low_cutoff': 10,
                           'high_cutoff': '20'}
        types_analysis_params = {'low_cutoff': 10}
        types_error_analysis_params = {'low_cutoff': 10.0}

        # Class without validation, but without custom `_process`. Should accept empty input parameters but throw
        # NotImplementedError
        with self.assertRaises(NotImplementedError):
            BasicClassNoProcess()

        # This should work despite not giving input parameters
        self.assertIsInstance(BasicNoParameters(), BasicNoParameters)

        # Wrong implementations of `_required_types` and `_required_args`
        with self.assertRaises(buf.exceptions.BuffaloImplementationError):
            BasicClassWrongRequiredParams(params=analysis_params)
        with self.assertRaises(buf.exceptions.BuffaloImplementationError):
            BasicClassWrongRequiredParamsItems(params=analysis_params)
        with self.assertRaises(buf.exceptions.BuffaloImplementationError):
            BasicClassWrongRequiredParamsItems(params=analysis_params)
        with self.assertRaises(buf.exceptions.BuffaloImplementationError):
            BasicClassWrongRequiredTypes(params=analysis_params)
        with self.assertRaises(buf.exceptions.BuffaloImplementationError):
            BasicClassWrongRequiredTypesItems(params=analysis_params)

        # Despite string, should work because not checking types
        self.assertIsInstance(BasicClassNoRequiredTypes(params=analysis_params), BasicClassNoRequiredTypes)

        # Should fail because checking only required parameters
        with self.assertRaises(buf.exceptions.BuffaloMissingRequiredParameters):
            BasicClassNoRequiredTypes(params=types_analysis_params)

        # Should work because types are correct
        self.assertIsInstance(BasicClassNoRequiredParams(params=types_analysis_params), BasicClassNoRequiredParams)

        # Should fail because doing type checking only
        with self.assertRaises(buf.exceptions.BuffaloWrongParameterType):
            BasicClassNoRequiredParams(params=types_error_analysis_params)

    def test_required_attributes(self):
        analysis_params = {'low_cutoff': 10,
                           'high_cutoff': 20}

        with self.assertRaises(buf.exceptions.BuffaloImplementationError):
            BasicClassNoAttributes(params=analysis_params)
        self.assertIsInstance(BasicClassExample(params=analysis_params), BasicClassExample)

    def test_annotations(self):
        analysis = BasicNoParameters()
        self.assertEqual(len(list(analysis.annotations.keys())), 0)

        analysis.annotate(annotation1=56)
        self.assertEqual(len(list(analysis.annotations.keys())), 1)
        self.assertTrue('annotation1' in analysis.annotations.keys())
        self.assertEqual(analysis.annotations['annotation1'], 56)

        analysis.annotate(annotation2='teste', annotation3=56.7)
        self.assertEqual(len(list(analysis.annotations.keys())), 3)
        self.assertTrue('annotation2' in analysis.annotations.keys())
        self.assertTrue('annotation3' in analysis.annotations.keys())
        self.assertEqual(analysis.annotations['annotation2'], "teste")
        self.assertEqual(analysis.annotations['annotation3'], 56.7)

        analysis.annotate(annotation1=45, annotation4={'a': 5, 'b': 6})
        self.assertEqual(len(list(analysis.annotations.keys())), 4)
        self.assertEqual(analysis.annotations['annotation1'], 45)
        self.assertNotEqual(analysis.annotations['annotation1'], 56)
        self.assertIsInstance(analysis.annotations['annotation4'], dict)
        self.assertEqual(analysis.annotations['annotation4']['a'], 5)
        self.assertEqual(analysis.annotations['annotation4']['b'], 6)

    def test_class_attributes(self):
        analysis_params = {'low_cutoff': 10,
                           'high_cutoff': 20}

        extra_analysis_params = {'low_cutoff': 10,
                                 'high_cutoff': 20,
                                 'method': 'raw'}

        analysis = BasicClassExample(params=analysis_params)
        extra_analysis = BasicClassExample(params=extra_analysis_params)

        for test_object in [analysis, extra_analysis]:
            self.assertIsInstance(test_object, BasicClassExample)
            self.assertEqual(test_object.name, TEST_NAME)
            self.assertEqual(test_object.description, TEST_DESCRIPTION)
            self.assertEqual(test_object.input_parameters['low_cutoff'], 10)
            self.assertEqual(test_object.input_parameters['high_cutoff'], 20)
        self.assertTrue('method' not in analysis.input_parameters)
        self.assertEqual(extra_analysis.input_parameters['method'], "raw")


if __name__ == '__main__':
    unittest.main()