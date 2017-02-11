from PurgeData import writeFiles
def process():
    L = []
    with open('./result/train.txt', 'r', encoding='utf-8') as f:
        trainLines = f.readlines()

    with open('./result/tagSet.txt', 'r', encoding='utf-8') as f:
        tagSet = f.readlines()
        tagSet = [item[:-1] for item in tagSet]
        print(tagSet)

    for line in trainLines:
        parts = line.strip().split('$')
        x = parts[0].split(',')
        y = tagSet.index(parts[1])
        L.append(",".join(x) + '$' + str(y))

    return L

writeFiles(process(), './test/test.txt')

