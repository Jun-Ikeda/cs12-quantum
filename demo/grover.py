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
      if (round(coef.real, 3) == 0 and round(coef.imag, 3) == 0):
        continue
      bin_i = format(i, 'b').zfill(digit)
      coef = round(coef.real, 3) + round(coef.imag, 3) * 1j
      output += '{}|{}> + '.format(coef, bin_i)
    output = output[:-3]
    print(output)
    print('-' * 60)

s = 3
n = 3
qc = QuantumCircuit(n + 1, n)

def oracle(w, qc_arg):
  if not (type(w) is str):
    w = format(w, 'b').zfill(n)
  # in case s = 101, n = 3, |Ψ>=1/2^(3/2)*|->(|000>+|001>+|010>+|011>+|100>+|101>+|110>+|111>)
  qc = qc_arg.copy()

  for i in range(n):
    if w[i] == 0:
      qc.x(i)
  # |ψ> = 1/2^(3/2)*|->(|010>+|011>+|000>+|001>+|110>+|111>+|100>+|101>)
  # The component equal to s became |111>

  qc.mcx(list(range(n)), n)
  # |ψ> = 1/2^(3/2)*|->(|010>+|011>+|000>+|001>+|110>-|111>+|100>+|101>)

  for i in range(n):
    if w[i] == 0:
      qc.x(i)
  # |Ψ>=1/2^(3/2)*|->(|000>+|001>+|010>+|011>+|100>-|101>+|110>+|111>)
  return qc

qc.x(n)
qc.h(n)

qc.h(range(n))

for i in range(int(np.sqrt(2**n))):
  qc = oracle(s, qc)
  qc.h(range(n))
  qc = oracle(0, qc)
  qc.h(range(n))

print_results(qc, 'statevector_simulator', n, title='Grover')
