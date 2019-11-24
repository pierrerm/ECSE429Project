import compile_and_run
import json

class MutantTester:
    def __init__(self, mutant_lib, mutants_location, vectors):
        self.mutant_lib = self.load_lib(mutant_lib)
        self.mut_numbers = len(self.mutant_lib["mutants"])
        self.mutant_folder = mutants_location
        self.vectors = load_lib(vectors)['vectors']

    def load_lib(self, path_to_lib):
        with open(path_to_lib) as json_file:
            data = json.load(json_file)
        return data

    def test_mutant(self, mutant_number):
        compiler = "gcc";
        options = []
        options.append("-lm")
        mutant = compile_and_run.CVirtualMachine(compiler, options)
        path_mutant = self.mutant_folder +
            "Matrix_inverse_LUP_mut_{}.c".format(mutant_number)
        mutant.compile(path_mutant, "mutant_{}.exe".format(mutant_number))

        for vector in self.vectors:
            res_mutant = mutant.run("mutant", vector[0])

            if vector[1] != res_mutant:
                this.mutant_lib["mutants"][mutant_number]["vector"] = vector
                os.remove('mutant_{}.exe'.format(mutant_number))
                return true

        this.mutant_lib["mutants"][mutant_number]["vector"] = None
        os.remove('mutant_{}.exe'.format(mutant_number))
        return false

    def test_mutants_subset(self, min, max):
        for i in range(min, max):
            bool = test_mutant(i)
            if not bool:
                print("No test vector found for mutant: \n{}\n".format(self.mutant_lib["mutants"][i]))

    def test_all_mutants(self):
        test_mutants_subset(0, self.mut_numbers)

    def output_library(self, destination):
        with open(destination, 'w') as outfile:
            json.dump(self.library, outfile, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description='Test all the mutants from a file with certain vectors')
    parser.add_argument('library', help='input library')
    parser.add_argument('vectors', help='Vectors to test out')
    parser.add_argument('mutant_location', help='folder where mutated programs are contained')
    parser.add_argument('--mult', default=-1, type=int, help='Split the mutants and generate vectors side by side')
    args = parser.parse_args()
    tester = MutantTester(args.library, args.mutant_location, args.vectors)
    if args.mult == -1:
        tester.test_all_mutants()
    else:
        # subset_size = tester.mut_numbers / float(args.mult)
        # for i in range(tester.mut_number / subset_size):
        print("inshallah un jour ya multiprocessing")

    # compiler = "gcc";
    # options = []
    # options.append("-lm")
    # sut = compile_and_run.CVirtualMachine(compiler, options)
    # path_sut = "../sut/Matrix_inverse_LUP.c"
    # sut.compile(path_sut, "sut")
    #
    # mutant = compile_and_run.CVirtualMachine(compiler, options)
    # path_mutant = "../mutants/Matrix_inverse_mutant.c"
    # mutant.compile(path_mutant, "mutant")
    #
    # f = open("simulation_file.json")
    # data = json.load(f)
    #
    # v = data.get('vectors')
    # kill_mutant = []
    #
    # for i in range(int(len(v) / 10)):
    #     new_lst = [str(j) for sub in v[i] for j in sub]
    #     res_sut = sut.run("sut", new_lst)
    #     res_mutant = mutant.run("mutant", new_lst)
    #
    #     if res_sut != res_mutant:
    #         kill_mutant.append(i)
    #
    # print(kill_mutant)

main()
