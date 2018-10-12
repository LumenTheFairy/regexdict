import unittest
import re
from regexdict import RegexDict

class TestRegexDict(unittest.TestCase):

	basic_dict = RegexDict([
		('a', 1),
		('b', 2),
		('c', 3)
	])

	def test_basic_get(self):
		self.assertEqual( self.basic_dict.get('a'), 1 )
		self.assertEqual( self.basic_dict.get('b'), 2 )
		self.assertEqual( self.basic_dict.get('c'), 3 )

	def test_basic_getitem(self):
		self.assertEqual( self.basic_dict['a'], 1 )
		self.assertEqual( self.basic_dict['b'], 2 )
		self.assertEqual( self.basic_dict['c'], 3 )

	def test_basic_get_with_match(self):
		value, match = self.basic_dict.get_with_match('b')
		self.assertEqual(value, 2)
		self.assertEqual(match.group(), "b")

	def test_underlying(self):
		underlying = self.basic_dict.get_underlying_dict()
		self.assertEqual(underlying, [
			('a', 1),
			('b', 2),
			('c', 3)
		])

	def test_basic_key_error(self):
		with self.assertRaises(KeyError):
			self.basic_dict.get('d')

	group_dict = RegexDict([
		('(a)(b)', 1),
		('(c)(d)(e)', 2),
		('(f)(g)', 3)
	])

	def test_group_get(self):
		self.assertEqual( self.group_dict.get('ab'), 1 )
		self.assertEqual( self.group_dict.get('cde'), 2 )
		self.assertEqual( self.group_dict.get('fg'), 3 )

	def test_group_getitem(self):
		self.assertEqual( self.group_dict['ab'], 1 )
		self.assertEqual( self.group_dict['cde'], 2 )
		self.assertEqual( self.group_dict['fg'], 3 )

	def test_group_get_with_match(self):
		value, match = self.group_dict.get_with_match('cde')
		self.assertEqual( value, 2 )
		self.assertEqual( match.group(), "cde" )
		self.assertEqual( match.group(1), "c" )
		self.assertEqual( match.group(2), "d" )
		self.assertEqual( match.group(3), "e" )

	reg_dict = RegexDict([
		('a*', 1),
		('b|c', 2),
		('\d+', 3)
	])

	def test_reg_get(self):
		self.assertEqual( self.reg_dict.get('a'), 1 )
		self.assertEqual( self.reg_dict.get('aa'), 1 )
		self.assertEqual( self.reg_dict.get('aaaaa'), 1 )
		self.assertEqual( self.reg_dict.get(''), 1 )

		self.assertEqual( self.reg_dict.get('b'), 2 )
		self.assertEqual( self.reg_dict.get('c'), 2 )

		self.assertEqual( self.reg_dict.get('1'), 3 )
		self.assertEqual( self.reg_dict.get('5'), 3 )
		self.assertEqual( self.reg_dict.get('50005'), 3 )
		self.assertEqual( self.reg_dict.get('0123'), 3 )

	def test_reg_get_with_match(self):
		value, match = self.reg_dict.get_with_match('aaa')
		self.assertEqual( value, 1 )
		self.assertEqual( match.group(), "aaa" )

		value, match = self.reg_dict.get_with_match('c')
		self.assertEqual( value, 2 )
		self.assertEqual( match.group(), "c" )

		value, match = self.reg_dict.get_with_match('1024')
		self.assertEqual( value, 3 )
		self.assertEqual( match.group(), "1024" )

	def test_reg_key_error(self):
		with self.assertRaises(KeyError):
			self.basic_dict.get('a2')


	precedence_dict = RegexDict([
		('a', 1),
		('a|b', 2),
		('.*', 3),
	])

	def test_precedence_get(self):
		self.assertEqual( self.precedence_dict.get('a'), 1 )
		self.assertEqual( self.precedence_dict.get('b'), 2 )
		self.assertEqual( self.precedence_dict.get('aaa'), 3 )

	def test_precedence_get_with_match(self):
		value, match = self.precedence_dict.get_with_match('a')
		self.assertEqual( value, 1 )
		self.assertEqual( match.group(), "a" )

		value, match = self.precedence_dict.get_with_match('b')
		self.assertEqual( value, 2 )
		self.assertEqual( match.group(), "b" )

		value, match = self.precedence_dict.get_with_match('aaa')
		self.assertEqual( value, 3 )
		self.assertEqual( match.group(), "aaa" )


	apply_dict = RegexDict([
		( 'five', lambda: 5 ),
		( 'id(\w*)', lambda w: w ),
		( '(\d+)\+(\d+)', lambda x,y: int(x) + int(y) ),
	])

	def test_apply(self):
		self.assertEqual( self.apply_dict.apply('five'), 5 )

		self.assertEqual( self.apply_dict.apply('idea'), 'ea' )
		self.assertEqual( self.apply_dict.apply('idontknow'), 'ontknow' )
		self.assertEqual( self.apply_dict.apply('id'), '' )

		self.assertEqual( self.apply_dict.apply('1+1'), 2 )
		self.assertEqual( self.apply_dict.apply('5+7'), 12 )
		self.assertEqual( self.apply_dict.apply('1+21'), 22 )
		self.assertEqual( self.apply_dict.apply('21+2'), 23 )
		self.assertEqual( self.apply_dict.apply('123+321'), 444 )

	def test_call(self):
		self.assertEqual( self.apply_dict('five'), 5 )

		self.assertEqual( self.apply_dict('idea'), 'ea' )
		self.assertEqual( self.apply_dict('idontknow'), 'ontknow' )
		self.assertEqual( self.apply_dict('id'), '' )

		self.assertEqual( self.apply_dict('1+1'), 2 )
		self.assertEqual( self.apply_dict('5+7'), 12 )
		self.assertEqual( self.apply_dict('1+21'), 22 )
		self.assertEqual( self.apply_dict('21+2'), 23 )
		self.assertEqual( self.apply_dict('123+321'), 444 )

	flags_dict = RegexDict([
		('x', 1),
		('y', 2),
		('z', 3)
	], re.IGNORECASE)

	def test_flags(self):
		self.assertEqual( self.flags_dict.get('x'), 1 )
		self.assertEqual( self.flags_dict.get('X'), 1 )
		self.assertEqual( self.flags_dict.get('y'), 2 )
		self.assertEqual( self.flags_dict.get('Y'), 2 )
		self.assertEqual( self.flags_dict.get('z'), 3 )
		self.assertEqual( self.flags_dict.get('Z'), 3 )

	from_dict = RegexDict({
		'r': 1,
		's': 2,
		't': 3,
	}.items())

	def test_from_dict(self):
		self.assertEqual( self.from_dict.get('r'), 1 )
		self.assertEqual( self.from_dict.get('s'), 2 )
		self.assertEqual( self.from_dict.get('t'), 3 )


	def test_update(self):
		update_dict = RegexDict([
			('u', 0),
			('v', 0)
		])
		self.assertEqual( update_dict.get('u'), 0 )
		update_dict.update('u', 5)
		self.assertEqual( update_dict.get('u'), 5 )

		self.assertEqual( update_dict.get('v'), 0 )
		update_dict.update('v', "something else")
		self.assertEqual( update_dict.get('v'), "something else" )

	def test_setitem(self):
		update_dict = RegexDict([
			('u', 0),
			('v', 0)
		])
		self.assertEqual( update_dict.get('u'), 0 )
		update_dict['u'] = 5
		self.assertEqual( update_dict.get('u'), 5 )

		self.assertEqual( update_dict.get('v'), 0 )
		update_dict['v'] = "something else"
		self.assertEqual( update_dict.get('v'), "something else" )


	def test_update_underlying(self):
		update_dict = RegexDict([
			('u', 0),
			('v', 0)
		])
		underlying = update_dict.get_underlying_dict()
		self.assertEqual(underlying, [
			('u', 0),
			('v', 0)
		])
		update_dict.update('u', 5)
		update_dict.update('v', "something else")
		underlying = update_dict.get_underlying_dict()
		self.assertEqual(underlying, [
			('u', 5),
			('v', "something else")
		])

if __name__ == '__main__':
    unittest.main()