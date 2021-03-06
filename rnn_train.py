import sys, os
from pathlib import Path
import argparse


import simpleRNN.rnn_words as rnn_words
import word2vec_gensim as word2vec
import simpleRNN.rnn_words_seq2seq as seq2seq

def train(training_file, root_path, model_name, n_hidden, min_count, learning_rate, training_iters, n_input, batch_size, to_train, use_seq2seq):
    my_file = Path(root_path + model_name + "_vocab.csv")
    # if no embedding exists for the current model name, make one
    if not my_file.is_file():
        word2vec.create_embedding(training_file=training_file,
            root_path=root_path, model_name=model_name,
            n_hidden=n_hidden, min_count=min_count)
    # use sequence to sequence if told to
    if use_seq2seq:
        seq2seq.run(learning_rate=learning_rate, training_iters=training_iters,
            n_input=n_input, batch_size=batch_size, n_hidden=n_hidden,
            path_to_model=root_path, model_name=model_name, train=to_train, training_file=training_file)
    # otherwise use the basic rnn model
    else:
        rnn_words.run(learning_rate=learning_rate, training_iters=training_iters,
            n_input=n_input, batch_size=batch_size,n_hidden=n_hidden,
            path_to_model=root_path,model_name=model_name, train=to_train, training_file=training_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="asdf wtf")
    parser.add_argument("--training-file", "-t", action="store")
    parser.add_argument("--model-name", "-m", action="store")
    parser.add_argument("--n-hidden", "-n", action="store")
    parser.add_argument("--min-count", "-c", action="store")
    parser.add_argument("--learning-rate", "-l", action="store")
    parser.add_argument("--training-iters", "-i", action="store")
    parser.add_argument("--n_input", "-p", action="store")
    parser.add_argument("--batch-size", "-b", action="store")
    parser.add_argument("--to-train", "-r", action="store_true")
    parser.add_argument("--seq2seq", "-s", action="store_true")
    parser.add_argument("--directory", "-d", action="store")


    training_file="simpleRNN/data/charles_dickens_great_expectations.txt"
    model_name="basic_model"

    n_hidden=300
    min_count=1
    learning_rate=0.001
    training_iters=10000
    n_input=6
    batch_size=10
    to_train=False
    use_seq2seq = False
    model_loc = "simpleRNN/models/basic_model1/"

    args = parser.parse_args(sys.argv[1:])
    if args.training_file:
        training_file = args.training_file
    if args.model_name:
        model_name = args.model_name
    if args.n_hidden:
        n_hidden = int(args.n_hidden)
    if args.min_count:
        min_count = int(args.min_count)
    if args.learning_rate:
        learning_rate = float(args.learning_rate)
    if args.training_iters:
        training_iters = int(args.training_iters)
    if args.n_input:
        n_input = int(args.n_input)
    if args.batch_size:
        batch_size = int(args.batch_size)
    if args.to_train:
        print("training")
        to_train = True
    if args.seq2seq:
        use_seq2seq = True
        model_loc = "simpleRNN/seq2seq_models/"
    if args.directory:
        model_loc = args.directory

    if not os.path.exists(model_loc):
        os.mkdir(model_loc)

    print("training file:\t", training_file)
    print("model name:\t", model_name)
    print("model path:\t", model_loc)
    print("n hidden:\t", n_hidden)
    print("min count:\t", min_count)
    print("learning rate:\t", learning_rate)
    print("n input:\t", n_input)
    print("batch size:\t", batch_size)
    print("training:\t", to_train)
    print("seq2seq:\t", use_seq2seq)
    if not input("confirm these params:(y/N) ") == "y":
        sys.exit(0)
    train(training_file, model_loc, model_name, n_hidden, min_count, learning_rate, training_iters, n_input, batch_size, to_train, use_seq2seq)
