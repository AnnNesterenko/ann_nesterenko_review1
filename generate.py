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

args = parser.parse_args()


class Generating(object):
    def __init__(self, seed, model, output):
        self.seed = seed
        self.model = model
        self.output = output
        self.statistics = {}
        self.generated_sentence = ''

    def get_file_for_generation(self):
        with open(self.model, 'rb') as f:
            self.statistics = pickle.load(f)

    def start_word(self):
        if self.seed == '':
            return random.choice(list(self.statistics.keys()))
        elif args.seed not in self.statistics.keys():
            print("Ой, такого слова нет :(")
            print("Вот вам предложение с другим начальным словом:")
            return random.choice(list(self.statistics.keys()))
        else:
            return self.seed

    def weighted_random_next(self, word):
        t = 0
        for i in self.statistics[word].values():
            t += i
        random_int = random.randint(0, t)
        index = t
        list_of_keys = self.statistics[word].keys()
        for i in self.statistics[word].keys():
            index -= self.statistics[word][i]
            if index <= random_int:
                return i

    def generate_sentence(self):
        current_word = self.start_word()
        self.generated_sentence = [current_word]
        i = 1
        while i < args.length and current_word in self.statistics.keys():
            next_word = self.weighted_random_next(current_word)
            self.generated_sentence.append(next_word)
            current_word = next_word
            i += 1
        if i < args.length:
            print("Не получилось построить слово заданной длины:(")
            self.generated_sentence[0] = self.generated_sentence[0].capitalize()
        return

    def give_back_generated_sentence(self):
        if self.output == 'stdout':
            print(self.generated_sentence)
        else:
            with open(self.output, 'w') as file:
                file.write(self.generated_sentence)


if __name__ == "__main__":
    generating_sentence = Generating(args.seed, args.model, args.output)
    generating_sentence.generate_sentence()
    generating_sentence.give_back_generated_sentence()