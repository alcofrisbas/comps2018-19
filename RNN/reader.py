# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


"""Utilities for parsing text files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys
import numpy as np
import RNN
import nltk
import csv
from nltk.tokenize import word_tokenize

import tensorflow as tf

Py3 = sys.version_info[0] == 3

def gen_vocab(filename):
    print("reading words\n")
    wordlist = []
    with open("RNN/data/vocab.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["_UNK_", "_UNK_"])
        with open(filename, "r") as vocab:
            lines = vocab.readlines()
            for line in lines:
                line = line.replace("\n", "")
                text = word_tokenize(line)
                text = nltk.pos_tag(text)
                for word in text:
                    if word[0].lower() not in wordlist:
                        wordlist.append(word[0].lower())
                        writer.writerow(word)


    print("vocab written\n")

def word_to_id(word, word_dict):
    id = word_dict.get(word)
    return id if id is not None else word_dict.get("_UNK_")

def gen_id_seqs(filepath=""):

    with open(RNN.FLAGS.vocab_file, "r") as vocab_file:
        lines = []
        reader = csv.reader(vocab_file, delimiter=',')
        for line in reader:
            if line != []:
                lines.append(line[0])
        word_dict = dict([(b,a) for (a,b) in enumerate(lines)])

    with open(filepath, 'r') as raw_file:
        with open("RNN/data/" + filepath.split("/")[-1]+".ids", "w") as current_file:
            for line in raw_file.readlines():
                sent = []
                temp_sent = []
                line = line.strip()
                temp_sent = word_tokenize(line)
                for char in temp_sent:
                    sent.append(char)
                if len(sent) >= 3:
                    line = [word_to_id(word, word_dict) for word in sent]

                    current_file.write(" ".join([str(id) for id in line]) + "\n")


if __name__ == "__main__":
    gen_id_seqs()
