"""
Generators of arbitrary strings.
"""
import random
import re
import string

from pyqcy.arbitraries import arbitrary, is_arbitrary
from pyqcy.arbitraries.standard import int_


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


# Regular expressions

@arbitrary(str)
def regex(pattern):
	"""Generator for strings matching a regular expression.

	:param pattern: A regular expression - either a compiled one
				  	or string pattern
	"""
	if not isinstance(pattern, basestring):
		pattern = pattern.pattern	# assuming regex object

	random_char = str_(min_length=1, max_length=1)
	def generate_node_match((type_, data)):
		if type_ == 'at':
			return ''	# match-beginning (^) or match-end ($);
						# irrelevant for string generation

		if type_ == 'any':
			return next(random_char)
		if type_ == 'literal':
			return chr(data)

		if type_ == 'in': # TODO: add support for negation: [^...]
			in_type, in_data = random.choice(data)
			if in_type == 'range':
				return chr(random.randint(*in_data))
			if in_type == 'category': 	# TODO: support more categories
				if in_data == 'category_word':
					return random.choice(string.ascii_letters)
				if in_data == 'category_digit':
					return random.choice(string.digits)
				if in_data == 'category_space':
					return ' '
			return generate_node_match(what)

		if type_ in ['min_repeat', 'max_repeat']:
			min_count, max_count, [what] = data
			count = random.randint(min_count, max_count)
			return generate_node_match(what) * count

		if type_ == 'subpattern':
			_, inner = data 	# first item is subpattern index
			return generate_node_match(inner)

		# TODO: add support for the rest of regex syntax elements
		raise ValueError("unsupported regular expression element: %s", type_)

	regex_data = re.sre_parse.parse(pattern).data
	return ''.join(map(generate_node_match, regex_data))
