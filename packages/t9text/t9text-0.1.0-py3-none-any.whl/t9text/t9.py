import itertools
import re

def get_touchtone(phone_str: str):
    '''Given a string of alphabetic characters `phone_str`,
    return a string of corresponding numeric touchtone buttons.
    This method will accept *, -, and # characters as a convenience.'''
    try:
        char_list = list([x.lower() for x in phone_str])
    except err as e:
        print(e)
        raise T9InputException

    acceptable = re.compile(r'([a-z]|[A-Z]|[0-9]|[\*#-])+')
    for c in char_list:
        if not acceptable.match(c):
            raise T9InputException

    tone_dict = {
        'a': '2',
        'b': '2',
        'c': '2',
        'd': '3',
        'e': '3',
        'f': '3',
        'g': '4',
        'h': '4',
        'i': '4',
        'j': '5',
        'k': '5',
        'l': '5',
        'm': '6',
        'n': '6',
        'o': '6',
        'p': '7',
        'q': '7',
        'r': '7',
        's': '7',
        't': '8',
        'u': '8',
        'v': '8',
        'w': '9',
        'x': '9',
        'y': '9',
        'z': '9',
        '-': '-',
        '#': '#',
        '*': '*',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '0': '0',
    }

    return ''.join([tone_dict[c] for c in char_list])


def get_words(touchtone_nums: str):
    '''Given a string `touchtone_nums` which is a string of integers 0-9
       (and optionally dashes, parentheses, stars, and pounds "()*#-"),
       return a list where each entry is a lowercase, alphabetic string
       of chars that match the touchtone buttons.

       This solution was borrowed heavily / plagiarized from this
       StackOverflow answer:
       https://stackoverflow.com/a/12078199'''

    tone2char = {
        0: '0',  # 0 does not have any associated characters
        1: '1',  # 1 does not have any associated characters
        2: 'abc',
        3: 'def',
        4: 'ghi',
        5: 'jkl',
        6: 'mno',
        7: 'pqrs',
        8: 'tuv',
        9: 'wxyz',
        '#': '#',
        '*': '*',
        '-': '-',
    }

    try:
        assert isinstance(touchtone_nums, str)
    except AssertionError:
        try:
            touchtone_nums = str(touchtone_nums)
        except:
            raise T9InputException

    tones = [int(x) if x not in set(list('*#-')) else x for x in list(touchtone_nums)]
    t = [tone2char[i] for i in tones]
    return tuple(''.join(x) for x in itertools.product(*(t)))


class T9InputException(Exception):
    '''This type of exception is raised when illegal input is
    given to `get_touchtone()` or `get_words()`'''
    pass
