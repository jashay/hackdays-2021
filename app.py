from flask import Flask, render_template, request
#from recipe_recommendation import make_queue
from queue import PriorityQueue
import pandas as pd
from check_similarity import is_similar
from collections import defaultdict
from multiprocessing import Pool
from object_detection import *
import numpy as np


#lst_in = []

print("reading pandas")
df = pd.read_csv("Final_Recipes_v2.csv")
df_copy = pd.read_csv("Recipes.csv")
print("READ")
q = PriorityQueue()

def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def modded_make_queue(df):
    for i in range(len(df["Ingredients"])):
        print(df["Ingredients"].iloc[i])
        score = is_similar(df["Ingredients"].iloc[i], ' '.join(lst_in))
        print(score)
        q.put((-score, i))
    return df


def make_queue(list_ing_recipe):
    #global q
    #global lst_in
    #lst_in = list_ing_recipe
    print("making queue")

    q = PriorityQueue()

    for i in range(len(df["Ingredients"].dropna())):
        try:
            score = is_similar(df["Ingredients"].iloc[i], ' '.join(list_ing_recipe))
            print(score)
            q.put((-score, i))
        except:
            continue

    #parallelize_dataframe(df, modded_make_queue)

    lst = [q.get() for _ in range(5)]
    q = PriorityQueue()
    print(lst)
    res = []


    def get_missing(lst1, lst2):
        for w in lst1:
            if w.lower() not in list(map(lambda x: x.lower,lst2)):
                yield w
    '''
    def string_format(l):
        l = l[1:-1].split(",")
        s = ""
        for word in l:
            s += "<li>" + word[1:-1].replace("'", "").replace('"', '') + "</li>"
        return s
    '''

    '''
    def rec_format(s):
        t = ""
        s = s.split(".")
        for word in s:
            if not word.isdigit():
                t += "<li>" + word + "</li>"
        return t
    '''

    for pair in lst:
        index = pair[1]
        d = {}
        d["title"]=df["Title"].iloc[index]
        d["ingredients"]=df_copy["Ingredients"].iloc[index]
        d["recipe"]=df["Instructions"].iloc[index]
        d["missing"]='\n'.join(set(get_missing(df["Ingredients"].iloc[index].split(), list_ing_recipe)))
        res.append(d)
    return res


def gen_div_from_dict(lst_dict):
    flag = True
    x = ""
    count = 0
    string_html = '</br></br><div class="row"><div class="col-4"><div class="list-group" id="list-tab" role="tablist">'
    for d in lst_dict:
        value = d["title"]
        if flag:
            x = "active"
            flag = False
        string_html+='<a class="list-group-item list-group-item-action '+x+'" id="list-'+str(count)+'-list" data-toggle="list" href="#list-'+str(count)+'" role="tab" aria-controls="'+str(count)+'">'+value+'</a>'
        count += 1
        x = ""

    flag = True
    count = 0
    string_html+='</div></div><div class="col-8"><div class="tab-content" id="nav-tabContent">'
    for d in lst_dict:
        if flag:
            x = "active"
            flag = False
        string_html += '<div class="tab-pane fade show '+x+'" id="list-'+str(count)+'" role="tabpanel" aria-labelledby="list-'+str(count)+'-list"><h3>Ingredients</h3><p>'+d["ingredients"]+'</p><h3>Recipe</h3><p>'+d["recipe"]+'</p><h3>Missing Ingredients</h3><p>'+d["missing"]+'</p></div>'
        x = ""
        count += 1
    string_html += '</div></div></div>'

    return string_html
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
@app.route('/', methods=['post', 'get'])
def home():
    message = ''
    success=False
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        inp = get_labels(file1.read())
        print("fn call")
        x = make_queue(inp)
        print("done")
        message = gen_div_from_dict(x)
        success=True

    return render_template('index.html', success=success, resp=message)

if __name__ == "__main__":
    app.run(debug=True)
