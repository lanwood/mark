"""
数据： 一个csv文本，将近10w条文本
以下处理：
1. 去除所有的标点符号
2. 去除所有括号内的东西
3. 去除长度最短的10%文本和长度最长的10%文本
4. 统计每一条保留的数据里边，每个字符的个数 => characters count vector

python -m cProfile -o text_process.out text_process.py  # python代码性能分析模块运行
python -c "import pstats; p=pstats.Stats('text_process.out'); p.print_stats()" # 进一步分析
python -c "import pstats; p=pstats.Stats('text_process.out'); p.sort_stats('time').print_stats()"

python -m http.server
"""
from typing import List

import pandas as pd
from tqdm import tqdm
from collections import Counter
import re
import multiprocessing as mp


def remove_non_char(need_clean):
    non_char = ',，.。【】[]*、/\|:""@!！'
    for c in non_char:
        need_clean = need_clean.replace(c, ' ')
    return need_clean


non_char = re.compile('[,，\.。【】\[\]\*、\|:;"\'!！\? ？]')


def remove_non_char_re(need_clean):
    return non_char.sub(' ', need_clean)


pattern = re.compile('[\(\（\{].*?[\)\）\}]')


def remove_all_brackets_re(need_clean):
    return pattern.sub('', need_clean)


def remove_all_brackets(need_clean):
    find_bracket_begin = False
    find_bracket_end = False

    result = ""
    for c in need_clean:
        if c in '(（' and not find_bracket_begin:
            find_bracket_begin = True
            find_bracket_end = False
            continue
        elif c in ')）' and not find_bracket_end:
            find_bracket_end = True
            find_bracket_begin = False
            continue
        elif find_bracket_begin and not find_bracket_end:
            continue
        else:
            result += c

    return result


def rank_length(text):
    ranked = sorted(text, key=len)  # n * log(n)
    return ranked[int(len(text) * 0.1): int(len(text) * 0.9)]


def counter_to_text(counter):
    result = ''
    for word, times in counter.items():
        if not word.strip(): continue
        result += '\t{}:{}'.format(word, times)
    return result


def counter_to_text_v2(counter):
    return str(dict(counter))


def reduce_fn(functions: List, init):
    if not functions: return init
    return reduce_fn(functions[1:], functions[0](init))


def clean_by_funcs(functions):
    def _wrap(s):
        return reduce_fn(functions, s)
    return _wrap


def process_chunk(chunk, index):
    news = chunk
    news = news.fillna('')

    functions = [
        remove_all_brackets_re,
        remove_non_char
    ]

    clean = clean_by_funcs(functions)
    news['content'].apply(lambda s: clean(s))

    all_length_medium = rank_length(news['content'].tolist())

    print(all_length_medium[:10])

    with open('words_count_{}.out'.format(index), 'w', encoding='gb18030') as f:
        for text in all_length_medium:
            counter = Counter(text)
            f.write('\n')
            f.write(counter_to_text_v2(counter)) # v3


if __name__ == '__main__':
    CHUNK_SIZE = 15000

    test_string = """
        知乎答主@小司（北京市政设计研究总院工程师）解释道，觉得火车声音大是人离得近。
        平常在站台上等火车、远远看到火车正在进站时，其实我们是听不到什么噪声的，除非鸣笛。
        当火车开进站台后，离得越来越近，我们才能慢慢听到电机的噪音和轮轨声。
        而在正线上，假设火车以100km/h的速度行驶（K字头最高限速120），每秒27米。
        当我们能听到火车的噪声时，一般距离我们只有不足200米了，此时，火车大概6~7秒就可以到达人的面前。
        反应稍微慢点，是很可能跑不出铁轨范围的!
    """
    print(remove_non_char_re(test_string))
    print(remove_all_brackets_re(test_string))

    exit(0)

    # v6
    CPU_NUM = 4
    pools = mp.Pool(CPU_NUM)

    # news = pd.read_csv('data/news.csv', encoding='gb18030') # v5
    news = pd.read_csv('data/news.csv', encoding='gb18030', usecols=['content'], chunksize=CHUNK_SIZE)  # v5

    funcs = []
    for i, chunk in enumerate(news):
        f = pools.apply_async(process_chunk, [chunk, i])
        funcs.append(f)

    for f in funcs:
        f.get()

    # v6
    # news = news.fillna('')
    # precessed = []
    #
    # # v3
    # functions = [
    #     remove_all_brackets_re,
    #     remove_non_char
    # ]
    #
    # # v3
    # # for i, row in tqdm(enumerate(news.iterrows())):
    # #     _, info = row
    # #     # precessed.append(remove_non_char(remove_all_brackets(info['content'])))  # v1
    # #     # precessed.append(remove_non_char(remove_all_brackets_re(info['content'])))  # v2
    # #     precessed.append(reduce_fn(functions, info['content']))  # v3
    # # news['content'] = precessed
    #
    # # v4
    # clean = clean_by_funcs(functions)
    # news['content'].apply(lambda s: clean(s))
    #
    # all_length_medium = rank_length(news['content'].tolist())
    #
    # print(all_length_medium[:10])
    #
    # with open('words_count.out', 'w', encoding='gb18030') as f:
    #     for text in all_length_medium:
    #         counter = Counter(text)
    #         f.write('\n')
    #         # f.write(counter_to_text(counter)) # v1
    #         f.write(counter_to_text_v2(counter)) # v3
