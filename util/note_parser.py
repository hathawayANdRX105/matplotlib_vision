import jieba
import re
import numpy as np
from util.parser import get_word_list, get_filter_source_symbols, get_data_without_single_word


# 获取小说每一章的list
def get_chapter_list(note_path):
    note_source = get_word_list(note_path)
    filter_note_source = get_filter_source_symbols(note_source)

    regexp_string = r'第.*?部第.*?章节'
    maker_setup_note_source = re.sub(regexp_string, 'mark', filter_note_source)

    maker_string = r'mark'
    chapter_list = re.split(maker_string, maker_setup_note_source)

    del chapter_list[0]

    return chapter_list


# 根据每一章 以及 名字list 获取统计
def get_character_name_count(data, data_count, note_name_list):
    note_name_list = set(note_name_list)
    note_name_dict = dict()

    i = 0
    for word in data:
        if word in note_name_list:
            note_name_dict[word] = data_count[i]

        i += 1

    return note_name_dict


# 获取 保护词频以及统计的 章节list  和  每章名字的 list
def get_chapter_word_list_and_name_list(chapter_source, name_list):
    """
    :param chapter_source: [ chapter1, chapter2, chapter3 .. ]
    :param name_list: [ 'name1', 'name2', 'name3', ... ]
    :return chapter_ => [ [ word1, word1_count], [ word2, word2_count], ..]
    :return name_ => [ { 'name1':count, 'name2':count2, .. } , { ... } ]
    """

    chapter_ = []
    name_ = []
    for single_chapter in chapter_source:
        split_word_list = list(jieba.cut(single_chapter, cut_all=False))
        result, count = np.unique(split_word_list, return_counts=True)

        data, data_count = get_data_without_single_word(result, count)

        chapter_.append([data, data_count])
        name_dict = get_character_name_count(data, data_count, name_list)
        name_.append(name_dict)

    return chapter_, name_
