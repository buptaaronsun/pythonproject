# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @Email   :
# @File    : main.py
# @Software: PyCharm

# 引入python自带的os包
import os
# pandas
import pandas as pd
# 云图第三方包WordCloud
from wordcloud import WordCloud
# 分词第三方包jieba
import jieba
# 在numpy基础上的一个操作numpy数组的函数库, scipy,imread模块用于读取图
# from scipy.misc import imread
# 画图第三方包
import matplotlib.pyplot as plt
# 一个高性能的多维数组的计算库
import numpy as np
# 读入图片
from scipy.misc import imread


"""
初始化操作,创建目录
"""
def init():
    # 目录名
    path = "pic"
    # 判断路径是否存在
    # 存在    true
    # 不存在   False
    isExists =  os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        os.mkdir(path)
        print(path + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')

"""
读取文件
@param: 文件名
@return: 文件内容
"""
def readFile(filename):
    # 初始化s
    s = ""
    # 打开文件
    with open(filename, 'r', encoding='utf-8') as f:
        # 读取文件内容
        s = f.read()
    # 返回文件内容
    return s

"""
读取正面词负面词文件
@param: 文件名
@return: 文件内容
"""
def readFileWords(filename):
    # 初始化s
    ss = []
    result = []
    # 打开文件
    with open(filename, 'r',encoding='utf-8') as f:
        # 读取文件内容
        ss = f.read().split()
        result = list(map(lambda  x: x.strip(), ss))
    # 返回文件内容
    return result

"""
统计文件内容
@:param filename，文件名
@:return freq20 前n个频率数组
@:return words20 前n个单词数组
@:return N 前多少个
@:return filecontent, 文件内容
"""
def statisticalFile(filename, people, positiveFilePath, negativeFilePath):
    # 需要统计词频的文件名称
    # 文件内容
    filecontent = readFile(filename)
    positiveWords = readFileWords(positiveFilePath)
    negativeWords = readFileWords(negativeFilePath)

    print('positiveWords', positiveWords[0:10])
    print('negativeWords', negativeWords[0:10])
    #读取停用词，创建停用词表
    stwlist = [line.strip() for line in open('chineseStopWord.txt', encoding='utf-8').readlines()]
    # 先进行分词, cut_all:是否采用全模式,HMM：是否采用HMM模型
    jieba.load_userdict("people.txt")
    # 动态调整词频，让未登录词的词频自动靠前，这样可以优先匹配
    [jieba.suggest_freq(line.strip(), tune=True) for line in open('people.txt', 'r', encoding ='utf-8')]
    words = jieba.cut(filecontent, cut_all=False, HMM=True)

    # 去停用词,统计词频
    word_ = {}
    # 遍历结巴分词结果
    for word in words:
        # 如果不再停用此中
        if word.strip() not in stwlist:
            # 如果单词不为空
            if len(word) > 1:
                # 如果单词不为\t
                if word != '\t':
                    # 如果单词不为\r\n
                    if word != '\r\n':
                        # 计算词频
                        if word in word_:
                            # 递增一
                            word_[word] += 1
                        else:
                            # 初始化为1
                            word_[word] = 1

    # 将词汇和词频以元组的形式保存
    word_freq = []
    # 遍历
    for word, freq in word_.items():
        # 添加到单词频率数组中
        word_freq.append((word, freq))

    # 进行降序排列
    word_freq.sort(key=lambda x: x[1], reverse=True)
    # 前10人物名称数组，前10人物词频数组
    human10, humanFreq10 = [], []
    # 前10正面词名称数组，前10正面词词频数组
    positive10, positiveFreq10 = [], []
    # 前10负面词名称数组，前10负面词词频数组
    negative10, negativeFreq10 = [], []
    # 前N个
    N = 10
    # 查看前10个结果
    for i in range(1000):
        if word_freq[i][0] in people and len(human10) <10:
            word, freq = word_freq[i]
            # 将单词放到words20
            human10.append(word)
            # 将频率放到freq20
            humanFreq10.append(freq)
        if word_freq[i][0] in positiveWords and len(positive10) <10:
            word, freq = word_freq[i]
            # 将单词放到words20
            positive10.append(word)
            # 将频率放到freq20
            positiveFreq10.append(freq)
        if word_freq[i][0] in negativeWords and len(negative10) <10:
            word, freq = word_freq[i]
            # 将单词放到words20
            negative10.append(word)
            # 将频率放到freq20
            negativeFreq10.append(freq)
    # 输出结果
    print('人物词频统计前10:')
    for i in range(N):
        print('{0:10}{1:5}'.format(human10[i], humanFreq10[i]))
    print('正面词词频统计前10:')
    for i in range(N):
        print('{0:10}{1:5}'.format(positive10[i], positiveFreq10[i]))
    print('负面词词频统计前10:')
    for i in range(N):
        print('{0:10}{1:5}'.format(negative10[i], negativeFreq10[i]))
    # 返回结果
    dataHuman = pd.DataFrame({'word': human10, 'frequence': humanFreq10})
    dataPositive = pd.DataFrame({'word': positive10, 'frequence': positiveFreq10})
    dataNegative = pd.DataFrame({'word': negative10, 'frequence': negativeFreq10})
    dataHuman.to_csv("人物词频统计前10.csv")
    dataPositive.to_csv("正面词词频统计前10.csv")
    dataNegative.to_csv("负面词词频统计前10.csv")
    return humanFreq10, human10,positiveFreq10, positive10, negativeFreq10, negative10, N, filecontent

"""
绘制柱状图
@:param freq20 前n个频率数组
@:param words20 前n个单词数组
@:param N 前多少个
"""
def getBarMap(words20, freq20, N, title):
    # 生成词频柱状图
    # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
    plt.figure(figsize=(12, 6), dpi=80)
    # 包含每个柱子下标的序列
    index = np.arange(N)
    # 柱子的宽度
    width = 0.35
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色
    p2 = plt.bar(index, freq20, width, label="rainfall", color="#87CEFA")
    # 设置横轴标签
    plt.xlabel('词语')
    # 设置纵轴标签
    plt.ylabel('频次')
    # 添加标题
    plt.title(title)
    # 添加纵横轴的刻度
    plt.xticks(index, words20)
    # 显示次数
    for a, b in zip(index, freq20):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
    # 保存图片为top20.png
    plt.savefig("./pic/{}.png".format(title))
    # 图片展示
    plt.show()

"""
绘制折线图
@:param freq20 前n个频率数组
@:param words20 前n个单词数组
@:param N 前多少个
"""
def getLineMap(words20, freq20, N):
    # 指定画布大小
    fig = plt.figure(figsize=(12,6))
    # 绘制折线图,指定颜色为空色
    plt.plot(words20, freq20,c='red')
    # 保存图片为top20line.png
    plt.savefig("./pic/top20line.png")
    # 图片展示
    plt.show()

"""
生成云图
@:param: filecontent, 数据文件内容
"""
def getCloudMap(filecontent, mask, people):
    font = './font/SimHei.ttf'

    # 生成云图
    # 全部转换为小写
    f = filecontent.replace('道','')
    f = f.replace('心想', '')
    f = f.replace('笑', '')
    f = f.replace('盈盈', '')

    #创建worldcloud对象，并设置形状图为lufei.jpeg
    wordcloud = WordCloud(background_color="white",stopwords = people, mask=mask, font_path=font, width=800, height=660, margin=2).generate(f)

    # 展示云图
    plt.imshow(wordcloud)
    # x轴取消显示
    plt.axis("off")
    # 云图展示
    plt.show()
    # 保存云图到文件中
    wordcloud.to_file("./pic/wordcloud.png")


"""
主函数，入口文件
"""
if __name__ == '__main__':

    # # 解决显示中文问题
    # plt.rcParams['font.family'] = ['sans-serif']
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # # 解决保存图像是负号'-'的显示问题
    # plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # 数据文件名
    filename = '笑傲江湖.txt'
    # 角色
    people = readFileWords('people.txt')
    print(people)
    # 云图的形状图
    mask = imread("lufei.jpeg")
    #初始化操作
    init()
    # 统计数据
    humanFreq10, human10,positiveFreq10, positive10, negativeFreq10, negative10, N, filecontent = statisticalFile(filename, people, './words/positive.txt', './words/negative.txt')
    # 输出人物出场前10的柱状图
    getBarMap(human10, humanFreq10, N, '人物出场前10的柱状图')
    # 输出正面次前10的柱状图
    getBarMap(positive10, positiveFreq10, N, '输出正面次前10的柱状图')
    # 输出负面次前10的柱状图
    getBarMap(negative10, negativeFreq10, N, '输出负面次前10的柱状图')
    # 输出云图
    getCloudMap(filecontent, mask, people)


