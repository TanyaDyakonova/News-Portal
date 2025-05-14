from django import template

register = template.Library()

BAD_WORDS = ['коронавируса', 'отношения']

@register.filter(name='censor')
def censor(value):
    for bad_word in BAD_WORDS:
        value = value.replace(bad_word, bad_word[0] + '*' * (len(bad_word) - 1))
    return value