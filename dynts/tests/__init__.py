from timeseries import *
from dsl import *
from dataprovider import *
from testdynts import *
from testflot import *
from testop import *
from testcrossection import *
from test_datastructures import *


import functions

class TestMeanFunction(functions.SimpleFunctionTest):
    function = 'mean'

class TestMaxFunction(functions.SimpleFunctionTest):
    function = 'max'

class TestMinFunction(functions.SimpleFunctionTest):
    function = 'min'
