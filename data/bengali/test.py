#%%
from bnlp import BasicTokenizer

basic_tokenizer = BasicTokenizer()
raw_text = "আমি বাংলায় গান গাই।"
tokens = basic_tokenizer.tokenize(raw_text)
print(tokens)


#%%
from bnlp import NLTKTokenizer

bnltk = NLTKTokenizer()
text = "আমি ভাত খাই। সে বাজারে যায়। তিনি কি সত্যিই ভালো মানুষ?"
word_tokens = bnltk.word_tokenize(text)
sentence_tokens = bnltk.sentence_tokenize(text)
print(word_tokens)
print(sentence_tokens)
