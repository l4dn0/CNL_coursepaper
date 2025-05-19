
# -*- coding: utf-8 -*-
from cnl_parser import parser
from match import cnl_match
mtch = cnl_match()
from ruwordnet import RuWordNet
wn = RuWordNet()
from pymorphy3 import MorphAnalyzer
morph = MorphAnalyzer()

############################################# тесты #########################################################
try:
    # frm_match
    print(mtch.frm_match(parser.parse('крыша.')[0], parser.parse('крыша.')[0]))
    print(mtch.frm_match(parser.parse('крыша.')[0], parser.parse('кровля.')[0]))
    pass
    print('красная крыша')
    # print(mtch.frm_match(parser.parse('крыша.')[0], parser.parse('красная крыша.')[0]))
    print(mtch.frm_match(parser.parse('красная крыша.')[0], parser.parse(' железная крыша красная.')[0]))
    print(mtch.frm_match(parser.parse('железная крыша.')[0], parser.parse('красная  крыша .')[0]))

    # print(mtch.frm_match(mtch.preprocessing(parser.parse('железная крыша.')[0]), mtch.preprocessing(parser.parse('красная железная крыша.')[0])))

    print('крыша замка')
    print(mtch.frm_match(parser.parse('крыша замка.')[0], parser.parse('крыша башни замка.')[0]))
    print(mtch.frm_match(parser.parse('крыша башни.')[0], parser.parse('крыша башни замка.')[0]))
    print('слоеный')
    pass
    print(mtch.frm_match(parser.parse('слоеный объект_ПЕЧЕНЫЕ_ИЗДЕЛИЯ с мелким маком.')[0], parser.parse('вкусный слоеный пирог с черным мелким маком.')[0]))
    print(mtch.frm_match(parser.parse('слоеный объект_ПЕЧЕНЫЕ_ИЗДЕЛИЯ с крупным маком.')[0], parser.parse('вкусный слоеный пирог с черным мелким маком.')[0]))
    pass
    print('элемент')
    print(mtch.frm_match(parser.parse('элемент поверхности.')[0], parser.parse('элемент поверхности объекта узла сборки.')[0]))
    print(mtch.frm_match(parser.parse('красный элемент поверхности.')[0], parser.parse('красный железный элемент поверхности объекта узла сборки.')[0]))
    print(mtch.frm_match(parser.parse('деталь с отверстиями круглыми.')[0],parser.parse('деталь с отверстиями круглыми глухими.')[0]))
    print(mtch.frm_match(parser.parse('деталь с отверстиями круглыми без глухих отверстий.')[0],parser.parse('деталь с отверстиями круглыми глухими без глухих некруглых отверстий.')[0]))
    print('кусок')
    # Спецтермины в списке определений.
    # print(parser.parse('кусок корки пирога с луком.'))

    # print(mtch.frm_match(parser.parse('кусок объекта_ПЕЧЕНЫЕ_ИЗДЕЛИЯ.')[0], parser.parse('кусок корки пирога.')[0]))
    print(mtch.frm_match(parser.parse('кусок объекта_ПЕЧЕНЫЕ_ИЗДЕЛИЯ.')[0], parser.parse('кусок корки пирога с луком.')[0]))
    print(mtch.frm_match(parser.parse('кусок объекта_ПРОДУКТЫ_ПИТАНИЯ.')[0], parser.parse('кусок корки объекта_ПЕЧЕНЫЕ_ИЗДЕЛИЯ с луком.')[0]))
    print(mtch.frm_match(parser.parse('кусок объекта_ПЕЧЕНЫЕ_ИЗДЕЛИЯ.')[0],  parser.parse('кусок корки объекта_ПРОДУКТЫ_ПИТАНИЯ с луком.')[0]))
    pass


except Exception as e:
    print(e)


