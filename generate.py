import argparse
import pickle
import random
from sys import stdout

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str,
                    help="Way to file with model for generation")
parser.add_argument('--seed', type=str, default='', help="First word")
parser.add_argument('--length', type=int,
                    help="Number of words in generated string")
parser.add_argument('--output', default='stdout', type=str,
                    help="File where result will be saved")

args, _ = parser.parse_known_args()

# open file
with open(args.model, 'rb') as f:
    _model = pickle.load(f)


def start_word(args):
    if args.seed == '':
        return (random.choice(list(_model.keys())))
    elif args.seed not in _model.keys():
        print("Ой, такого слова нет :(")
        print("Вот вам предложение с другим начальным словом:")
        return (random.choice(list(_model.keys())))
    else:
        return(args.seed)


def weighted_random_next(word):
    l = 0
    for i in _model[word].values():
        l += i
    random_int = random.randint(0, l)
    index = l
    list_of_keys = _model[word].keys()
    for i in _model[word].keys():
        index -= _model[word][i]
        if index <= random_int:
            return i


def generate_sentence(args):
    current_word = start_word(args)
    sentence = [current_word]
    i = 1
    while i < args.length and current_word in _model.keys():
        next_word = weighted_random_next(current_word)
        sentence.append(next_word)
        current_word = next_word
        i += 1
    if i < args.length:
        print("Не получилось построить слово заданной длины:(")
    sentence[0] = sentence[0].capitalize()
    return sentence


sentence = ' '.join(generate_sentence(args))
sentence += '.'
if args.output == 'stdout':
    print(sentence)
else:
    with open(args.output, 'w') as file:
        file.write(sentence)
