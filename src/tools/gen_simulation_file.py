# Generate a random list of matrices used to kill mutants and compute their inverse
from compile_and_run import CVirtualMachine
import json
import random

VECTOR_NUMBERS = 1000

def main():
    compiler = "gcc";
    options = []
    options.append("-lm")
    testvm = CVirtualMachine(compiler, options)
    path_sut = "../sut/Matrix_inverse_LUP.c"
    testvm.compile(path_sut, "matinv")
    simulation_vectors = {
        "vectors": []
    }

    # add the edge cases
    res = testvm.run("matinv", ['1'])
    simulation_vectors['vectors'].append((['1'], res))

    res = testvm.run("matinv", [])
    simulation_vectors['vectors'].append(([], res))

    res = testvm.run("matinv", ['0', '0', '0', '0', '0', '0', '0', '0', '0'])
    simulation_vectors['vectors'].append((['0', '0', '0', '0', '0', '0', '0', '0', '0'], res))

    # Add some random vectors to simulation file
    for i in range(VECTOR_NUMBERS - 3):
        random_vector = [str((random.random() - 0.5) * 1000)
                for n in range(random.randint(1, 5) ** 2)]
        res = testvm.run("matinv", random_vector)
        simulation_vectors['vectors'].append((random_vector, res))

    with open('simulation_file.json', 'w') as file:
        file.write(json.dumps(simulation_vectors))


if __name__ == '__main__':
    main()
