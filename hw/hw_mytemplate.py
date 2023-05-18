import math
import numpy as np
import matplotlib.pyplot as plt
import time
from qiskit import QuantumCircuit, execute, BasicAer, IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library.standard_gates import HGate

# print quantum circuit and simulation results
def print_results(arg_qc, backend_type, shots=8192, title=None):
  print('-' * 60)
  qc = arg_qc.copy()
  n = qc.num_qubits
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
