import argparse
import json
import os
import ntpath


MUTANT_LIST = ['+', '-', '/', '*']


class MutantLibrary:
    def __init__(self, filename):
        self.filename = filename
        self.lines = self.__open_file()
        self.mutant_counter = {
            '+': 0,
            '-': 0,
            '/': 0,
            '*': 0
        }
        self.library = {
            'counter': self.mutant_counter,
            'mutants': []
        }
        self.mutation_id = 0

    def register_mutants(self):
        '''
        Go through all the lines of the input program file an register
        each necessary mutants
        '''
        for line_index, line in enumerate(self.lines):
            for char_index, char in enumerate(line):
                if char in MUTANT_LIST:
                    self.__create_mutant_entry(
                        char, line_index, char_index)

    def output_library(self, destination):
        '''
        output the library to a new file
        '''
        if not destination:
            destination = os.path.abspath('./mut_lib_'
                + ntpath.basename(self.filename))
        with open(destination, 'w') as outfile:
            json.dump(self.library, outfile, indent=4)

    def __open_file(self):
        '''
        Open the input program text file and return a simple list
        containing all the lines
        '''
        with open(self.filename, 'r') as file_reader:
            return [line for line in file_reader]

    def __create_mutant_entry(self, original_op, line_num, char_num):
        '''
        Create an actual entry for mutants based on the original
        operation and the line number
        '''
        temp_mut_list = MUTANT_LIST.copy()
        temp_mut_list.remove(original_op)
        for mutation in temp_mut_list:
            self.library['mutants'].append({
                'mutation_id': self.mutation_id,
                'original_op': original_op,
                'line_number': line_num,
                'char_number': char_num + 1,
                'type_mutation': mutation
            })
            self.library['counter'][mutation] += 1
            self.mutation_id += 1


def main():
    parser = argparse.ArgumentParser(
        description='Create a library of mutants for any input program')
    parser.add_argument('filename', help='input filename')
    parser.add_argument('--dest', help='output destination')
    args = parser.parse_args()
    mut_lib = MutantLibrary(os.path.abspath(args.filename))
    mut_lib.register_mutants()
    mut_lib.output_library(args.dest)


if __name__ == '__main__':
    main()
