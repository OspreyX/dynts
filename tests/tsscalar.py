import numpy as np

from dynts import tsname
from dynts.utils import test
from dynts.utils.py2py3 import zip
from dynts.utils.populate import randomts


class TestScalar(test.TestCase):
    
    def getts(self, cols, **kwargs):
        return randomts(20, cols, backend = self.backend, **kwargs)
    
    def _testscalar(self, oper, rs, ts):
        for rv,cv in zip(rs.values(),ts.values()):
            for r,v in zip(rv,cv):
                self.assertAlmostEqual(r,oper(v))

    def testSqrt(self):
        ts = self.getts(2, name = tsname('a','b'))
        rs = ts.sqrt()
        self.assertEqual(rs.names(),['sqrt(a)','sqrt(b)'])
        self._testscalar(np.sqrt, rs, ts)
        
    def testLog(self):
        ts = self.getts(2, name = tsname('a','b'))
        rs = ts.log()
        self.assertEqual(rs.names(),['log(a)','log(b)'])
        self._testscalar(np.log, rs, ts)
        
    def testSquare(self):
        ts = self.getts(2, name = tsname('a','b'))
        rs = ts.square()
        self.assertEqual(rs.names(),['square(a)','square(b)'])
        self._testscalar(np.square, rs, ts)


@test.skipUnless(test.haszoo(), 'Requires R zoo package')
class TestScalarZoo(TestScalar):
    backend = 'zoo'