import argparse
import pickle
import os
from sys import stdin

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', default="stdin", dest='train_file',
                    help="Way to text file")
parser.add_argument('--lc', action='store_true', help="Check for lowercase")
parser.add_argument('--model', type=str, default='model.pickle',
                    help="Way to file with model for generation")

args = parser.parse_args()


# auxiliary functions
def fix(args, line):
    if args.lc:
        line = line.lower()
    fixed_line = ''
    for symb in line:
        if symb.isalpha() or symb == ' ':
            fixed_line += symb
    return fixed_line.split()


def prepare(model, line):
    for i in range(len(line) - 1):
        if line[i] in model.keys() and line[i + 1] in model[line[i]].keys():
            model[line[i]][line[i + 1]] += 1
        elif line[i] in model.keys() and line[i + 1] not in model[line[i]].keys():
            model[line[i]][line[i + 1]] = 1
        else:
            model[line[i]] = {}
            model[line[i]][line[i + 1]] = 1
    return model


# main functions
def create_model_if_stdin(args):
    model = {}
    for line in stdin:
        sep_line = fix(args, line)
        model = prepare(model, sep_line)
        return model


def create_model_if_file(args):
    files = os.listdir(args.train_file)
    model = {}
    for f in files:
        with open(os.path.join(args.train_file, f)) as data:
            for line in data.readlines():
                sep_line = fix(args, line)
                model = prepare(model, sep_line)
    return model


final_model = {}
if args.train_file == "stdin":
    final_model = create_model_if_stdin(args)
else:
    final_model = create_model_if_file(args)

with open(args.model, 'wb') as file:
    pickle.dump(final_model, file)
