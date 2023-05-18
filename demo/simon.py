from qiskit import QuantumCircuit, execute, Aer
import numpy as np
import sympy
from scipy.linalg import null_space
from helpers import *

# s = 10...0
def oracle1(qc):
    m = qc.num_qubits
    n = m // 2

    for i in range(1, n):
        qc.cx(i, n + i)

# s = 0...01
def oracle2(qc):
    m = qc.num_qubits
    n = m // 2

    for i in range(0, n - 1):
        qc.cx(i, n + i)

# one-to-one
def oracle3(qc):
    m = qc.num_qubits
    n = m // 2

    for i in range(0, n):
        qc.cx(i, n + i)

# s = 1010...10
def oracle4(qc):
    n = qc.num_qubits // 2
    for i in range(0, n):
        if i != n-2:
            qc.cx(i, n + i)
    for i in range(0, n//2-1):
        qc.cx(n-2, n+2*i)
    return qc

def simon(oracle, qc):
    m = qc.num_qubits
    n = m // 2

    qc.h(range(n))
    oracle(qc)
    qc.h(range(n))

    qc.measure(range(n), range(n))

    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend=backend, shots=1)

    result = job.result()
    counts = result.get_counts(qc)
    res = list(counts.keys())[0][::-1]
    return list(map(int, res))

lst = []
n = 8
count = 0
qc = QuantumCircuit(2*n, n)
while True:
    y = simon(oracle4, qc)

    count += 1
    if count > 20:
        break

    if (isLinIndep(lst + [y])):
        lst.append(y)
    
if (len(lst) != n - 1):
    print('one to one')
else:
    # find s
    print(list(map(int, simonSysSolver(lst))))