# -*- coding: utf-8 -*-
"""MachineTranslation-with-Transformers-PythonCode.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RIcKVMVRcKVbhoyqpzy2s1KSchS4XJX2
"""

!pip install transformers==4.12.4 sentencepiece

from transformers import *

# source & destination languages
src = "en"
dst = "de"

task_name = f"translation_{src}_to_{dst}"
model_name = f"Helsinki-NLP/opus-mt-{src}-{dst}"

translator  = pipeline(task_name, model=model_name, tokenizer=model_name)

translator("You're a genius.")[0]["translation_text"]

article = """
Albert Einstein ( 14 March 1879 – 18 April 1955) was a German-born theoretical physicist, widely acknowledged to be one of the greatest physicists of all time. 
Einstein is best known for developing the theory of relativity, but he also made important contributions to the development of the theory of quantum mechanics. 
Relativity and quantum mechanics are together the two pillars of modern physics. 
His mass–energy equivalence formula E = mc2, which arises from relativity theory, has been dubbed "the world's most famous equation". 
His work is also known for its influence on the philosophy of science.
He received the 1921 Nobel Prize in Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect", a pivotal step in the development of quantum theory. 
His intellectual achievements and originality resulted in "Einstein" becoming synonymous with "genius"
"""

translator(article)[0]["translation_text"]

def get_translation_model_and_tokenizer(src_lang, dst_lang):
  """
  Given the source and destination languages, returns the appropriate model
  See the language codes here: https://developers.google.com/admin-sdk/directory/v1/languages
  For the 3-character language codes, you can google for the code!
  """
  # construct our model name
  model_name = f"Helsinki-NLP/opus-mt-{src}-{dst}"
  # initialize the tokenizer & model
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
  # return them for use
  return model, tokenizer

# source & destination languages
src = "en"
dst = "zh"

model, tokenizer = get_translation_model_and_tokenizer(src, dst)

# encode the text into tensor of integers using the appropriate tokenizer
inputs = tokenizer.encode(article, return_tensors="pt", max_length=512, truncation=True)
print(inputs)

# generate the translation output using greedy search
greedy_outputs = model.generate(inputs)
# decode the output and ignore special tokens
print(tokenizer.decode(greedy_outputs[0], skip_special_tokens=True))

# generate the translation output using beam search
beam_outputs = model.generate(inputs, num_beams=3)
# decode the output and ignore special tokens
print(tokenizer.decode(beam_outputs[0], skip_special_tokens=True))

# let's change target language
src = "en"
dst = "ar"

# get en-ar model & tokenizer
model, tokenizer = get_translation_model_and_tokenizer(src, dst)

# yet another example
text = "It can be severe, and has caused millions of deaths around the world as well as lasting health problems in some who have survived the illness."
# tokenize the text
inputs = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)
# this time we use 5 beams and return 5 sequences and we can compare!
beam_outputs = model.generate(
    inputs, 
    num_beams=5, 
    num_return_sequences=5,
    early_stopping=True,
)
for i, beam_output in enumerate(beam_outputs):
  print(tokenizer.decode(beam_output, skip_special_tokens=True))
  print("="*50)

