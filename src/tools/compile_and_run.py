# Script providing functions to compile and run C programs from a python script
# It is iportant that the input and output of thos scripts can be specified
import subprocess
import os

class CVirtualMachine:
    '''
    Class that takes a certain compiler and provides methods to compile and run
    a c program
    '''
    def __init__(self, compiler, options):
        self.compiler = compiler
        self.options = options
        self.compiler_skeleton = "{} {} -o {}"

    def compile(self, source, target_name):
        for option in self.options:
            self.compiler_skeleton += " {}".format(option)
        cmd = self.compiler_skeleton.format(self.compiler, source, target_name)
        #print("Running command {}".format(cmd))
        subprocess.run([self.compiler, source, "-o", target_name] + self.options)

    def run(self, target_name, input):
        cmd = "./{} {}".format(target_name, input)
        #print("Running command {}".format(cmd))
        result = subprocess.run(['./{}'.format(target_name)] + input, encoding='utf8', stdout=subprocess.PIPE)
        result = self.__parser(result.stdout)
        return result

    def __parser(self, input):
        lines = input.split("\n")
        floats = lines[-1].split(" ")
        matrix = []
        for fl in floats:
            fll = 0.0;
            try:
                fll = float(fl)
            except ValueError:
                continue
            matrix.append(fll)
        return matrix


def main():
    compiler = "gcc";
    options = []
    options.append("-lm")
    testvm = CVirtualMachine(compiler, options)
    path_sut = "../sut/Matrix_inverse_LUP.c"
    testvm.compile(path_sut, "matinv")
    res = testvm.run("matinv", ['2', '6', '7', '3', '12', '10', '11', '13', '14', '5', '15', '8', '16', '4', '9', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26'])
    print(res)


if __name__ == '__main__':
    main()
