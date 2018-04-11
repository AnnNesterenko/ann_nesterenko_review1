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


class Training(object):
    def __init__(self, case, destination, model):
        self.case = case
        self.destination = destination
        self.model = model
        self.statistics = {}

    @staticmethod
    def fix(self, line):
        if self.case:
            line = line.lower()
        fixed_line = ''
        for symbol in line:
            if symbol.isalpha() or symbol == ' ':
                fixed_line += symbol
        return fixed_line.split()

    @staticmethod
    def prepare(self, model, line):
        for i in range(len(line) - 1):
            if line[i] in model.keys() and line[i + 1] in model[line[i]].keys():
                model[line[i]][line[i + 1]] += 1
            elif line[i] in model.keys() and line[i + 1] not in model[line[i]].keys():
                model[line[i]][line[i + 1]] = 1
            else:
                model[line[i]] = {}
                model[line[i]][line[i + 1]] = 1
        return model

    def make_statistics_model_if_stdin(self):
        for line in self.destination:
            sep_line = self.fix(self, line)
            self.statistics = self.prepare(self, self.statistics, sep_line)
            return

    def make_statistics_model_if_file(self):
        files = os.listdir(self.destination)
        for f in files:
            with open(os.path.join(self.destination, f)) as data:
                for line in data.readlines():
                    sep_line = self.fix(line)
                    self.statistics = self.prepare(self.statistics, sep_line)
        return

    def choose_way_and_make_statistics_model(self):
        if self.destination == "stdin":
            self.make_statistics_model_if_stdin()
        else:
            self.make_statistics_model_if_file()

    def create_file_with_statistics_model(self):
        with open(self.model, 'wb') as file:
            pickle.dump(self.statistics, file)


if __name__ == "__main__":
    stat_for_generation = Training(args.lc, args.train_file, args.model)
    stat_for_generation.choose_way_and_make_statistics_model()
    stat_for_generation.create_file_with_statistics_model()
