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


"""Utilities for parsing PTB text files."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os
import re
import sys
import numpy as np

import tensorflow as tf

Py3 = sys.version_info[0] == 3

def _read_words(filename):
    with tf.gfile.GFile(filename, "r") as f:
        if Py3:
            full = []
            words = re.split('(\.)', f.read())
            for line in words:
                full.append(line.strip().replace("<unk>", "__UNK__").split())
            full = [item for sublist in full for item in sublist]
            return full

        else:
            return f.read().decode("utf-8").split()


def gen_vocab(filename):
    word_list = _read_words(filename)
    word_list = list(set(word_list))

     # We need to tell LSTM the start and the end of a sentence.
    # And to deal with input sentences with variable lengths,
    # we also need padding position as 0.
    word_list = ["_PAD_", "_BOS_", "_EOS_"] + word_list

    with open("data/vocab.txt", "w") as vocab_file:
        for word in word_list:
            vocab_file.write(word + '\n')



def gen_id_seqs(filepath="C:\\Users\Malcolm\Desktop\Classes\comps\comps2018-19\RNN"):

    def word_to_id(word, word_dict):
        id = word_dict.get(word)
        return id if id is not None else word_dict.get("_UNK_")

    with open("data/vocab.txt", "r") as vocab_file:
        lines = [line.strip() for line in vocab_file.readlines()]
        word_dict = dict([(b,a) for (a,b) in enumerate(lines)])

    with open(filepath, 'r') as raw_file:
        with open("data/" + filepath.split("/")[-1]+".ids", "w") as current_file:
            for line in raw_file.readlines():
                line = [word_to_id(word, word_dict) for word in line.strip().replace("<unk>","_UNK_").split()]
                # each sentence has the start and the end
                line_word_ids = [1] + line + [2]
                current_file.write(" ".join([str(id) for id in line_word_ids]) + "\n")


if __name__ == "__main__":
    gen_id_seqs()