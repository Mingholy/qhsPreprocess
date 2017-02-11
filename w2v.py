from PurgeData import writeFiles

# 保留特定标签的词
includeTags = ['a', 'ad', 'ag', 'al', 'an', 'b', 'bl', 'd', 'dg', 'dl', 'g', 'gb', 'gbc', 'gc', 'gg',
               'gi', 'gm', 'gp', 'n', 'nb', 'nba', 'nbc', 'nbp', 'nf', 'ng''nh', 'nhd', 'nhm', 'ni', 'nic',
               'nis', 'nit', 'nm', 'nmc', 'nn', 'nnd', 'nnt', 'nr', 'nr', 'nr', 'nrf', 'nrj', 'nsf', 'nt', 'ntc',
               'ntcb', 'ntcf', 'ntch', 'nth', 'nto', 'nts', 'ntu', 'nx', 'nz', 'o', 'p', 's', 't', 'v', 'vd',
               'vf', 'vg', 'vi', 'vl', 'vn', 'vshi', 'vx', 'vyou', 'y', 'yg', 'z', 'zg']

def wordFilter(inputUrl):
    filtered = []
    with open(inputUrl, 'r', encoding='utf-8') as fileIn:
        for rawLine in fileIn:
            filtered.append(posFilter(rawLine))
    return filtered

def posFilter(rawLine):
    line = []
    string =''
    rawLine = rawLine.replace('%', '').replace('\s\s+', ' ')
    tokens = rawLine.split(' ')
    tag = tokens[-1]
    for token in tokens:
        word = (token.split('/'))[0]
        posTag = (token.split('/'))[-1]
        if posTag in includeTags:
            line.append(word)
    for w in line:
        string = string +' ' + w
    return string + tag

def prepareTrainData(filteredList):
    dict = []
    tags = []
    trainData = []
    for rawLine in filteredList:
        trainLine = []
        tag = rawLine.split(('&&'))[-1].strip()
        if tag not in tags:
            tags.append(tag)
        sentence = (rawLine.split('&&'))[0].strip().split(' ')
        for word in sentence:
            if word not in dict:
                dict.append(word)
            trainLine.append(str(dict.index(word)))
        trainData.append(",".join(trainLine) + '$' + (rawLine.split('&&'))[-1].strip())
    return dict, tags, trainData

dictionary, tagSet, train = prepareTrainData(wordFilter('./temp/POS.txt'))
writeFiles(dictionary, './result/dictionary.txt')
writeFiles(tagSet, './result/tagSet.txt')
writeFiles(train, './result/train.txt')

