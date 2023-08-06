import nbformat as nbf

def push_cmd(file_name = None,codes = None):
    fname = 'speech-generated-ML.ipynb'
    try:
        with open(fname) as fp:
            notebook = nbf.read(fp, nbf.NO_CONVERT)
        cells = notebook['cells']
        if(file_name is None):
            cells.append(nbf.v4.new_code_cell(codes))
            print("Done with adding single code!")
        else:
            f = open(file_name, "r")
            cells.append(nbf.v4.new_code_cell(f.read()))
            print("Done with adding code from file!")
        with open(fname, 'w') as f:
            nbf.write(notebook, f)
    except:
        nb = nbf.v4.new_notebook()
        text = """#Speech-generated Machine Learning Script by Speech2ML
        All rights reserved by Tony Dong."""
        nb['cells'] = [nbf.v4.new_markdown_cell(text)]
        print('Done with create Speech-gnerated Machine Learning Script')
        if(file_name is None):
            nb['cells'].append(nbf.v4.new_code_cell(codes))
            print("Done with adding single code!")
        else:
            f = open(file_name, "r")
            nb['cells'].append(nbf.v4.new_code_cell(f.read()))
            print("Done with adding code from file!")
        with open(fname, 'w') as f:
            nbf.write(nb, f)
        
    
    # f = open("./optimalflow/selectorFS.py", "r")


# push_cmd(codes= """print('Hello World!')""")
# push_cmd(file_name ="./optimalflow/selectorFS.py")
# push_cmd(codes= """print('Hello Universe!')""")
# push_cmd(file_name ="./optimalflow/autoPP.py")

from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import re
a_string = "A string is more than its parts!"
# word_list = list(a_string)
a_string = re.sub(r"[^A-Za-z\s]", "", a_string.strip())
text_tokens = word_tokenize(a_string)
filtered_words = [w.lower() for w in text_tokens if w.lower() not in stopwords.words('english')]
filtered_sentence = (" ").join(filtered_words)
filtered_sentence


def cmd_identify(text = None,lev_thresh = 3):
    text = re.sub(r"[^A-Za-z\s]", "", text.strip())
    text_tokens = word_tokenize(text)
    filtered_words = [w.lower() for w in text_tokens if w.lower() not in stopwords.words('english')]
    filtered_sentence = (" ").join(filtered_words)
    cmd_01 = ['load','input','dataset']
    cmd_02 = ['feature','selection']
    cmd_03 = ['feature','prepare']
    cmd_04 = ['split','dataset']
    cmd_05 = 
    if all(x in filtered_sentence for x in cmd_01) and jellyfish.levenshtein_distance(filtered_sentence, 'load input data') <=3:
        return("Load_input_dataset")
    elif

