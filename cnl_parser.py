################################### yacc ######################################################
import ply.lex as lex
import ply.yacc as yacc
import cnl_lexer as tokrules
from cnl_lexer import tokens


'''
s → (sl)
sl → sentence | sl sentence

sentence →  aim_condition sub_pred DOT
aim_condition → ε | aim_condition_prep sub_pred COMMA
aim_condition_prep → IF | FOR 
sub_pred → sub pred

sub → name  
name → prop_noun aggregate_material_loc_part_except
prop_noun → prop NOUN prop

op → AND | OR | DASH    # DASH - дефис '-' 
prop → ε | ADJF prop | LPAREN prop op prop RPAREN prop

aggregate_material_loc_part_except → aggregate material loc part except
prop_gent → ε | ADJF_gent prop_gent
prop_ablt → ε | ADJF_ablt prop_ablt | LCURLYBRACE prop_ablt op prop_ablt RCURLYBRACE prop_ablt

aggregate → ε | prop_gent Gent_noun_prtf__plur aggregate| LSBRACKET aggregate op aggregate RSBRACKET aggregate
material → ε | FROM prop_gent Gent_noun_prtf__plur
loc → ε | LOC_PREP prop_name aggregate
part → ε | prep_part prop_name part
prop_name → prop_noun | prop_gent Gent_noun_prtf__plur | prop_gent Loct | prop_ablt Ablt prop_ablt 
prep_part → WITH | WITHOUT
except → ε | EXCEPT aggregate 

pred → ε | quality feature obj_instr
quality → ε | ADVB
feature → act | relation
act →  VERB | INFN | PRTS | PRCL # PRTS краткое причастие - выточена. PRCL частица - есть 
relation → COMP

obj_instr → obj instr
obj → ε | obj_loc obj_name | obj_name 
obj_loc → LOC_PREP | FROM  
obj_name → name | prop_gent Gent_noun_prtf__plur aggregate_material_loc_part
instr → ε | Ablt prop_ablt 
'''

# def p_s(p):
#     's : sl'
#     p[0] = [p[1]]
#
# def p_sl(p):
#     'sl : sentence'
#     p[0] = p[1]
def p_s(p):
    's : sl'
    p[0] = p[1]

def p_sl(p):
    'sl : sentence'
    p[0] = [p[1]]


def p_empty(p):
    'empty :'
    pass


def p_sl_sent(p):
    'sl : sl sentence'
    p[0] = p[1] + [p[2]]


def p_sentence(p):
    'sentence : aim_condition sub_pred DOT'
    p[0] = ['sentence', p[1], p[2]]


def p_aim_condition_empty(p):
    'aim_condition : empty'
    p[0] = ['aim_condition']


def p_aim_condition(p):
    'aim_condition : aim_condition_prep sub_pred COMMA'
    p[0] = ['aim_condition', p[1], p[2]]


def p_aim_condition_prep_if(p):
    'aim_condition_prep : IF'
    p[0] = ['if', p[1]]


def p_aim_condition_prep_for(p):
    'aim_condition_prep : FOR'
    p[0] = ['aim', p[1]]


def p_sub_pred(p):
    'sub_pred : sub pred'
    p[0] = ['sub_pred', p[1], p[2]]


##############################################

def p_sub(p):
    'sub : name'
    p[0] = ['sub', p[1]]


def p_name(p):
    'name : prop_noun aggregate_material_loc_part_except'
    p[0] = ['name', p[1], p[2]]


def p_prop_noun(p):
    'prop_noun : prop NOUN prop'
    if p[1] == []: sp1 = ['prop_list']
    else: sp1 = ['prop_list'] + p[1]
    if p[3] == []: sp3 = ['prop_list']
    else: sp3 = ['prop_list'] + p[3]
    p[0] = ['prop_noun', sp1, p[2], sp3]


def p_op_and(p):
    'op : AND'
    p[0] = p[1]


def p_op_or(p):
    'op : OR'
    p[0] = p[1]


def p_op_dash(p):
    'op : DASH'
    p[0] = p[1]


def p_prop__empty(p):
    'prop : empty'
    p[0] = []


def p_prop_1(p):
    'prop : ADJF prop'
    p[0] = [p[1]] + p[2]
    pass

def p_prop_2(p):
    'prop : LPAREN prop op prop RPAREN prop'
    p[0] = [[p[3], ['prop_list'] + p[2], ['prop_list'] + p[4]]] + p[6]
    # p[0] = [p[3], p[2], p[4]] + p[6]


def p_aggregate_material_loc_part_except(p):
    'aggregate_material_loc_part_except : aggregate material loc part except'
    if p[1] == []: sp1 = ['aggregate_list']
    else: sp1 = ['aggregate_list'] + p[1]
    if p[2] == []: sp2 = ['material']
    else: sp2 = ['material'] + p[2]
    if p[3] == []: sp3 = ['loc']
    else: sp3 = ['loc'] + p[3]
    if p[4] == []: sp4 = ['part_list']
    else: sp4 = ['part_list'] + p[4]
    if p[5] == []: sp5 = ['except']
    else: sp5 = ['except'] + p[5]

    p[0] = ['aggregate_material_loc_part_except', sp1, sp2, sp3, sp4, sp5]



def p_prop_gent_empty(p):
    'prop_gent : empty'
    p[0] = []


def p_prop_gent(p):
    'prop_gent : ADJF_gent prop_gent'
    p[0] = [p[1]] + p[2]


def p_prop_ablt_empty(p):
    'prop_ablt : empty'
    p[0] = []


def p_prop_ablt_1(p):
    'prop_ablt : ADJF_ablt prop_ablt'
    p[0] = [p[1]] + p[2]


def p_prop_ablt_2(p):
    'prop_ablt : LCURLYBRACE prop_ablt op prop_ablt RCURLYBRACE prop_ablt'
    p[0] = [[p[3], ['prop_ablt_list'] + p[2], ['prop_ablt_list'] + p[4]]] + p[6]


def p_aggregate_empty(p):
    'aggregate : empty'
    p[0] = []


def p_aggr_1(p):
    'aggregate : prop_gent Gent_noun_prtf__plur aggregate'
    if p[1] == []: sp1 = ['prop_gent_list']
    else: sp1 = ['prop_gent_list'] + p[1]
    p[0] = [['prop_gent___Gent_noun_prtf__plur',sp1, p[2]]] + p[3]


def p_aggr_2(p):
    'aggregate : LSBRACKET aggregate op aggregate RSBRACKET aggregate'
    #p[0] = ['aggregate_list', [p[3], p[2],p[4]]] + p[6]
    p[0] = [[p[3], ['aggregate_list'] + p[2], ['aggregate_list'] + p[4]]] + p[6]


def p_material_empty(p):
    'material : empty'
    p[0] = []


def p_material(p):
    'material : FROM prop_gent Gent_noun_prtf__plur'
    if p[2] == []: sp2 = ['prop_gent_list']
    else: sp2 = ['prop_gent_list'] + p[2]
    p[0] = [p[1], sp2] + [p[3]]


def p_loc_empty(p):
    'loc : empty'
    p[0] = []


def p_loc(p):
    'loc : LOC_PREP prop_name aggregate'
    if p[3] == []: sp3 = ['aggregate_list']
    else: sp3 = p[3]
    p[0] = [p[1], p[2], sp3]


def p_part_empty(p):
    'part : empty'
    p[0] = []


def p_part(p):
    'part : prep_part prop_name part'
    p[0] = [['part',p[1], p[2]]] + p[3]


def p_prop_name(p):
    'prop_name : prop_noun'
    p[0] = ['prop_name', p[1]]


def p_prop_name_1(p):
    'prop_name : prop_gent Gent_noun_prtf__plur'
    if p[1] == []: sp1 = ['prop_gent_list']
    else: sp1 = ['prop_gent_list'] + p[1]
    p[0] = ['prop_name', sp1, p[2]]

def p_prop_name_2(p):
    'prop_name : prop_gent Loct'
    if p[1] == []: sp1 = ['prop_gent_list']
    else: sp1 = ['prop_gent_list'] + p[1]
    p[0] = ['prop_name', sp1, p[2]]


def p_prop_name_3(p):
    'prop_name : prop_ablt Ablt prop_ablt'
    if p[1] == []: sp1 = ['prop_ablt_list']
    else: sp1 = ['prop_ablt_list'] + p[1]
    if p[3] == []: sp3 = ['prop_ablt_list']
    else: sp3 = ['prop_ablt_list'] + p[3]
    p[0] = ['prop_name', sp1, p[2], sp3]



def p_prep_part_with(p):
    'prep_part : WITH'
    p[0] = p[1]


def p_prep_part_without(p):
    'prep_part : WITHOUT'
    p[0] = p[1]


def p_except(p):
    'except : empty'
    p[0] = []


def p_except_1(p):
    'except : EXCEPT aggregate'
    if p[2] == []: sp2 = ['aggregate_list']
    else: sp2 =  ['aggregate_list'] + p[2]
    p[0] = [p[1], sp2]


#########################
def p_pred_empty(p):
    'pred : empty'
    p[0] = ['pred']


def p_pred(p):
    'pred : quality feature obj_instr'
    p[0] = ['pred', p[1], p[2], p[3]]


def p_quality__empty(p):
    'quality : empty'
    p[0] = ['quality']


def p_quality(p):
    'quality : ADVB'
    p[0] = ['quality', p[1]]


def p_feature_act(p):
    'feature : act'
    p[0] = ['act', p[1]]


def p_feature_relation(p):
    'feature : relation'
    p[0] = ['relation', p[1]]


def p_act_verb(p):
    'act : VERB'
    p[0] = ['act_VERB', p[1]]


def p_act_infn(p):
    'act : INFN'
    p[0] = ['act_INFN', p[1]]


def p_act_prts(p):
    'act : PRTS'
    p[0] = ['act_PRTS', p[1]]


def p_act_prcl(p):
    'act : PRCL'
    p[0] = ['act_PRCL', p[1]]


def p_relation_comp(p):
    'relation : COMP'
    p[0] = ['rel_COMP', p[1]]


####################################################
def p_obj_instr(p):
    'obj_instr : obj instr'
    p[0] = ['obj_instr', p[1], p[2]]


def p_obj_empty(p):
    'obj : empty'
    p[0] = ['obj']


def p_obj(p):
    'obj : obj_loc obj_name'
    p[0] = ['obj', p[1], p[2]]

def p_obj_1(p):
    'obj : obj_name'
    p[0] = ['obj', p[1]]


def p_obj_loc(p):
    'obj_loc : LOC_PREP'
    p[0] = ['obj_loc', p[1]]

def p_obj_loc_1(p):
    'obj_loc : FROM'
    p[0] = ['obj_loc', p[1]]


def p_obj_name(p):
    'obj_name : name'
    p[0] = ['obj_name', p[1]]


def p_obj_name_1(p):
    'obj_name : prop_gent Gent_noun_prtf__plur aggregate_material_loc_part_except'
    if p[1] == []: sp1 = ['prop_gent_list']
    else: sp1 = ['prop_gent_list'] + p[1]
    p[0] = ['obj_name', sp1, p[2], p[3]]


def p_instr_empty(p):
    'instr : empty'
    p[0] = ['instr']


def p_instr(p):
    'instr : Ablt prop_ablt'
    p[0] = ['instr ', p[1], ['prop_ablt_list'] + p[2]]

#############################################################
# def str1(s):
#     """
#     Вставка двоеточия перед терминами.
#     """
#     if s[0] != '(' and s[0] != ':':
#         s = ':' + str(s)
#
#     return str(s)


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")
    print(p)


# Build lexer and parser
lexer = lex.lex(module=tokrules)
parser = yacc.yacc(debug=True)


