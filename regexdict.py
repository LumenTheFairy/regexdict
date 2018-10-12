import re

class RegexDict():

	# d should be a list of pairs if precedence of matches should be enforced
	# (precedence is in the order of the given list; earlier in the list means higher precedence)
	# if the precedence is not important, and the user has a dict d, d.items() can be passed
	# flags are passed on the underlying re functions called when using this object
	def __init__(self, d, flags=0):

		# give indices to the (key, value) pairs
		self._patterns = []
		self._values = []
		self._compiled_patterns = []
		# maps what will be a full match's lastindex
		# to the index of the associated key, value pair
		# this is relevant in case the keys themselves have groups
		self._group_indices = {}

		cur_key = 0
		cur_group_index = 1
		for key, value in d:

			# compile the given expression
			compiled = re.compile( key, flags )

			# store the info for this pair
			self._patterns.append(key)
			self._values.append(value)
			self._compiled_patterns.append(compiled)
			self._group_indices[cur_group_index] = cur_key

			# increment counters
			cur_key += 1
			cur_group_index += compiled.groups + 1

		# this creates a single compiled regex to test all keys 'simultaneously'
		full_regex = '|'.join( ( '({})'.format(k) ) for k in self._patterns )
		self._full_regex = re.compile( full_regex, flags )

	# takes a string key, and returns the index of the looked up value
	# if there is more than one match, the one with highest precedence is used
	# if there are no matches, KeyError is raised
	def _get_index(self, key):

		# try to match the key
		match = self._full_regex.fullmatch(key)

		if match:
			# return the appropriate index
			return self._group_indices[match.lastindex]
		else:
			# there was no match, so raise an error
			raise KeyError(key)

	# takes a string key, and returns the value that was looked up
	# if there is more than one match, the one with highest precedence is used
	# if there are no matches, KeyError is raised
	def get(self, key):
		# get the index of the value
		index = self._get_index(key)
		# return the value
		return self._values[index]

	# takes a string key, and returns a pair (value, match)
	# where value is the value that was looked up
	# and match is the Match object that matched the given key
	# if there is more than one match, the one with highest precedence is used
	# if there are no matches, KeyError is raised
	def get_with_match(self, key):
		# get the index of the value
		index = self._get_index(key)
		# match the original key regex
		match = self._compiled_patterns[index].fullmatch(key)
		# return the value and match
		return self._values[index], match

	# for dicts with functions as values, this can be used as a shortcut
	# to call the looked up function with the captured groups as parameters
	def apply(self, key):
		# get the function and match for the key
		f, match = self.get_with_match(key)
		# call the function with the match groups as parameters
		return f( *match.groups() )

	# updates the value for the pattern that matches the given key
	# raises KeyError is the key does not match (unlike a normal dictionary, which would add the value)
	def update(self, key, value):
		# get the index of the value
		index = self._get_index(key)
		# update it
		self._values[index] = value

	# returns the underlying list of (pattern, value) pairs
	def get_underlying_dict(self):
		return list(zip( self._patterns, self._values ))

	# regdictojb[key] can be used as shortcut for get
	__getitem__ = get

	# regdictojb[key] = val can be used as shortcut for update
	__setitem__ = update

	# regdictojb(key) can be used as shortcut for apply
	__call__ = apply