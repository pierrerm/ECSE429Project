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
        # subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=False)
        subprocess.run([self.compiler, source, "-o", target_name] + self.options)

    def run(self, target_name, input):
        cmd = "./{} {}".format(target_name, input)
        subprocess.call(cmd, stdin=None, stdout=None, stderr=None, shell=False)
        # subprocess.run(cmd)


def main():
    compiler = "gcc";
    options = []
    options.append("-lm")
    testvm = CVirtualMachine(compiler, options)
    path_sut = "../sut/Matrix_inverse_LUP.c"
    testvm.compile(path_sut, "matinv")
    testvm.run("matinv", "1 2 3 4 5 6 7 8 9")


if __name__ == '__main__':
    main()
