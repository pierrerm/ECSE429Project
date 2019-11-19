import argparse
import json
import os
import ntpath


class MutantInjector:
    def __init__(self, library_name, sut_name):
        self.lib_name = library_name
        self.sut_blank = self.__read_sut(os.path.abspath(sut_name))
        self.mutant_lib = self.__read_library()
        self.mutations = []

        # Get clean output names and extension to create all the extensions
        _, self.sut_extension = os.path.splitext(sut_name)
        self.sut_name = ntpath.basename(sut_name).replace(self.sut_extension, "")

    def inject_mutations(self):
        '''
        Go through all the lines of the mutants library and generate a
        mutated clone of the SUT
        '''
        for mutant in self.mutant_lib['mutants']:
            mod_list = self.sut_blank.copy()
            index = mutant['char_number'] - 1
            list = mod_list[mutant['line_number']]
            mod_list[mutant['line_number']] = list[:index] + mutant['type_mutation'] + list[index + 1:]
            self.mutations.append(mod_list)

    def output_mutations(self, destination):
        '''
        output the mutated versions of the program to the output directory
        if specified
        '''
        # Create a new directory to save all the mutants if one is not specified
        if destination:
            dest_filename = os.path.abspath(destination)
        else:
            out_dir_str = self.sut_name + self.sut_extension.replace('.', '_') + ".dir"
            try:
                os.mkdir(out_dir_str)
            except FileExistsError:
                pass
            dest_filename = os.path.abspath(out_dir_str)
        print(dest_filename)

        self.inject_mutations()

        # Output all the mutations to the directory
        for index, mutation in enumerate(self.mutations):
            filename = os.path.join(dest_filename, \
                "{}_mut_{}{}".format(self.sut_name, index, self.sut_extension))
            with open(filename, 'w') as file_writer:
                file_writer.writelines(mutation)

    def __read_library(self):
        '''
        Open the input program text file and return a simple list
        containing all the lines
        '''
        with open(self.lib_name, 'r') as file_reader:
            return json.load(file_reader)

    def __read_sut(self, filename):
        '''
        Open the software under test and return the mutant free version that
        will be used to generate mutated versions
        '''
        with open(filename, 'r') as file_reader:
            return [line for line in file_reader]


def main():
    parser = argparse.ArgumentParser(
        description='Open a mutant library and generate the mutant injected \
                    software.')
    parser.add_argument('lib_file', help='mutant library input filename')
    parser.add_argument('sut_file', help='Software Under Test filename')
    parser.add_argument('--dest', help='output destination')
    args = parser.parse_args()
    mut_gen = MutantInjector(args.lib_file, args.sut_file)
    mut_gen.output_mutations(args.dest)


if __name__ == '__main__':
    main()
