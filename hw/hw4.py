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

# 1 a
def oracle_const_zero(arg_qc):
  qc = arg_qc.copy()
  return qc
# Since f(x) = 0, U_f|x>|z>=|x>|z>.  
# So, passing the circuit without adding any gate
# does the job.

# 1 b
def oracle_const_one(arg_qc):
  qc = arg_qc.copy()
  n = qc.num_qubits
  qc.x(n - 1)
  return qc
# f(x) = 1, U_f|x>|z>=|x>|z⊕1>.
# This oracle only needs to flip the (n-1)'th qubit.

# 1 c
def oracle_xor(arg_qc):
  qc = arg_qc.copy()
  n = qc.num_qubits
  for i in range(n - 1):
    qc.cx(i, n - 1)
  return qc
# Modulo 2 addition is associative. So, by applying
# ⊕x_i one by one to (n-1)'th qubit, z->z⊕x_1⊕...⊕x_n.
# ⊕x_i is achieved by cx where the control is the i'th qubit.

# 1 d
def oracle_even(arg_qc):
  qc = arg_qc.copy()
  n = qc.num_qubits
  qc.x(0)
  qc.cx(0, n - 1)
  qc.x(0)
  return qc
# If the 0th qubit is 0, 1 should be added to (n-1)'th qubit.
# So, first flip 0th qubit and apply cx_0,(n-1) and change 0th qubit
# back.

# 1 e
def oracle_four_n(arg_qc):
  qc = arg_qc.copy()
  n = qc.num_qubits
  qc.x(0)
  qc.x(1)
  qc.ccx(0, 1, n - 1)
  qc.x(0)
  qc.x(1)
  return qc
# If the 0th and 1st qubits are 0, 1 should be added to (n-1)'th qubit.
# So, first flip 0, 1st qubit and apply ccx_0,1,(n-1) and change them back.
# 1 is added to (n-1)'th qubit iff 0, 1th qubits are both 0.

# # test
# n = 2
# qc = QuantumCircuit(n + 1, n)
# qc.x(n)
# qc.h(n)
# qc.x(0)
# qc.x(1)
# # qc.h(range(n))
# print_results(oracle_const_zero(qc), 'statevector_simulator', n, title='1 a')
# print_results(oracle_const_one(qc), 'statevector_simulator', n, title='1 b')
# print_results(oracle_xor(qc), 'statevector_simulator', n, title='1 c')
# print_results(oracle_even(qc), 'statevector_simulator', n, title='1 d')
# print_results(oracle_four_n(qc), 'statevector_simulator', n, title='1 e')
