# ChineseWordSegmentation
Chinese word segmentation algorithm without corpus

## Usage
```
from wordseg import WordSegment
doc = u'十四是十四四十是四十，十四不是四十，四十不是十四'
ws = WordSegment(doc, max_word_len=2, min_aggregation=1, min_entropy=0.5)
ws.segSentence(doc)
```

This will generate words

`十四 是 十四 四十 是 四十 ， 十四 不是 四十 ， 四十 不是 十四`

In fact, `doc` should be a long enough document string for better results. In that condition, the min_aggregation should be set far greater than 1, such as 50, and min_entropy should also be set greater than 0.5, such as 1.5.

Besides, both input and output of this function should be decoded as unicode.

`WordSegment.segSentence` has an optional argument `method`, with values `WordSegment.L`, `WordSegment.S` and `WordSegment.ALL`, means

+ `WordSegment.L`: if a long word that is combinations of several shorter words found, given only the long word.
+ `WordSegment.S`: given the several shorter words.
+ `WordSegment.ALL`: given both the long and the shorters.

## Reference

Thanks Matrix67's [article](http://www.matrix67.com/blog/archives/5044)

## Find—new-words part

Functions:
Find new words and only keep good quality words.
过滤英文单字，符号，数字和中文单字
通过设置aggregation和entropy的上下限和步长来进行多次循环分词并记录所有出现的新词和其在实验中出现的次数，以键值对的形式在self.result中。

例如：aggregation从1到10，步长为1；entropy从0.1到1.5，步长为0.1，共进行10 * 15=150次分词，假设其中“程维”出现了100次，则在self.result中记录：{‘程维’：100}

继续通过appear rate生成新词，以列表形式存进self.new_word中。

接上例：假设新词字典中最高出现的次数为140，key为‘滴滴’，此时appear rate设置为默认值0.5，则出现次数小于等于70的所有新词会被过滤掉，只有剩下的会存进新词列表new_word。

aggregation，entropy和appear rate参数均可调，试验次数越多，覆盖范围越广新词的质量越好，如追求高精确率（precision）则可适当调高appear rate进行更严格的删选；追求高召回率（recall）和降低appear rate使结果包括更多新词。

实例请参考example notebook。函数说明请参照fliter_new.py
