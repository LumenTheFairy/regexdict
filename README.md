# Regex Dictionaries

`regexdict` provides an implementation of dictionaries with regular expression patterns as keys, with efficient lookup, for python. For example:

```
from regexdict import RegexDict

rough_type = RegexDict([
    ("[a-z]+", "word"),
    ("\d+", "number"),
    ("", "empty")
])

print( rough_type["test"] ) # prints "word"
print( rough_type["blah"] ) # also prints "word"
print( rough_type["1234"] ) # prints "number"
print( rough_type[""]     ) # prints "empty"
print( rough_type["six6"] ) # raises KeyError
```

## Functionality

`regexdict` is a very simple library, with only a few functions. They are:

### Constructor

A `RegexDict` is constructed with a list of `(pattern, value)` pairs as seen above. A list is used instead of a dict in order to allow the user to define a precedence on the matches. If precedence is unimportant (for example if no matches overlap), a dictionary `d` can be passed into the constructor as `d.items()`. An additional `flags` parameter can also be supplied, which is passed on to the underlying `re` functions, [as described here](https://docs.python.org/3/library/re.html#contents-of-module-re).

### `RegexDict.get(key)`

Takes a string key, and returns the value associated with the first pattern that matches the given key. Note that all matches are full matches, meaning the pattern must match the entire given key, not just the start or some part in the middle. If no patterns match, `KeyError` is raised. `__getitem__` is an alias for `get`, so `[]` can also be used to lookup a value.

### `RegexDict.get_with_match(key)`

Similar to `get`, but returns a pair `(value, match)`, where match is a [match object](https://docs.python.org/3/library/re.html#match-objects) matching the key with the pattern that took. This is relevant if the patterns have group captures:

```
from regexdict import RegexDict

group_type = RegexDict([
    ("([a-z]+) ([a-z]+)", "two words"),
    ("(\d+):(\d+):(\d+)", "three numbers")
])

value, match = group_type.get_with_match("test blah")
print( value )          # prints "two words"
print( match.groups() ) # prints "('test', 'blah')"

value, match = group_type.get_with_match("12:255:9")
print( value )          # prints "three numbers"
print( match.groups() ) # prints "('12', '255', '9')"
```

### `RegexDict.apply(key)`

Used for the special case where the dictionary values are all functions (or at least all callable) -- `RegexDict.apply` looks up the function associated with the given key, and then calls that function, passing the matched groups in as parameters. `__call__` is an alias for `apply`, so `()` can also be used directly on the `RegexDict` object. For example:

```
from regexdict import RegexDict

def return5(): return 5
def bang(s): return s + "!"
def adds(x, y): return int(x) + int(y)

commands = RegexDict([
    ("five", return5),
    ("(.*) with a bang", bang),
    ("(\d+) \+ (\d+)", adds)
])

print( commands.apply("five") )             # prints "5"
print( commands.apply("boom with a bang") ) # prints "boom!"
print( commands.apply("21 + 7") )           # prints "28"
# or simply...
print( commands("five") )             # prints "5"
print( commands("boom with a bang") ) # prints "boom!"
print( commands("21 + 7") )           # prints "28"
```

### `RegexDict.update(key, value)`

Takes a string key and a value, and replaces the value associated with the first pattern that matches the key with the given value. Note that even for update, if no patterns match, `KeyError` is raised (unlike a normal dictionary, which would typically add the key). `__setitem__` is an alias for `get`, so `[] =` can also be used to update a value. So for example:

```
from regexdict import RegexDict

counter = RegexDict([
    ("[a-z]+", 0),
    ("\d+", 0),
    ("", 0)
])

for s in ["test", "", "1234", "a", "33", "blah"]:
    counter[s] += 1

print( counter["a"] ) # prints "3"
print( counter["0"] ) # prints "2"
print( counter[""]  ) # prints "1"
```

### `RegexDict.get_underlying_dict()`

Returns the underlying list of `(pattern, value)` pairs.

## Ommited Functionality

`regexdict` does not include an add or remove function. In order to add or remove a new pattern, the full pattern list needs to be recompiled, so a new RegeDict may as well be built.

## Efficiency

A naive implementation of the get for a regex keyed dictionary would simply test all patterns in sequence. Something like this:

```
def get(regDict, key):
    for regex, value in regDict:
        if re.fullmatch(regex, key):
            return value
    raise KeyError
```

The problem with this approach is that it redoes work and wastes time on irrelevant patterns. For example, take two patterns `"slow" * 1000 + "\d"` and `"slow" * 1000 + "[a-z]"` (appearing in that order). If our key happens to be `"slow" * 1000 + "a"`, the naive implementation will try to match with the first pattern, and (assuming `re` scans the string forward) will fail after scanning through almost all of the string. Matching on the second pattern will have to do the exact same scan again. The patterns should be able to be scanned 'simultaneously' (and indeed, something like a DFA would be able to accomplish this).

`regexdict` solves this problem by reducing the entire lookup to a single regular expression, which is compiled on construction, and used to match any key. The grouping information from this match allows it to recover the original pattern that was matched.

## Version Information

`regexdict` was written with, and has only been tested for, `python 3.7`. It's very likely to work for earlier versions, but no promises.