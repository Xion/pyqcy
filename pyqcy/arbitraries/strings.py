"""
Generators of arbitrary strings.
"""
import random
import re
import string

from pyqcy.arbitraries import arbitrary, is_arbitrary
from pyqcy.arbitraries.numbers import int_


@arbitrary(str)
def str_(of=int_(min=0, max=255), min_length=1, max_length=64):
    """Generator for arbitrary strings.

    Parameters for this generator allow for adjusting the length
    of resulting strings and the set of characters they are composed of.

    :param of: Characters used to construct the strings.
               This can be either an iterable of characters
               (e.g. a string) or a generator that produces them.
    :param min_length: A minimum length of string to generate
    :param max_length: A maximum length of string to generate
    """
    length = random.randint(min_length, max_length)
    char = lambda ch: ch if isinstance(ch, basestring) else chr(ch)
    if is_arbitrary(of):
        return ''.join(char(next(of)) for _ in xrange(length))
    return ''.join(char(random.choice(of)) for _ in xrange(length))


@arbitrary(unicode)
def unicode_(of=int_(min=0, max=65535), min_length=1, max_length=64):
    """Generator for arbitrary Unicode strings.

    Parameters for this generator allow for adjusting the length
    of resulting strings and the set of characters they are composed of.

    :param of: Characters used to construct the strings.
               This can be either an iterable of characters
               (e.g. a string) or a generator that produces them.
    :param min_length: A minimum length of string to generate
    :param max_length: A maximum length of string to generate
    """
    length = random.randint(min_length, max_length)
    char = lambda ch: ch if isinstance(ch, basestring) else unichr(ch)
    if is_arbitrary(of):
        return u''.join(char(next(of)) for _ in xrange(length))
    return u''.join(char(random.choice(of)) for _ in xrange(length))


# Common patterns

@arbitrary(str)
def email():
	"""Generator of arbitrary email addresses."""
	return next(regex(r'[\w\d\.\+]+@[\w\d]+(\.[\w\d]+)+'))


# Regular expressions

@arbitrary(str)
class regex(object):
	"""Generator for strings matching a regular expression.

	:param pattern: A regular expression - either a compiled one
				  	or string pattern
	"""
	def __init__(self, pattern):
		if not isinstance(pattern, basestring):
			pattern = pattern.pattern	# assuming regex object
		self.regex_ast = re.sre_parse.parse(pattern).data

	def __iter__(self):
		return self

	def next(self):
		return ''.join(self.__reverse_node(node)
					   for node in self.regex_ast)

	def __reverse_node(self, (type_, data)):
		"""Generates a string that matches given node
		from the regular expression AST.
		"""
		if type_ == 'literal':
			return chr(data)
		if type_ == 'any':
			return next(self.__random_char)

		if type_ == 'in': #
			return self.__reverse_in_node(data)
		if type_ in ['min_repeat', 'max_repeat']:
			return self.__reverse_repeat_node(data)
		if type_ == 'subpattern':
			return self.__reverse_subpattern_node(data)

		if type_ == 'at':
			return ''	# match-beginning (^) or match-end ($);
						# irrelevant for string generation

		# TODO: add support for the rest of regex syntax elements
		raise ValueError("unsupported regular expression element: %s", type_)

	__random_char = str_(min_length=1, max_length=1)

	def __reverse_in_node(self, node_data):
		"""Generates a string that matches 'in' node
		from the regular expression AST. Such node is an alternative
		between several variants.
		"""
		# TODO: add support for negation: [^...]
		chosen = random.choice(node_data)
		type_, data = chosen

		if type_ == 'range':
			min_char, max_char = data
			return chr(random.randint(min_char, max_char))
		if type_ == 'category':
			return self.__reverse_category_node(data)

		return self.__reverse_node(chosen)

	def __reverse_category_node(self, node_data):
		"""Generates a string that matches 'category' node
		from the regular expression AST. Such node specifies
		a particular kind of characters, like letters or whitespace.
		"""
		type_ = node_data

		# TODO: support more categories
		if type_ == 'category_word':
			return random.choice(string.ascii_letters)
		if type_ == 'category_digit':
			return random.choice(string.digits)
		if type_ == 'category_space':
			return ' '

	def __reverse_repeat_node(self, node_data):
		"""Generates a string that matches 'min_repeat' or 'max_repeat' node
		from the regular expression AST. As name implies, such node
		is a repetition of some pattern.
		"""
		min_count, max_count, [what] = node_data
		count = random.randint(min_count, min(max_count, 64))
		return self.__reverse_node(what) * count

	def __reverse_subpattern_node(self, node_data):
		"""Generates a string that matches 'subpattern' node
		from the regular expression AST. Subpattern specifies
		a (capture) group defined within the regex.
		"""
		_, inner = node_data 	# first element is group index; unused for now
		return ''.join(self.__reverse_node(node) for node in inner)
