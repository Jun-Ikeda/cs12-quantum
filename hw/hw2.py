import math
import numpy as np
import matplotlib.pyplot as plt
import time
from qiskit import QuantumCircuit, execute, BasicAer, IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library.standard_gates import HGate

# print quantum circuit and simulation results
def print_results(arg_qc, backend_type, n, shots=8192, title=None):
  print('-' * 100)
  qc = arg_qc.copy()
  if (backend_type in ['qasm_simulator', 'ibmq_lima']):
    qc.measure(range(n), range(n))
  if (title != None):
    print(title)
  print(qc)

  if (backend_type in ['qasm_simulator', 'statevector_simulator']):
    backend = BasicAer.get_backend(backend_type)
  elif (backend_type in ['ibmq_lima', 'ibm_nairobi']):
    backend = IBMQ.load_account().get_backend(backend_type)

  job = execute(qc, backend = backend, shots=shots)

  if (backend_type in ['ibmq_lima', 'ibm_nairobi']):
    print('{} Job ID: {}'.format(title, job.job_id()))
    print('-' * 100)
    return
  elif (backend_type in ['qasm_simulator']):
    result = job.result()
    counts = result.get_counts(qc)
    print(counts)
    print('-' * 100)
    plt.bar(counts.keys(), counts.values())
    plt.show()
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
    print('-' * 100)

# 1 c
n1 = 3
qc1 = QuantumCircuit(n1, n1)
qc1.ry(np.pi/3, 0)
qc1.h(2)
qc1.cx(0, 1)
qc1.cz(1, 2)
# 1 d
print_results(qc1, 'qasm_simulator', n1, title='1 d')
# # 1 e
# print_results(qc1, 'ibmq_lima', n1, title='1 e')

# # 2
# def qrandint(k):
#   n = math.ceil(math.log2(k))
#   while (True):
#     qc = QuantumCircuit(n, n)
#     qc.h(range(n))
#     qc.measure(range(n), range(n))
#     backend = BasicAer.get_backend('qasm_simulator')
#     job = execute(qc, backend = backend, shots=1)
#     result = job.result()
#     counts = result.get_counts(qc)
#     for key in counts.keys():
#       if (int(key, 2) < k):
#         return int(key, 2)
# results = []
# for i in range(2000):
#   results.append(qrandint(10))
# plt.hist(results, bins=10)
# plt.show()

# 3 a
n3a = 3
qc3a = QuantumCircuit(n3a, n3a)
qc3a.h(0)
qc3a.cx(0,1)
qc3a.cx(1,2)
print_results(qc3a, 'statevector_simulator', n3a, title='3 a')
# 3 b
n3b = 3
qc3b = QuantumCircuit(n3b, n3b)
qc3b.ry(2*math.atan(math.sqrt(2)), 0)
qc3b.cx(0,1)
qc3b.cx(1,2)
qc3b.x(1)
qc3b.append(HGate().control(2), [0, 2, 1])
qc3b.x(0)
qc3b.x(2)
qc3b.cx(1,2)
qc3b.x(1)
print_results(qc3b, 'statevector_simulator', n3b, title='3 b')

# # experiment
# print_results(qc3a, 'ibmq_lima', n3a, title='3 a')
# print_results(qc3b, 'ibmq_lima', n3b, title='3 b')