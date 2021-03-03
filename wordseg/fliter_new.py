"""
Simple algorithm to fliter new words
Author: Hao Wang 王昊
"""

from wordseg import WordSegment
from tqdm import tqdm
import numpy as np

class find_new(object):
    '''
	find new words that not belong to previous dictionary
	Run multiple cycle of word segment to find new words of best quality
	@params maxmin_aggregation: the largest threshold of aggregation
			maxmin_entropy: the largest threshold of entropy
			minmin_aggregation: the smallest threshold of aggregation
			minmin_entropy: the smallest threshold of entropy
			aggregation_step: the step of aggregation parameter move from minmin_aggregation to maxmin_aggregation
			entropy_step: the step of entropy parameter move from minmin_entropy to maxmin_entropy
			total_cycle_num: computed from above params, used to show the tqdm bar
			appear_rate: determine which are qualified words in dictionary, only words that appears more than the 
						rate in all segmentation will be regarded as new words.
						
	@variables	doc: the document used to get new words
				dic: the dictionary of existed words
				result: the dictionary of all new words, {new words:the number of new words appeared in all segmentations}
				new_word: the list used to store all qualified new words
	
	@funcs	set_cycle_parameter: set params about segmentation cycle
			complete_dic: add symbols, numbers, english characters to the dictionary
			run_cycle: run cycle and record all new words in self.result
			generate_new_words: use appear_rate to fliter new words
			get_new_words: run complete_dic(optional) --> run_cycle --> generate_new_words, then return self.new_word
			
	'''
	
    def __init__(self,doc,dic,appear_rate=0.5,max_word_len=5):
        from tqdm import tqdm
        self.doc = doc
        self.dic = dic
        self.appear_rate = appear_rate
        self.result = {}
        self.new_word = []
        self.maxmin_aggregation=20
        self.maxmin_entropy=2
        self.minmin_aggregation=1
        self.minmin_entropy=0.1
        self.aggregation_step=1
        self.entropy_step=0.1
        self.max_word_len = max_word_len
        self.total_cycle_num = ((1+(self.maxmin_aggregation-self.minmin_aggregation)//self.aggregation_step))*\
        (1+((self.maxmin_entropy-self.minmin_entropy)//self.entropy_step))
    
    def set_cycle_parameter(self,maxmin_aggregation,maxmin_entropy,minmin_aggregation,minmin_entropy,aggregation_step,entropy_step):
        self.maxmin_aggregation=maxmin_aggregation
        self.maxmin_entropy=maxmin_entropy
        self.minmin_aggregation=minmin_aggregation
        self.minmin_entropy=minmin_entropy
        self.aggregation_step=aggregation_step
        self.entropy_step=entropy_step
    
    def complete_dic(self,add_on=[' ','.','+','\n','%',':','!']):
        for i in range(10):
            self.dic.append(str(i))
        small = [chr(i) for i in range(97,123)]
        big = [chr(i) for i in range(65,91)]
        self.dic = self.dic+add_on+small+big
        print('dic updated.')
        
    def run_cycle(self,fliter_one_character=True):
        temp_res = {}
        pbar = tqdm(total=self.total_cycle_num)
        for i in np.arange(self.minmin_aggregation,self.maxmin_aggregation+self.aggregation_step,self.aggregation_step):
            for j in np.arange(self.minmin_entropy,self.maxmin_entropy+self.entropy_step,self.entropy_step):
                pbar.update(1)
                ws = WordSegment(self.doc, max_word_len=self.max_word_len, min_aggregation=i, min_entropy=j)
                news_dic = set(ws.segSentence(self.doc))
                for word in news_dic:
                    if word not in temp_res:
                        temp_res[word]=1
                    else:
                        temp_res[word]+=1
        for key in temp_res:
            if fliter_one_character:
                if key not in self.dic and len(key)>1:
                    self.result[key]=temp_res[key]
            else:
                if key not in self.dic:
                    self.result[key]=temp_res[key]
                
                
    def generate_new_words(self,clear_previous_new_word=True):
        if clear_previous_new_word:
            self.new_word = []
        max_appear_time = self.result[max(self.result,key=self.result.get)]
        threshold = max_appear_time*self.appear_rate
        for key in self.result:
            if self.result[key] >= threshold:
                self.new_word.append(key)
        print("new word dictionary generated.")
        
    def get_new_words(self, default_add_on = True,fliter_one_character=True):
        self.new_word = []
        if default_add_on:
            self.complete_dic()
        self.run_cycle(fliter_one_character)
        self.generate_new_words()
        return self.new_word