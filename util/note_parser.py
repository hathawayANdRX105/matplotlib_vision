import re

import jieba
import numpy as np
import pandas as pd

from util.parser import get_data_without_single_word, get_word_list
from util.parser import get_filter_source_symbols
from util.parser import get_sort_data


def get_file_path(file_name):
    import os
    project_path = os.path.dirname(os.getcwd())
    note_path = r"{}\data\seaborn_data\{}".format(project_path, file_name)

    return note_path


# 获取小说每一章的list
def get_chapter_list(note_path):
    note_source = get_word_list(note_path)
    filter_note_source = get_filter_source_symbols(note_source)

    short_name_list = ['道静', '永泽', '嘉川']
    name_list = ['林道静', '余永泽', '卢嘉川', ]
    for short_name, full_name in zip(short_name_list, name_list):
        filter_note_source = re.sub(short_name, full_name, filter_note_source)

    regexp_string = r'第.*?部第.*?章节'
    maker_setup_note_source = re.sub(regexp_string, 'mark', filter_note_source)
    print(maker_setup_note_source)

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


def replace_text_short_name_with_roles_full_name(text_source):
    """替换某些缺省人物名称, 方便统计"""
    match_name_list = [r'林道静', r'余永泽', r'卢嘉川', r'王晓燕', r'白莉苹', ]
    replace_name_list = ['道静', '永泽', '嘉川', '晓燕', '莉苹', ]

    filter_note_source = text_source
    for match_name, replace_name in zip(match_name_list, replace_name_list):
        # print(match_name)
        filter_note_source = re.sub(match_name, replace_name, filter_note_source, flags=re.I | re.S)

    return filter_note_source


def get_stopword_list(file):
    with open(file, 'r', encoding='utf-8') as f:  #
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list


def filter_out_stopword(source):
    # filter out stop word
    stopword_list = get_stopword_list(get_file_path('hit_stopwords.txt'))
    word_list = jieba.lcut(source)
    result = ""

    for w in word_list:
        if w not in stopword_list:
            result += w

    return result


def get_chapter_list(note_path):
    print(note_path)
    """ 获取章节list, 未分词 """
    note_source = get_word_list(note_path)
    # filter_note_source = get_filter_source_symbols(note_source)

    maker_setup_note_source = note_source
    regexp_string = r'（第.*章节'
    maker_setup_note_source = re.sub(regexp_string, 'mark', maker_setup_note_source)

    # print(maker_setup_note_source)
    maker_setup_note_source = replace_text_short_name_with_roles_full_name(maker_setup_note_source)

    # filter out stop word
    maker_setup_note_source = filter_out_stopword(maker_setup_note_source)

    # print(maker_setup_note_source)
    maker_string = r'mark'
    chapter_list = re.split(maker_string, maker_setup_note_source)

    del chapter_list[0]

    return chapter_list


def save_chapter_count_to_csv_file(chapter_list, csv_name):
    """
    每章分词 保存为csv
    """
    jieba.load_userdict(get_file_path('dict.txt'))

    i = 1
    total_chapter_index, total_data, total_data_count = [], [], []
    for single_chapter in chapter_list:
        # print(single_chapter, '\n\n ------------------------------------')

        single_chapter = filter_out_stopword(single_chapter)
        split_word_list = list(jieba.cut(single_chapter, cut_all=False))

        result, count = np.unique(split_word_list, return_counts=True)
        data, data_count = get_data_without_single_word(result, count)

        total_chapter_index += np.full_like(data, i, dtype=int).tolist()
        total_data += data.tolist()
        total_data_count += data_count.tolist()
        i += 1

    stack_data = {
        'chapter': total_chapter_index,
        'word': total_data,
        'count': total_data_count
    }
    df = pd.DataFrame(stack_data)

    df.to_csv(csv_name)

    print("ok! csv_file => {}".format(csv_name))


def save_volume_count_to_csv_file(volume_file_path, csv_file_path):
    # 小说 每卷分词 (第一卷 , 第二卷)
    source = get_word_list(volume_file_path)
    jieba.load_userdict(get_file_path('dict.txt'))

    # 更多的筛选文本的补充函数, 输入文本, 输出过滤后的文本
    source = replace_text_short_name_with_roles_full_name(source)
    source = filter_out_stopword(source)

    # print(filter_source)
    split_word_list = list(jieba.cut(source, cut_all=False))
    result, count = np.unique(split_word_list, return_counts=True)

    # 过滤 单个字符以及字符
    data, data_count = get_data_without_single_word(result, count)
    sort_data, sort_data_count = get_sort_data(data, data_count)

    df = pd.DataFrame({'word': sort_data, 'count': sort_data_count})
    df.to_csv(csv_file_path)
    print("ok! csv_file => {}".format(csv_file_path))
