#! /usr/bin/env python3

import os
import io
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from nlp_funcs import *
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import coo_matrix
from nltk.tokenize import word_tokenize

UPLOAD_FOLDER = "../data/uploaded_data/"
ALLOWED_EXTENSIONS = ['pdf']
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/home', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form['submit-button'] == "upload":


            # first, delete content of upload folder
            for file in os.listdir(UPLOAD_FOLDER):
                os.unlink(UPLOAD_FOLDER+file)

            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                file.save(path_to_file)
                for file in os.listdir(upload_path):

                    #Check if file is a pdf
                    if file.endswith(".pdf"):
                        pdf_path = upload_path + file


                return render_template('extract_info.html', **case_info)

        elif request.form['submit-button'] == "search":
            query = request.form.get('query')
            new_query = sanititize_input(query)
            num_res = request.form.get('wtf-value')
            # handle value error exception and return error message if query not found
            try:
                    ind = vectorizer.get_feature_names().index(new_query)
            except ValueError:
                return render_template('search_fail.html', title='Home', name=query)

            # find index in vec where query term occurs
            indices = np.where(vec.col == ind)
            a = vec.data[indices]
            b = vec.row[indices]
            list1, list2 = zip(*sorted(zip(a, b), reverse=True))
            name1 = []
            score = []
            new_list1 = []
            new_list2 = []

            if int(num_res) == 15:
                for i in range(len(list1)):
                    if list1[i] > 0:
                        new_list1.append(list1[i])
                        new_list2.append(list2[i])

                list1 = new_list1
                list2 = new_list2
                num_res = len(list1)

            # make query term bold in retrieved documents
            for num in range(len(list2[:int(num_res)])):
                name1.append(re.sub(query,'<b>{}</b>'.format(new_query), texts[list2[num]], flags=re.I))
                score.append(round(list1[num], 3))

            return render_template('query_results.html', title='result', name=zip(range(1, int(num_res)+1), name1, score))
    else:
        return render_template('search.html', title='upload_page')

@app.route('/send/<filename>')
def send_pdf(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if  __name__=="__main__":

    stop_words_dutch_file = open('../data/misc_files/stopwords_dutch.txt', 'r')
    stop_words_english_file = open('../data/misc_files/stopwords_english.txt', 'r')
    stop_words_dutch = stop_words_dutch_file.read().split('\n')
    stop_words_english = stop_words_english_file.read().split('\n')
    stop_words = stop_words_dutch + stop_words_english

    texts = []
    source_path = "../data/text_files/clean/"
    for file in os.listdir(source_path):
        with io.open(source_path + file, "r", encoding="utf-8") as infile:
            texts.append(infile.readline())
    # get dataset and retrieved grams
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words=stop_words)

    vec = coo_matrix(vectorizer.fit_transform(texts))

    app.run(debug=True)