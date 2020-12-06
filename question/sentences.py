import unidecode
#import pprint
#import nltk
#from nltk.corpus import cess_esp as cess
#nltk.download('punkt')
#nltk.download('averaged_perceptron_taagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')

# to remove any non-alphanumeric character, punctuation, marks.
def removeNonWords(line):
    line = ''.join(e for e in line if e.isalnum() or e.isspace())
    return line

# to normalize special unicode characters to a common unicode character (á , â => a)
def normalizeChars(line):
    line = unidecode.unidecode(line)
    line = line.lower()
    return line

# to remove non-relevant words to analyze
def removeStopWords(stopWords, line):
    querywords = line.split()
    resultwords = [word for word in querywords if word.lower() not in stopWords]
    return ' '.join(resultwords)

# to make groups of n words to create arbitrary sentences
def chunks(list, n):
    for i in range(0, len(list) - n, 1):
        yield ' '.join(list[i:i + n])

# to make groups of n words to create arbitrary sentences, sorting words alphabetically to normalize the pattern
def sortedChunks(list, n):
    for i in range(0, len(list) - n, 1):
        yield ' '.join(sorted(list[i:i + n]))

# to delete all dictionary ocurrences with a value less or equal to maxValue
def dropValues(items, maxValue):
    result = dict(items)
    for key, value in items.items():
        if value <= maxValue:
            del result[key]
    return result

# to sort a dictionary for value (number of ocurrences)
def sortByValue(items, reverse):
    return sorted(items.items(), key=lambda x: x[1], reverse=reverse)

# append info to global statistics: repeated phrases and details
def appendStats(stats, detail, words, line, count):
    sortedPhrases = list(sortedChunks(words, count))
    phrases = list(chunks(words, count))
    key=0
    for phrase in sortedPhrases:
        if phrase in stats:
            stats[phrase] += 1
            detail[phrase]['questions'].append(line)
            detail[phrase]['words'].append(phrases[key])
        else:
            stats[phrase] = 1
            detail[phrase] = {}
            detail[phrase]['questions'] = [line]
            detail[phrase]['words'] = [phrases[key]]
        key+=1
    return stats

def removeDuplicates(items):
    return list(set(items))


# ======================
# Main program execution
# ======================

# select folder to read configuration and data
lang = "en"

# open file and read lines
file = open(lang + "/sentences.txt",encoding="utf8")
# lines = file.readlines()
lines = file.read().splitlines()
lines = removeDuplicates(lines)

file = open(lang + "/stopwords.txt",encoding="utf8")
stopWords = file.read().splitlines()

phrases = {}
details= {}

for line in lines:
    #tokens = nltk.word_tokenize(x)
    #tags = nltk.pos_tag(tokens)
    tmp = removeNonWords(line)
    tmp = normalizeChars(tmp)
    tmp = removeStopWords(stopWords,tmp)
    words = tmp.split()
    phrases = appendStats(phrases, details, words, line, 2)
    phrases = appendStats(phrases, details, words, line, 3)
    phrases = appendStats(phrases, details, words, line, 4)

phrases = dropValues(phrases, 2)

sortedPhrases = sortByValue(phrases, reverse=True)

print ( "Total lines " + str(len(lines)))
list=[]
for key, value in sortedPhrases:
    words = details[key]['words'][0]
    perc = value * 100 / len(lines)
    # print("\n[" + words + "] " + str(value) + " ocurrences (" + ("%.2f" % perc) + "%) :" )
    data="\n[" + words + "] " + str(value) + " ocurrences (" + ("%.2f" % perc) + "%) :" 
    print(data)
    list.append(data)

    for line in details[key]['questions']:
        print(line)
        list.append(line)

list = '\n'.join(list)
file=open("ans.txt","w")    
file.write(str(list))
file.close()    
            
    

# tokens
#tokens = nltk.word_tokenize(sentence)

# tags
#tags = nltk.pos_tag(tokens)

# entities
#entities = nltk.chunk.ne_chunk(tags)


