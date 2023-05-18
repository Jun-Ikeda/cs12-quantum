import math
import numpy as np
import matplotlib.pyplot as plt
import time
from qiskit import QuantumCircuit, execute, BasicAer, IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library.standard_gates import HGate

# print quantum circuit and simulation results
def print_results(arg_qc, backend_type, n, shots=8192, title=None):
  print('-' * 60)
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
    print('-' * 60)
    return
  elif (backend_type in ['qasm_simulator']):
    result = job.result()
    counts = result.get_counts(qc)
    print(counts)
    print('-' * 60)
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
    print('-' * 60)

# 1 a
n1a = 2
qc1a = QuantumCircuit(n1a, n1a)
qc1a.h(0)
qc1a.cx(0, 1)
print_results(qc1a, 'statevector_simulator', n1a, title='1 a')
# 1 b
n1b = 2
qc1b = QuantumCircuit(n1b, n1b)
qc1b.x(0)
qc1b.h(0)
qc1b.cx(0, 1)
print_results(qc1b, 'statevector_simulator', n1b, title='1 b')
# 1 c
n1c = 2
qc1c = QuantumCircuit(n1c, n1c)
qc1c.x(1)
qc1c.h(0)
qc1c.cx(0, 1)
print_results(qc1c, 'statevector_simulator', n1c, title='1 c')
# 1 d
n1d = 2
qc1d = QuantumCircuit(n1d, n1d)
qc1d.x(0)
qc1d.x(1)
qc1d.h(1)
qc1d.cx(1, 0)
print_results(qc1d, 'statevector_simulator', n1d, title='1 d')

# 2
def distinguish(bell_qc, shots=8192, accuracy=0.9):
  bell_qc.cx(0, 1)
  bell_qc.h(0)
  bell_qc.measure(range(2), range(2))
  backend = BasicAer.get_backend('qasm_simulator')
  job = execute(bell_qc, backend=backend, shots=8192, optimization_level=3)
  result = job.result()
  counts = result.get_counts(bell_qc)
  for key in counts:
    if (counts[key] > shots * accuracy):
      return int(key, 2)
  return -1

print('-' * 60)
print('2')
print('input |Φ+>, output: {}'.format(distinguish(qc1a)))
print('input |Φ->, output: {}'.format(distinguish(qc1b)))
print('input |Ψ+>, output: {}'.format(distinguish(qc1c)))
print('input |Ψ->, output: {}'.format(distinguish(qc1d)))
print('-' * 60)

# 3
def CHSH(starategy):
  n = np.random.randint(0, 4)
  if (n == 0): x, y, z = 0, 0, 0
  elif (n == 1): x, y, z = 0, 1, 1
  elif (n == 2): x, y, z = 1, 0, 1
  elif (n == 3): x, y, z = 1, 1, 0
  a, b, c = starategy(x, y, z)
  return (a + b + c) % 2 == (x + y + z) / 2
def classical_strategy(x, y, z):
  return 1, 1, 1
def quantum_strategy(x, y, z):
  qc = QuantumCircuit(3, 3)
  qc.h(0)
  qc.cx(0, 1)
  qc.cx(0, 2)
  for (i, t) in enumerate([x, y, z]):  
    if (t == 0):
      # measure in |+>, |-> basis
      qc.h(i)
    elif (t == 1):
      # measure in |i>, |-i> basis
      qc.sdg(i)
      qc.h(i)
  qc.measure(range(3), range(3))
  backend = BasicAer.get_backend('qasm_simulator')
  job = execute(qc, backend=backend, shots=1, optimization_level=3)
  result = job.result()
  counts = result.get_counts(qc)
  for key in counts:
    if (counts[key] == 1):
      a, b, c = key
      return int(a), int(b), int(c)

print('-' * 60)
print('3')
cwin, qwin = 0, 0
n = 1000
for i in range(n):
  if (CHSH(classical_strategy)):
    cwin += 1
  if (CHSH(quantum_strategy)):
    qwin += 1
print('classic strategy: {} / {}'.format(cwin, n))
print('quantum strategy: {} / {}'.format(qwin, n))
print('-' * 60)