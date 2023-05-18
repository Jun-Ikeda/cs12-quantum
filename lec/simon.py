from qiskit import QuantumCircuit, execute, BasicAer
import numpy as np
from numpy.linalg import solve
import sympy
from scipy.linalg import null_space
import math
import matplotlib.pyplot as plt
import time
from scipy import optimize
from helpers import *
import galois


def is_lin_independent(lst):
    A = galois.GF2(lst)
    rref = A.row_reduce(len(lst[0]))
    return np.linalg.matrix_rank(rref) == len(lst)

def print_results(arg_qc, backend_type, n, shots=8192, title=None):
#   print('-' * 60)
  qc = arg_qc.copy()
  if (backend_type in ['qasm_simulator', 'ibmq_lima']):
    qc.measure(range(n), range(n))
#   if (title != None):
#     print(title)
#   print(qc)

  if (backend_type in ['qasm_simulator', 'statevector_simulator']):
    backend = BasicAer.get_backend(backend_type)
  elif (backend_type in ['ibmq_lima', 'ibm_nairobi']):
    backend = IBMQ.load_account().get_backend(backend_type)

  job = execute(qc, backend = backend, shots=shots)

  if (backend_type in ['ibmq_lima', 'ibm_nairobi']):
    print('{} Job ID: {}'.format(title, job.job_id()))
    print('-' * 60)
    return
  elif (backend_type in ['qasm_simulator']):
    result = job.result()
    counts = result.get_counts(qc)
    print(counts)
    # print('-' * 60)
    # plt.bar(counts.keys(), counts.values())
    # plt.show()
  elif (backend_type in ['statevector_simulator']):
    result = job.result()
    state = result.get_statevector(qc)
    output = '|Ψ> = '
    digit = math.ceil(math.log2(len(state)))
    for i, coef in enumerate(state):
      bin_i = format(i, 'b').zfill(digit)
      coef = round(coef.real, 3) + round(coef.imag, 3) * 1j
      output += '{}|{}> + '.format(coef, bin_i)
    output = output[:-3]
    print(output)
    print('-' * 60)

# s = 100...0
def oracle1(qc_arg):
    qc = qc_arg.copy()
    n = qc.num_qubits // 2
    for i in range(1, n):
        qc.cx(i, n + i)
    return qc

# s = 000...1
def oracle2(qc_arg):
    qc = qc_arg.copy()
    n = qc.num_qubits // 2
    for i in range(0, n - 1):
        qc.cx(i, n + i)
    return qc

def dot_mod2(x, y):
    if not (type(x) is str):
        x = str(x)
    if not (type(y) is str):
        y = str(y)
    if (len(x) != len(y)):
        raise Exception("two arguments have to have the same number of digits")
    result = 0
    for i in range(len(x)):
        xi = int(x[i])
        yi = int(y[i])
        if xi != 0 and xi != 1:
            raise Exception("The arguments have to only have 0 or 1 in each digit")
        if yi != 0 and yi != 1:
            raise Exception("The arguments have to only have 0 or 1 in each digit")
        result += (xi * yi)
    result %= 2
    return result

def add_mod2(x, y):
    if not (type(x) is str):
        x = str(x)
    if not (type(y) is str):
        y = str(y)
    if (len(x) != len(y)):
        raise Exception("two arguments have to have the same number of digits")
    result = ""
    for i in range(len(x)):
        xi = int(x[i])
        yi = int(y[i])
        if xi != 0 and xi != 1:
            raise Exception("The arguments have to only have 0 or 1 in each digit")
        if yi != 0 and yi != 1:
            raise Exception("The arguments have to only have 0 or 1 in each digit")
        n = (xi + yi) % 2
        result  = str(n) + result
    return int(result)

# one-to-one
def oracle3(qc_arg):
    qc = qc_arg.copy()
    n = qc.num_qubits // 2
    for i in range(0, n):
        qc.cx(i, n + i)
    return qc

# one-to-one <- this is not one-to-one, but constant, all-to-one
def oracle4(qc_arg):
    qc = qc_arg.copy()
    n = qc.num_qubits // 2
    for i in range(n):
        qc.z(i)
    return qc

# s = 0101...01
def oracle5(qc_arg):
    qc = qc_arg.copy()
    n = qc.num_qubits // 2
    for i in range(0, n):
        if i != n-2:
            qc.cx(i, n + i)
    for i in range(0, n//2-1):
        qc.cx(n-2, n+2*i)
    return qc

def simon(oracle, qc_arg):
    qc = qc_arg.copy()
    n = qc.num_qubits // 2

    # simon's algorithm
    qc.h(range(n))
    qc = oracle(qc)
    qc.h(range(n))

    qc.measure(range(n), range(n))

    backend = BasicAer.get_backend('qasm_simulator')
    job = execute(qc, backend=backend, shots=1)
    
    result = job.result()
    counts = result.get_counts(qc)
    res = list(counts.keys())[0]
    return list(map(int, res))

# simon test
n = 10
qc = QuantumCircuit(n * 2, n)
lst = []
count = 0
for i in range(2*n):
    count += 1
    v = simon(oracle5, qc)
    if (is_lin_independent(lst + [v])):
        lst.append(v)

print(np.array(lst))
A = galois.GF2(lst)
sols = A.null_space()
print(sols)

