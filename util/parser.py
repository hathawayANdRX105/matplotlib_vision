import re

import PIL.Image as image
import jieba
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud


# word cloud
def get_word_list(word_list_path):
    f = open(word_list_path, encoding='utf-8')
    wordList = f.read()
    return wordList


def get_word_cloud(word_list_path, img_mask_path):
    word_list = get_word_list(word_list_path)
    img_mask = np.array(image.open(img_mask_path))

    # load wordlist and set background image mask
    font_path = r"C:\Windows\Fonts\simhei.ttf"
    wordcloud = WordCloud(font_path=font_path, background_color='white', mask=img_mask).generate(word_list)

    plt.axis('off')  # undisplay axies
    plt.imshow(wordcloud)


def get_specified_len_word_cloud(specified_data, specified_count, mask_path):
    word_join = ""
    all_list = []

    for word, count in zip(specified_data, specified_count):
        temp_list = []
        temp_list.append(word)

        temp_list = temp_list * count

        all_list += temp_list


def get_filter_source_symbols(source):
    r_en = "[A-Za-z0-9_.!+-=——,$%^~@#￥%……&*《》<>「」{}()/\\\[\]'\"]"
    filter_en_source = re.sub(r_en, '', source)
    r_cn = r"[，。？ \n\t：！“”（）【】、；]"
    filter_cn_source = re.sub(r_cn, '', filter_en_source)

    return filter_cn_source


def get_sort_data(data, data_count):
    arg_index = data_count.argsort()

    sort_data = data[arg_index]
    sort_count = data_count[arg_index]
    return sort_data, sort_count


def get_data_without_single_word(sort_result, sort_count):
    i = 0
    single_word_indexs = []
    for word in sort_result:
        if len(word) <= 1:
            single_word_indexs.append(i)

        i += 1

    data = np.delete(sort_result, single_word_indexs)
    data_count = np.delete(sort_count, single_word_indexs)

    return data, data_count


def get_data(word_list_path):
    source = get_word_list(word_list_path)
    filter_source = get_filter_source_symbols(source)

    split_word_list = list(jieba.cut(filter_source, cut_all=False))
    result, count = np.unique(split_word_list, return_counts=True)

    data, data_count = get_data_without_single_word(result, count)

    sort_data, sort_data_count = get_sort_data(data, data_count)

    return sort_data, sort_data_count


def get_top_data(topNum, data, data_count):
    size = len(data)
    from_index = size - topNum

    return data[from_index:], data_count[from_index:]


def getSpecifiedLenWord(slen, data, count):
    unsatisfiedIndexs = []
    i = 0

    for word in data:
        if len(word) != slen:
            unsatisfiedIndexs.append(i)

        i = i + 1

    data = np.delete(data, unsatisfiedIndexs)
    count = np.delete(count, unsatisfiedIndexs)

    return data, count
