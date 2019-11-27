import compile_and_run
import json
import argparse
import multiprocessing
import threading
import os

class MutantTester:
    def __init__(self, mutant_lib, mutants_location, vectors):
        self.mutant_lib = self.load_lib(mutant_lib)
        self.mut_numbers = len(self.mutant_lib["mutants"])
        self.mutant_folder = mutants_location
        self.vectors = self.load_lib(vectors)['vectors']
        self.test_lib = {}
        self.list = []

    def load_lib(self, path_to_lib):
        with open(path_to_lib) as json_file:
            data = json.load(json_file)
        return data

    def test_mutant(self, mutant_number, dict):
        compiler = "gcc";
        options = []
        options.append("-lm")
        mutant = compile_and_run.CVirtualMachine(compiler, options)
        path_mutant = self.mutant_folder + \
            "Matrix_inverse_LUP_mut_{}.c".format(mutant_number)
        bool = mutant.compile(path_mutant, "mutant_{}.exe".format(mutant_number))

        if dict is None:
            dict = self.mutant_lib

        if not bool:
            return False

        for vector in self.vectors:
            res_mutant = mutant.run("mutant_{}.exe".format(mutant_number), vector[0])

            if vector[1] != res_mutant:
                dict[mutant_number]["vector"] = vector
                os.remove('mutant_{}.exe'.format(mutant_number))
                print("Found vector: {}\nKilling mutant: {}".format(vector[1], \
                    dict[mutant_number]))
                return True

        dict[mutant_number]["vector"] = None
        os.remove('mutant_{}.exe'.format(mutant_number))
        return False

    def test_mutants_subset(self, min, max, dict):
        for i in range(min, max):
            bool = self.test_mutant(i, dict)
            if not bool:
                print("No test vector found for mutant: \n{}\n".format(dict[i]))

    def test_all_mutants(self, dict):
        MutantTester.test_mutants_subset(0, self.mut_numbers, dict)

    def output_library(self, destination):
        with open(destination, 'w') as outfile:
            json.dump(self.mutant_lib, outfile, indent=4)

    def printLib(self):
        print(self.test_lib)

def main():
    parser = argparse.ArgumentParser(
        description='Test all the mutants from a file with certain vectors')
    parser.add_argument('library', help='input library')
    parser.add_argument('vectors', help='Vectors to test out')
    parser.add_argument('mutant_location', help='folder where mutated programs are contained')
    parser.add_argument('destination',  help='destination file for vectors')

    parser.add_argument('--mult', default=-1, type=int, help='Split the mutants and generate vectors side by side')
    args = parser.parse_args()
    tester = MutantTester(args.library, args.mutant_location, args.vectors)

    manager = multiprocessing.Manager()
    
    dict_managers = []

    for dict in tester.mutant_lib["mutants"]:
        dict_managers.append(manager.dict(dict))

    threads = []
    subset_size = int(tester.mut_numbers / args.mult)
    #for i in range(0, tester.mut_numbers, subset_size):
    for i in range(2):    
        endpoint = i + subset_size
        if endpoint > tester.mut_numbers:
            endpoint = tester.mut_numbers - 1
        pro = multiprocessing.Process(target=tester.test_mutants_subset, args=[20 + i, 20 + i + 1, dict_managers])
        threads.append(pro)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for i in range(len(dict_managers)):
        #print(dict_managers[i])
        tester.mutant_lib["mutants"][i] = dict_managers[i].copy()
        #print(tester.mutant_lib["mutants"][i])

    #print(tester.mutant_lib)
    tester.output_library(args.destination)


if __name__ == '__main__':
    main()
