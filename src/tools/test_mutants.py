import compile_and_run
import json

def main():
    compiler = "gcc";
    options = []
    options.append("-lm")
    sut = compile_and_run.CVirtualMachine(compiler, options)
    path_sut = "../sut/Matrix_inverse_LUP.c"
    sut.compile(path_sut, "sut")

    mutant = compile_and_run.CVirtualMachine(compiler, options)
    path_mutant = "../mutants/Matrix_inverse_mutant.c"
    mutant.compile(path_mutant, "mutant")

    f = open("simulation_file.json")
    data = json.load(f)

    v = data.get('vectors')
    kill_mutant = []
    
    for i in range(int(len(v) / 10)):
        new_lst = [str(j) for sub in v[i] for j in sub]     
        res_sut = sut.run("sut", new_lst)
        res_mutant = mutant.run("mutant", new_lst)

        if res_sut != res_mutant:
            kill_mutant.append(i)

    print(kill_mutant)

main()