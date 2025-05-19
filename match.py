# -*- coding: utf-8 -*-
# from cnl_parser import parser
import copy

from ruwordnet import RuWordNet
wn = RuWordNet(filename_or_session="ruwordnet.db")
from pymorphy3 import MorphAnalyzer
morph = MorphAnalyzer()

special_terms = {
'ПЕЧЕНЫЕ_ИЗДЕЛИЯ' : '107282-N',
'ПРОДУКТЫ_ПИТАНИЯ' : '368-N',
'ЦВЕТ__ОКРАСКА' : '106944-A'
}

class cnl_match:
    def is_special_term(self, name):
        """
        Распознавание специального термина.
        """
        if name.startswith('объект') and name.find('_') != -1:
            return True
        else:
            return False


    def special_term_prefix(self, name):
        """
        Префикс спец-термина.
        """
        return name.split('_',1)[0]


    def special_term(self,name):
        """
        Спец-термин.
        """
        return name.removeprefix(self.special_term_prefix(name) + '_')


    def id_spec_term(self, name):
        """
        id спец-термина в словаре special_terms.
        """
        if not self.is_special_term(name):
            raise Exception('id_spec_term : не коректный формат спецтермина ' + name)
        sp_term = self.special_term(name)
        try:
            id = special_terms[sp_term]
        except Exception as e:
            print('special_term : ' + sp_term + ' не найден в словаре special_terms.')
        return special_terms[sp_term]

    def title2id(self, name):
        """
        Возвращает id первого синсета или исключение:
        word2id: В RuWordNet не найдено слово '+name
        """
        synsets = wn.get_synsets(name)
        if len(synsets) == 0:
            raise Exception('getid : В RuWordNet не найдено слово ' + name)
        return synsets[0].id


    def id2title(self, id):
        """
        Вазвращает title синсета по id.
        """
        synset = wn.get_synset_by_id(id)
        if synset == None:
            raise Exception('id2title : В RuWordNet нет синсета с id ' + id)
        return synset.title


    def path2root_synsets(self, id):
        """
        Путь от слова к корню в RuWordNet.
        Возвращает список синсетов.
        """
        path = []
        # Выборка синсета слова.
        synset = wn.get_synset_by_id(id)
        if synset == None:
            raise Exception('path2root : В RuWordNet не найдено слово ' + id)

        # Сканирование пути от слова к корню в RuWordNet.
        while True:
            path.append(synset)
            synsets = synset.hypernyms
            if synsets == []:
                break
            synset = synsets[0]
        return path


    def path2root_titles(self, id):
        """
        Путь от слова к корню в RuWordNet.
        Возвращает список главных слов синсетов.
        """
        #id = title2id(word)
        path = self.path2root_synsets(id)
        titles = []
        for snst in path:
            titles.append([snst.title, snst.id])
        return titles


    def is_op(self, expr):
        """
        expr = ['и' ...] илм ['или' ...] или ['-' ...]
        """
        if type(expr) != type([]):
            return False
        if expr == []:
            return False
        if type(expr[0]) != type(''):
            return False
        if expr[0] == 'и' or expr[0] == 'или' or expr[0] == '-':
            return True
        return False


    def hyperonym_hyponym(self, x, y):
        """
        x, y находятся в отношении гипероним - гипоним.
        """
        # извлечение title из y.
        if self.is_special_term(x):
            hyperonym = self.special_term(x)

        if self.is_special_term(y):
            id = self.id_spec_term(y)
        else:
            norm_y = morph.parse(y)[0].normal_form
            norm_y = norm_y.replace('ё','е')
            id = self.title2id(norm_y)
        path = self.path2root_titles(id)
        if path == []:
            return False
        for title_id in path:
            title = title_id[0]
            title = title.replace(' ','_')
            title = title.replace(',', '_')
            if title == hyperonym:
                return True
        return False




    ##########################################################################################################
    def frm_match_rec(self, tmpl, frm):
        """
        Сопоставление шаблона с фреймом.
        """
        # Проверка корректности структуры аргументов.
        if not (type(tmpl) == type([]) or type(tmpl) == type('')):
            raise Exception('frm_match: некорректный тип аргумента.')
        if not (type(frm) == type([]) or type(frm) == type('')):
            raise Exception('frm_match: некорректный тип аргумента.')
        #
        # # Сопоставление.
        # if tmpl == []:  # пустой список шаблона сопоставим с любым термом.
        #     return True
        # elif frm == []: # шаблон не пустой список не сопоставим с пустым списком терма.
        #     return False

        # Строки.
        if type(tmpl) == type('') and type(frm) == type(''):
            return self.term_match(tmpl, frm)

        # Списки типа XXX_list.
        if self.is_list(tmpl) and self.is_list(frm):
            return self.list_match(tmpl, frm)

        # Типы шаблона и фрейма неравны.
        if type(tmpl) != type(frm):
            return False

        # Слоты не списки типа XXX_list.
        if len(tmpl) > len(frm):
            return False
        for i in range(0,len(tmpl)):
            if self.frm_match_rec(tmpl[i], frm[i]) == False:
                return False
        return True

    def frm_match(self, tmpl, frm):
        """

        """
        p_tmpl = self.preprocessing(tmpl)
        p_frm = self.preprocessing(frm)
        return self.frm_match_rec(p_tmpl, p_frm)

    def is_list(self, t):
        """
        python список типа ['XXX_list', ...]
        """
        if not (type(t) == type([]) and t != []):
            return False
        if type(t[0]) != type(''):
            return False
        if t[0].endswith('_list'):
            return True
        else:
            return False


    # def unpack_expr(self, op):
    #     """
    #     Распаковка скобочного выражения. Выражение распаковывается в список операндов.
    #     """
    #     if not self.is_op(op): raise Exception('unpack_expr : аргумент должны быть скобочным выражением.')
    #     list_op = []
    #     for i in range(1,len(op)):
    #         if type(op[i]) == type(''): list_op += [op[i]]
    #         elif self.is_op(op[i]): list_op += self.unpack_expr(op[i])
    #         elif self.is_list(op[i]): list_op += self.unpack_expr_in_list(op[i])
    #         else: raise Exception('unpack_expr : недопустимый тип аргумента - не \'\', не XXX_list и не скобочное выражение is_op.')
    #     return list_op
    #
    #
    # def unpack_expr_in_list(self,l):
    #     """
    #     Распаковка скобочных выражений. Выражение - элемент списка распаковывается в список операндов
    #     и вставляется на место выражения в исходном списке.
    #     """
    #     if not self.is_list(l): raise Exception('unpack_expr_in_list : аргумент должны быть списком XXX_list.')
    #     list = []
    #     for i in range(1,len(l)):
    #         if type(l[i]) == type(''): list += [l[i]]
    #         elif self.is_op(l[i]): list += self.unpack_expr(l[i])
    #         else: raise Exception('unpack_expr_in_list : недопустимый тип аргумента - не \'\', не XXX_list  и не скобочное выражение is_op.')
    #     return list

    def unpack_op(self, op, ctgr):
        """
        Распаковка скобочного выражения. Выражение распаковывается в список операндов.
        """
        if not self.is_op(op): raise Exception('unpack_op : аргумент должны быть скобочным выражением.')
        if len(op) != 3: raise Exception(' unpack_op : слот op должен иметь 3 элемента.')
        return self.unpack_list(op[1], ctgr) + self.unpack_list(op[2], ctgr)


    def unpack_list(self, l, ctgr):
        """
        Распаковка скобочных выражений. Выражение - элемент списка распаковывается в список операндов
        и вставляется на место выражения в исходном списке.
        """
        if not self.is_list(l): raise Exception('unpack_list : аргумент должны быть списком XXX_list.')
        if l[0] != ctgr: return [l]   # распаковывать только списки заданной категории.
        list = []
        for i in range(1, len(l)):
            if type(l[i]) == type(''):
                list += [l[i]]
            elif self.is_op(l[i]): list += self.unpack_op(l[i], ctgr)
            elif self.is_list(l[i]): list += self.unpack_list(l[i], ctgr)
            else: list += [l[i]] # слот

        return list

    def unpack_frame(self, fr, ctgr):
        """
        Распаковка скобочных выражений. Выражение - элемент списка распаковывается в список операндов
        и вставляется на место выражения в исходном списке.
        """
        if self.is_list(fr) and fr[0] == ctgr: return [ctgr] + self.unpack_list(fr, ctgr)
        vfr = []
        for el in fr:
            if type(el) != type([]): vfr += [el]
            else: vfr += [self.unpack_frame(el,ctgr)] # слот
        return vfr


    def definition_list_union(self, fr):
        """
        Распаковка скобочных выражений. Выражение - элемент списка распаковывается в список операндов
        и вставляется на место выражения в исходном списке.
        """
        if type(fr) != type([]): return fr
        vfr = []
        for el in fr:
            # объединение списков до и после.
            if type(el) != type([]): vfr += [el]
            elif el[0] == 'prop_name':
                if len(el) == 4:
                    if self.is_list(el[1]) and el[1][0] == 'prop_ablt_list':
                        lst = copy.deepcopy(el[3])
                        lst.pop(0)
                        vfr += [['prop_name', el[2], el[1] + lst]]
                        continue
                elif len(el) == 3:
                    if self.is_list(el[1]) and el[1][0] == 'prop_gent_list':
                        vfr += [['prop_name', el[2], el[1]]]

            elif el[0] == 'prop_noun' and len(el) == 4:
                lst = copy.deepcopy(el[3])
                lst.pop(0)
                vfr += [['prop_noun', el[2], el[1] + lst]]

            # Перемещение определений за главное слово.
            elif el[0] == 'prop_gent___Gent_noun_prtf__plur':
                vfr += [['prop_gent___Gent_noun_prtf__plur', el[2], el[1]]]
            elif el[0] == 'material' and len(el) == 4:
                vfr += [['material', el[1], el[3], el[2]]]
            elif el[0] == 'pred' and len(el) == 4:
                vfr += [['pred', el[2], el[1], el[3]]]



            else: vfr += [self.definition_list_union(el)]
        return vfr


    def preprocessing(self, fr):
        """
        """
        v = self.unpack_frame(fr, 'prop_list')
        v = self.unpack_frame(v, 'prop_ablt_list')
        v = self.unpack_frame(v, 'aggregate_list')
        v = self.definition_list_union(v)
        return v


        return
# def unpack_frame(self, fr, ctgr):
    #     """
    #     Распаковка скобочных выражений. Выражение - элемент списка распаковывается в список операндов
    #     и вставляется на место выражения в исходном списке.
    #     """
    #     vfr = []
    #     for el in fr:
    #         if type(el) != type([]): vfr += [el]
    #         elif self.is_list(el) and fr[0] == ctgr: vfr += [ctgr] + self.unpack_list(el, ctgr)
    #         elif self.is_op(el): vfr += self.unpack_op(el, ctgr)
    #
    #         else:
    #             vfr += [self.unpack_frame(el, ctgr)]  # слот
    #     return vfr
    def list_match(self, tmpl, frm):
        """
        Сопоставление термов типа ['XXX_list',...]
        """
        if not (self.is_list(tmpl) and self.is_list(frm)):
            return False

        # Цикл по членам списков.
        for el_tmpl in tmpl:
            if type(el_tmpl) == type(''):
                if el_tmpl.endswith('list'):
                    continue
            rez = False
            for el_frm in frm:
                if type(el_frm) == type(''):
                    if el_frm.endswith('list'):
                        continue
                if self.frm_match(el_tmpl, el_frm) == True:
                    rez = True
                    break
                else:
                    continue
            if rez == False:
                return False
        return True


    def term_match(self, x,y):
        """
        Сопоставление термов. True в случаях:
        1. x, y строки и равны.
        2. x гипероним в формате гиперонима, y строка - гипоним. True.
        Иначе False
        """
        if type(x) == type('') and type(y) == type(''):
            if x == y:
                return True
            elif self.is_special_term(x):
                if self.hyperonym_hyponym(x, y):
                    return True
        return False
