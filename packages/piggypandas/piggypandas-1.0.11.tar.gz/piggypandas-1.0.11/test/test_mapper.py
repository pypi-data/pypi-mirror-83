import unittest
from piggypandas import Mapper
import pandas as pd
import glob
import os


def _clean_tmp_dir():
    for f in glob.glob('../tmp/*'):
        try:
            os.remove(f)
        except OSError:
            pass


class TestMapperBase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        _clean_tmp_dir()

        df: pd.DataFrame = pd.DataFrame(data={
            'Name': ['Boris', 'Basil', 'Vincent', 'Murray'],
            'Species': ['Pig', 'Horse', 'Lamb', 'Mouse'],
            'Color': ['White', 'Black', 'Yellow', 'Gray']
        })
        xlsx_file_cs: str = '../tmp/demomapping-cs.xlsx'
        xlsx_file_ci: str = '../tmp/demomapping-ci.xlsx'
        df.to_excel(xlsx_file_cs, sheet_name='DATA', index=False)
        df.to_excel(xlsx_file_ci, sheet_name='DATA', index=False)
        self._mapper_cs: Mapper = Mapper(xlsx_file_cs, columns=['Name'], ignore_case=False)  # case-sensitive
        self._mapper_ci: Mapper = Mapper(xlsx_file_ci, columns=['Name'], ignore_case=True)  # case-insensitive

    def tearDown(self) -> None:
        self._mapper_cs.flush()
        self._mapper_ci.flush()
        _clean_tmp_dir()
        super().tearDown()


class TestMapperReadOnlyOperations(TestMapperBase):

    def test_has(self):
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertTrue(m.has('Vincent'))
            self.assertFalse(m.has('InvalidKey'))
            self.assertTrue(m.hasc('Vincent', 'Color'))
            self.assertFalse(m.hasc('InvalidKey', 'Color'))
            self.assertFalse(m.hasc('Vincent', 'InvalidCol'))
            self.assertTrue(m.hasc('Vincent'))

    def test_get_no_defaultvalue(self):
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertEqual(m.get('Vincent'), 'Lamb')
            self.assertEqual(m.getc('Murray', 'Color'), 'Gray')
            self.assertEqual(m['Color'].get('Boris'), 'White')
            with self.assertRaises(KeyError):
                m.get('InvalidKey')
            with self.assertRaises(KeyError):
                m.getc('Boris', 'InvalidCol')
            with self.assertRaises(KeyError):
                m.getc('InvalidKey', 'InvalidCol')

    def test_has_caseinsensitive(self):
        for key in ['Vincent', 'VINCENT', 'ViNcEnT']:
            self.assertTrue(self._mapper_ci.has(key))
            for col in ['Color', 'color', 'ColOr']:
                self.assertTrue(self._mapper_ci.hasc(key, col))
                self.assertTrue(self._mapper_ci[col].has(key))

    def test_get_caseinsensitive(self):
        for key in ['Vincent', 'VINCENT', 'ViNcEnT']:
            for col in ['Color', 'color', 'ColOr']:
                self.assertEqual(self._mapper_ci.getc(key, col), 'Yellow')
                self.assertEqual(self._mapper_ci[col].get(key), 'Yellow')

    # noinspection PyStatementEffect
    def test_indexer(self):
        self.assertIsNotNone(self._mapper_cs['Species'])
        self.assertIsNotNone(self._mapper_ci['Species'])
        with self.assertRaises(KeyError):
            self._mapper_cs['InvalidCol']
        with self.assertRaises(KeyError):
            self._mapper_ci['InvalidCol']
        with self.assertRaises(KeyError):
            self._mapper_cs['SPECIES']
        self.assertIsNotNone(self._mapper_ci['SPECIES'])

    def test_touch_no_defaultvalue(self):
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertTrue(m.touch('Vincent'))
            self.assertTrue(m['Species'].touch('Vincent'))
            self.assertFalse(m.touchc('Vincent', 'Sex'))
            self.assertFalse(m.touch('Mary'))
            self.assertFalse(m['Species'].touch('Mary'))
            self.assertFalse(m.touchc('Mary', 'Sex'))


class TestMapperModifyingTouch(TestMapperBase):

    def test_touchc_defaultvalue(self):
        self.assertEqual(self._mapper_cs.size, 4)
        self.assertEqual(self._mapper_ci.size, 4)
        self.assertEqual(len(self._mapper_cs.columns), 3)
        self.assertEqual(len(self._mapper_ci.columns), 3)
        for m in [self._mapper_cs, self._mapper_ci]:
            self.assertTrue(m.touchc('Vincent', 'Species', 'Mutton'))
            self.assertEqual(m.getc('Vincent', 'Species'), 'Lamb')
            self.assertFalse(m.is_changed)
            self.assertTrue(m.touchc('Vincent', 'Sex', 'Male'))
            self.assertEqual(m.getc('Vincent', 'Sex'), 'Male')
            self.assertTrue(m.is_changed)
            self.assertTrue(m.touchc('Mary', 'Species', 'Rat'))
            self.assertEqual(m.getc('Mary', 'Species'), 'Rat')
            self.assertTrue(m.touchc('Mary', 'Sex', 'Female'))
            self.assertEqual(m.getc('Mary', 'Sex'), 'Female')
        self.assertEqual(self._mapper_cs.size, 5)
        self.assertEqual(self._mapper_ci.size, 5)
        self.assertEqual(len(self._mapper_cs.columns), 4)
        self.assertEqual(len(self._mapper_ci.columns), 4)


class TestMapperSet(TestMapperBase):

    def test_set(self):
        self.assertEqual(self._mapper_cs.size, 4)
        self.assertEqual(self._mapper_ci.size, 4)
        self.assertEqual(len(self._mapper_cs.columns), 3)
        self.assertEqual(len(self._mapper_ci.columns), 3)
        for m in [self._mapper_cs, self._mapper_ci]:
            for key, col, value in [
                ('Vincent', 'Species', 'Mutton'),
                ('VinCent', 'Species', 'Mutton'),
                ('Mary', 'Species', 'Hamster'),
                ('MarY', 'SPECIES', 'Hamster')
            ]:
                self.assertTrue(m.setc(key, col, value))
        self.assertEqual(self._mapper_cs.size, 7)
        self.assertEqual(self._mapper_ci.size, 5)
        self.assertEqual(len(self._mapper_cs.columns), 4)
        self.assertEqual(len(self._mapper_ci.columns), 3)


class TestMapperPersistence(unittest.TestCase):

    def test_persistence1(self):
        df: pd.DataFrame = pd.DataFrame(data={
            'Artist': ['Rainbow', 'Yes', 'Sex Pistols'],
            'Genre': ['Hard Rock', 'Art Rock', 'Punk Rock']
        })
        xlsx_file: str = '../tmp/demo-persistence1.xlsx'
        df.to_excel(xlsx_file, sheet_name='DATA', index=False)

        m1: Mapper = Mapper(xlsx_file, columns=['Artist', 'Genre'])
        self.assertTrue(m1['Genre'].set('Godspeed You Black Emperor', 'Post-Rock'))
        self.assertTrue(m1.is_changed)
        m1.flush()
        self.assertFalse(m1.is_changed)
        self.assertTrue(m1.has('Godspeed You Black Emperor'))

        m2: Mapper = Mapper(xlsx_file, columns=['Artist', 'Genre'])
        self.assertFalse(m2.is_changed)
        self.assertTrue(m2.has('Godspeed You Black Emperor'))
        self.assertEqual(m2['Genre'].get('Godspeed You Black Emperor'), 'Post-Rock')

    def test_persistence2(self):
        xlsx_file: str = '../tmp/demo-persistence2'
        columns = ['A', 'B', 'C', 'D', 'E']
        m1: Mapper = Mapper(xlsx_file, columns=columns, ignore_case=True)
        self.assertEqual(m1['B'].get(key='XYZ', defaultvalue='XYZ B'), 'XYZ B')
        self.assertEqual(m1['C'].get(key='XYZ', defaultvalue='XYZ C'), 'XYZ C')
        m1.flush()

        m2: Mapper = Mapper(xlsx_file, columns=columns, ignore_case=True)
        self.assertEqual(m2['B'].get(key='XYZ'), 'XYZ B')
        self.assertEqual(m2['C'].get(key='XYZ'), 'XYZ C')
        m2.flush()

    def setUp(self) -> None:
        super().setUp()
        _clean_tmp_dir()

    def tearDown(self) -> None:
        _clean_tmp_dir()
        super().tearDown()


if __name__ == '__main__':
    unittest.main()
