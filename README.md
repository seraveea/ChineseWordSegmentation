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

## Find_new_words part

Functions:
Find new words and only keep good quality words.
过滤英文单字，符号，数字和中文单字
通过设置aggregation和entropy的上下限和步长来进行多次循环分词并记录所有出现的新词和其在实验中出现的次数，以键值对的形式在self.result中。

例如：aggregation从1到10，步长为1；entropy从0.1到1.5，步长为0.1，共进行10 * 15=150次分词，假设其中“程维”出现了100次，则在self.result中记录：{‘程维’：100}

继续通过appear rate生成新词，以列表形式存进self.new_word中。

接上例：假设新词字典中最高出现的次数为140，key为‘滴滴’，此时appear rate设置为默认值0.5，则出现次数小于等于70的所有新词会被过滤掉，只有剩下的会存进新词列表new_word。

aggregation，entropy和appear rate参数均可调，试验次数越多，覆盖范围越广新词的质量越好，如追求高精确率（precision）则可适当调高appear rate进行更严格的删选；追求高召回率（recall）可降低appear rate使结果包括更多新词。

实例请参考example notebook。函数说明请参照fliter_new.py

例子中还会有很多不合理的词比如“XX的”，“XX了”，“一XX”等等，可以通过微调appear rate或者通过模式匹配的后处理进行过滤。但在今后的使用中不排除符合相同模式的新词出现，比如‘好好的’，‘一点点’等，所以后处理不能作为必要操作，以免在今后调用中误删新词。

新的模块没有修改之前已有的文件，同时留了大部分参数的接口，详细请参照wordseg/fliter_new.py

## Three questions
### Q1: How to determine the parameters automatically?
在我的实现中，并未记录“最佳”参数并得到由最佳参数得到的分词结果，而是使用了很多组参数进行多次实验并记录的统计结果，最后根据所有新词的出现频率来决定保留与否。这里我的依据是“高质量新词应具有鲁棒性（robust），并对参数的变化不应十分敏感”。例如新词“滴滴”，在各种entropy和aggregation的阈值搭配下都应是会出现在分词结果里的；而典型的无意义分词如“了一个”在严苛的阈值要求下就不会被认作新词。

这里出现了另一个问题，既然新词对参数变化不敏感，为什么不只选用一组严格的参数阈值进行筛选呢？因为这里我们并不能通过数学的方式确定所有的高质量新词都会出现在一组参数下，由于语料库的不同，同一组参数在进行分词时并不一定都能取得好的效果，而且还有可能出现类似于梯度下降中的局部最优问题出现。这里我们可以将entropy和aggregation比作二维空间里的两个坐标轴，将最优分词结果作为最优解，同时两次分词的差异作为梯度。当梯度最小时，也就是两次分词差异最小的时候，此时取得最优解，可以获得新词。但最优解有可能不会包含所有的新词，某些局部最优解可能包含不同的新词。比如，在entropy=5，aggragation=10时，可以取到新词{‘滴滴’，‘程维’，‘新能源’}，但其他的新词如{‘网约车’，‘微信’}有可能在entropy=6，aggragation=5处取得。

如果说需要得到一组参数作为最佳参数，可以使用上面类比的方式做梯度下降，在entropy和aggragation变化时对比两次分词的差异，如果差异很大说明此时的分词结果不稳定，则向任意方向更新参数，由于机器学习中的梯度下降是向梯度为负的方向行进，在分词时我们也可以根据假设“高质量的新词往往是少数”来向新词数量减少的方向行进，当两次分词结果无很大差异时，便可视为已找到最优参数。同时为了防止局部最优解出现，既“得到了稳定的新词但是仍有很多新词并未被记录”，可以设置变异率进行随机跳跃来跳出局部最优，与梯度下降中的方式一致。

###   Q2：How to extract new words with good quality if you have a large corpus which focus on a specific domain, like 100000 pieces of biological paper.
根据上面的方法可以找到较高质量的分词，某一具体领域的
