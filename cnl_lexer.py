# module: tokrules.py
# This module just contains the lexing rules
from match import cnl_match
mtch = cnl_match()
from pymorphy3 import MorphAnalyzer
morph = MorphAnalyzer()

# List of token names.   This is always required
tokens = (
    'DOT',  # точка
    'COMMA', # запятая
    'NOUN', # имя существительное	хомяк
    'VERB',	# глагол (личная форма)	говорю, говорит, говорил
    'ADVB',	# наречие	круто
    #'PREP',	# предлог	в
    'ADJF', # имя прилагательное (полное)	хороший
    'INFN', # инфинитив
    'PRTS', # причастие (краткое)	прочитана
    #'PRTF', # причастие (полное)	прочитавший, прочитанная
    'COMP', # компаратив	лучше, получше, выше
    'PRCL', # частица	это, бы, же, лишь

    'Gent_noun_prtf__plur',
        # родительный сущ. Кого? Чего? или полного причастия 'направляющих'.
        # Краткое причастие - прочитана, полное - прочитанная.
    'Ablt', # творительный	Кем? Чем?	зерно съедено хомяком
    'Loct', # предложный О ком? О чём? и т.п.	хомяка несут в корзинке
    'ADJF_gent', # родительный прилагательного для применения в качестве prop у aggregate: большого дома
    'ADJF_ablt', # творительный прилагательного для применения в качестве prop у instr: сверлом победитовым,

    'WITH', # предлог 'c', 'со'
    'WITHOUT', # предлог 'без'
    'FROM',  # предлог 'из'
    'IF',   # предлог 'если'
    'FOR',   # предлог 'для', 'чтобы'
    'LOC_PREP',   # предлоги 'на', 'в', 'над', 'под', 'за', 'к', 'от'
    'AND',   # и
    'OR',   # или
    'DASH', # дефис '-'
    'EXCEPT',   # кроме

    'LPAREN',
    'RPAREN',
    'LSBRACKET',
    'RSBRACKET',
    #'LANGLEBRACKET',
    #'RANGLEBRACKET',
    'LCURLYBRACE',
    'RCURLYBRACE'
)
"""
precedence = (
    ('DOT','COMMA'),
    ('NOUN', 'Gent_noun_prtf__plur', 'Ablt'),
    ('ADVB','VERB','INFN','PRTS','COMP'),
    ('LOC_PREP','WITH','WITHOUT'),
    ('ADJF'),
    ('left', 'AND')
    #,
    #('right', 'LPAREN', 'RPAREN')
)
"""

# Идентификатор
def t_name(t):
    r'[a-zA-Z_а-яА-ЯёЁ][a-zA-Z_а-яА-ЯёЁ0-9]*'

    if t.value == 'с' or t.value == 'со':
        t.type = 'WITH'
        return t
    elif t.value == 'без':
        t.type = 'WITHOUT'
        return t
    elif t.value == 'из':
        t.type = 'FROM'
        return t
    elif t.value == 'если' or t.value == 'Если' :
        t.type = 'IF'
        return t
    elif t.value == 'для' or t.value == 'чтобы' or t.value == 'Для' or t.value == 'Чтобы':
        t.type = 'FOR'
        return t
    elif t.value == 'на' or t.value == 'в' or t.value == 'у' or t.value == 'над' or t.value == 'под' or t.value == 'за'\
            or t.value == 'к' or t.value == 'от':
        t.type = 'LOC_PREP'
        return t
    elif t.value == 'и':
        t.type = 'AND'
        return t
    elif t.value == 'или':
        t.type = 'OR'
        return t
    elif t.value == 'кроме':
        t.type = 'EXCEPT'
        return t

    buff = t.value
    if mtch.is_special_term(t.value):
        is_sp_term = True
        t.value = mtch.special_term_prefix(t.value)
    else:
        is_sp_term = False

    p = morph.parse(t.value)
    if (p[0].tag.POS == 'NOUN' or p[0].tag.POS == 'PRTF') and p[0].tag.case == 'gent':
        # родительный сущ. Кого? Чего? или полного причастия 'направляющих'.
        # Краткое причастие - прочитана, полное - прочитанная.
        t.type = 'Gent_noun_prtf__plur'
        if is_sp_term == True:
            t.value = buff
        return t
    elif p[0].tag.POS == 'NOUN' and p[0].tag.case == 'loct': # предложный О(В) ком? О(В) чём? и т.п.	хомяка несут в корзинке
        t.type = 'Loct'
        if is_sp_term == True:
            t.value = buff
        return t
    elif p[0].tag.POS == 'NOUN' and p[0].tag.case == 'ablt': #творительный	Кем? Чем?	зерно съедено хомяком
        t.type = 'Ablt'
        if is_sp_term == True:
            t.value = buff
        return t
    elif p[0].tag.POS == 'ADJF' and p[0].tag.case == 'gent':  #родительный Кого? Чего?
        t.type = 'ADJF_gent'
        return t
    elif p[0].tag.POS == 'ADJF' and p[0].tag.case == 'ablt':  #родительный Кого? Чего?
        t.type = 'ADJF_ablt'
        return t

    else:
        if is_sp_term == True:
            t.value = buff
        t.type = p[0].tag.POS

    return t


def t_dot(t):
    r'\.'
    t.type = 'DOT'
    return t


def t_comma(t):
    r','
    t.type = 'COMMA'
    return t


def t_lparen(t):
    r'\('
    t.type = 'LPAREN'
    return t


def t_rparen(t):
    r'\)'
    t.type = 'RPAREN'
    return t


def t_lsbracket(t):
    r'\['
    t.type = 'LSBRACKET'
    return t


def t_rsbracket(t):
    r'\]'
    t.type = 'RSBRACKET'
    return t


def t_langle(t):
    r'\<'
    t.type = 'LANGLEBRACKET'
    return t


def t_rangle(t):
    r'\>'
    t.type = 'RANGLEBRACKET'
    return t


def t_lcurlybrace(t):
    r'{'
    t.type = 'LCURLYBRACE'
    return t


def t_rcurlybrace(t):
    r'}'
    t.type = 'RCURLYBRACE'
    return t


def t_dash(t):
    r'\-'
    t.type = 'DASH'
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



