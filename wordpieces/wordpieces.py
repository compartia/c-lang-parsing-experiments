import operator

class WPDictBuilder(object):
    def __init__(self, max_chunk_len=4):
        self.stats={}
        self.max_chunk_len = max_chunk_len

    def learn_sentense(self, sentence):
        for n in range(1, self.max_chunk_len):
            pieces = splitIntoWordpieces(n, sentence)
            countWordpieces(pieces, self.stats)

    def sorted_wordpieces(self):
        return sortWordpieces(self.stats)

    def trim_stats(self, max_number_of_words):
        sortedWordpieces = self.sorted_wordpieces()
        self.stats = dict(sortedWordpieces[0:max_number_of_words])

    def build(self, max_number_of_words):
        sortedWordpieces = self.sorted_wordpieces()[0:max_number_of_words]
        print ("building WPDict of size %d"%len(sortedWordpieces))
        wp_dict = WPDict(dict(sortedWordpieces), self.max_chunk_len)
        return wp_dict

class WPDict(object):
    def __init__(self, _stats, max_chunk_len=4):
        self.max_chunk_len = max_chunk_len
        self.stats=_stats

    def find_longest_chunk(self, word):
        for i in range(self.max_chunk_len, 1, -1):
            chunk=word[0:i]
            if(chunk in self.stats):
                return chunk,i
        return "<UNK>",1


    def break_sentence(self, sentence):
        words=sentence.split()
        for word in words:
            for chunk in self.break_word(word):
                yield chunk

    def break_word(self, word):
        _word='_' + word
        while len(_word)>0:
            chunk, n = self.find_longest_chunk(_word)
            yield chunk
            _word=_word[n:]

    def joinSentence(self, chunks):
        replacements=[]
        if(chunks[0][1:].startswith("_")):
            replacements.append(chunks[0][1:])
        else:
            replacements.append(chunks[0])
            
        for chunk in chunks[1:]:
            if '_'==chunk[0:1]:
                replacements.append(' ')
                replacements.append(chunk[1:])
            else:
                replacements.append(chunk)

        return "".join(replacements)


def splitIntoWordpieces(chunk_len, sentence):
    words=sentence.split()
    for word in words:
        if(chunk_len>1):
            _word='_' + word
        else:
            _word=word
        for i in range(0, len(_word), chunk_len):
            yield _word[i:i + chunk_len]

def sortWordpieces(wordcount):
    return sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)

def countWordpieces(pieces, wordcount={}):
    for word in pieces:
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    return wordcount;
