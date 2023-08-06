import numpy as np
import daproli as dp

import unittest


class TransformerTest(unittest.TestCase):

    def test_Mapper(self):
        data = range(100)
        func = lambda x : x**2

        res1 = dp.map(func, data)
        res2 = dp.Mapper(func).transform(data)

        self.assertEqual(res1, res2)

    def test_Filter(self):
        data = range(100)
        pred = lambda x: x % 2 == 0

        res1 = dp.filter(pred, data)
        res2 = dp.Filter(pred).transform(data)

        self.assertEqual(res1, res2)

    def test_Splitter(self):
        data = range(100)
        func = lambda x: x % 2 == 0

        res1, res2 = dp.split(func, data)
        res3, res4 = dp.Splitter(func).transform(data)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_Expander(self):
        data = range(100)
        func = lambda x : [x, x**2]

        res1, res2 = dp.expand(func, data)
        res3, res4 = dp.Expander(func).transform(data)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_Combiner(self):
        data1 = range(0, 100, 2)
        data2 = range(1, 100, 2)
        func = lambda x1, x2: (x1, x2)

        res1 = dp.combine(func, data1, data2)
        res2 = dp.Combiner(func).transform([data1, data2])

        self.assertEqual(res1, res2)

    def test_Joiner(self):
        data1 = range(0, 100, 2)
        data2 = range(1, 100, 2)
        func = lambda x, y: y-x == 1

        res1 = dp.join(func, data1, data2)
        res2 = dp.Joiner(func).transform([data1, data2])

        self.assertEqual(res1, res2)

    def test_Manipulator(self):
        data = np.random.choice(np.arange(100), 100, replace=False)

        res = dp.Manipulator(sorted).transform(data)
        self.assertEqual([i for i in range(100)], res)

        res = dp.Manipulator(sorted, void=True).transform(data)
        self.assertEqual(data.tolist(), res.tolist())

    def test_Window(self):
        data = range(100)

        res1 = dp.windowed(data, 2, step=2)
        res2 = dp.Window(2, step=2).transform(data)

        self.assertEqual(res1, res2)

    def test_Flat(self):
        data = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]

        res1 = dp.flatten(data)
        res2 = dp.Flat().transform(data)

        self.assertEqual(res1, res2)

    def test_Union(self):
        data1 = range(0, 100, 2)
        data2 = range(1, 100, 2)

        func1 = lambda x : x**2
        func2 = lambda x : x**3

        res1, res2 = dp.map(func1, data1), dp.map(func2, data2)

        res3, res4 = dp.Union(
            dp.Mapper(func1),
            dp.Mapper(func2),
        ).transform([data1, data2])

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_Pipeline(self):
        data = range(10)

        res = dp.Pipeline(
            dp.Filter(lambda x : x > 1),
            dp.Filter(lambda x : all(x % idx != 0 for idx in range(2, x))),
        ).transform(data)

        self.assertEqual([2, 3, 5, 7], res)


