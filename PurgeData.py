# -*- coding: utf-8 -*-
import re

# 句子预处理:数词替换 切分标签
def preProcess(inputUrl, outputUrl = 'preOutput.txt'):
    # 替换数词 保留特殊带数词的名词
    chineseNumber = ['placeholder','二', '三', '四', '五', '六', '七', '八', '九', '十']
    specialTerms = {'2面角':'二面角', '3角形':'三角形', '4边形':'四边形', '5边形':'五边形', '6边形':'六边形', '8边形':'八边形', '1等奖':'一等奖', '2等奖':'二等奖', '3等奖':'三等奖'}
    untagged = []
    with open(inputUrl, 'r', encoding='utf-8') as fileIn:
        with open(outputUrl, 'w', encoding='utf-8') as fileOut:
            for rawLine in fileIn:
                taggedLine = rawLine.split('&&')
                if taggedLine[0] == taggedLine[-1]:
                    untagged.append(taggedLine[0])
                    continue
                line = taggedLine[0]
                for num in chineseNumber:
                    line = line.replace(num, str(chineseNumber.index(num) + 1))
                for term in specialTerms.keys():
                    line = line.replace(term, specialTerms[term])
                line = replaceExpr(line) + '&&' + taggedLine[1]
                fileOut.write(line)
    return untagged

def replaceExpr(string):
    # 匹配整段非中文字符
    regExpProb = r'[0-9a-zA-Z,\+\-\*\/_^><\[\]()≤=≥:μωσ|∞\\\.∈αβ\']+'
    # 匹配表达式中的运算符
    regExpExpr = r'[≤=≥><]'
    # 匹配区间或者坐标
    regExpPair = '[\[(]\d+,\d+[)\]]'
    # 匹配集合或者序列
    regExpSet = ['\d,\d,\.+,\d+', '((\d*\.?\d+,))+(\d*\.?\d+)', '((\d,)+,?)']
    # 匹配单独出现的字母实体
    regExpLetter = '[a-zA-ZαβγΩ\']+'
    # 匹配数字
    regExpNumber = '\d+'
    exStr = ['_,', '()' , '(', ')', ',', '#', '%', '_____']

    results = re.findall(regExpProb, string)
    exprs = ['@表达式']
    entities = ['@实体']
    sets = ['@集合']
    numbers = ['@数量']
    pairs = ['@数对']

    if results:
        for result in results:
            if result not in exStr:
                if re.search(regExpExpr, result):
                    exprs.append(result)
                elif re.search(regExpPair, result):
                    lpairs = re.findall(regExpPair, result)
                    pairs.extend(lpairs)
                elif re.search(regExpSet[0], result):
                    sets.append(result)
                elif re.search(regExpSet[1], result):
                    sets.append(result)
                elif re.search(regExpSet[2], result):
                    sets.append(result)
                elif re.search(regExpLetter, result):
                    entities.append(result)
                elif re.search(regExpNumber, result):
                    numbers.append(result)

    replaceLists = [exprs, pairs, sets, numbers, entities]
    # 区别不同实体的编号
    #alphabet = ['0','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
    for list in replaceLists:
        list = sorted(list, key = keylen, reverse = True)
        for element in list:
            string = string.replace(element, list[0] + ' ')
    for s in exStr:
        if s in string:
            string = string.replace(s, ' ')
    return string

def keylen(string):
    if '@' in string:
        strlen = 9999
    else:
        strlen = len(string)
    return strlen

def writeFiles(list, outUrl):
    with open(outUrl, 'w', encoding='utf-8') as f:
        list = [line + '\n' for line in list]
        f.writelines(list)

untagged  = preProcess('./data/origin-all.txt', './temp/out.txt')
writeFiles(untagged, './warning/untagged.txt')
