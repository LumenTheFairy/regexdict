from regexdict import RegexDict

rough_type = RegexDict([
	("[a-z]+", "word"),
	("\d+", "number"),
	("", "empty")
])

print( rough_type["test"] ) # prints "word"
print( rough_type["blah"] ) # also prints "word"
print( rough_type["1234"] ) # prints "number"
print( rough_type[""] )     # prints "empty"
#print( rough_type["six6"] ) # raises KeyError


group_type = RegexDict([
	("([a-z]+) ([a-z]+)", "two words"),
	("(\d+):(\d+):(\d+)", "three numbers")
])

value, match = group_type.get_with_match("test blah")
print( value )  		# prints "two words"
print( match.groups() ) # prints "('test', 'blah')"

value, match = group_type.get_with_match("12:255:9")
print( value )  		# prints "three numbers"
print( match.groups() ) # prints "('12', '255', '9')"


def return5(): return 5
def bang(s): return s + "!"
def adds(x, y): return int(x) + int(y)

commands = RegexDict([
	("five", return5),
	("(.*) with a bang", bang),
	("(\d+) \+ (\d+)", adds)
])

print( commands.apply("five") ) 			# prints "5"
print( commands.apply("boom with a bang") ) # prints "boom!"
print( commands.apply("21 + 7") )		    # prints "28"
# or simply...
print( commands("five") ) 			  # prints "5"
print( commands("boom with a bang") ) # prints "boom!"
print( commands("21 + 7") )		      # prints "28"