import math
import numpy as np
import matplotlib.pyplot as plt
import time
from qiskit import QuantumCircuit, execute, BasicAer, IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library.standard_gates import HGate
import hw4

def deutsch_jozsa(oracle, n):
  qc = QuantumCircuit(n + 1, n)
  
  # |->
  qc.x(n)
  qc.h(n)

  # H^(⊗n)
  qc.h(range(n))

  # U_f
  qc = oracle(qc)

  # H^(⊗n)
  qc.h(range(n))

  # Measure
  qc.measure(range(n), range(n))
  backend = BasicAer.get_backend('qasm_simulator')
  job = execute(qc, backend = backend, shots=1)
  result = job.result()
  counts = result.get_counts(qc)
  return 1 if list(counts.keys())[0] == '0' * n else 0

if __name__ == '__main__':
  oracles_ans_lst = [
    [hw4.oracle_const_zero, 1],
    [hw4.oracle_const_one, 1],
    [hw4.oracle_xor, 0],
    [hw4.oracle_even, 0]
  ]
  all_passed = True
  for oracle_ans in oracles_ans_lst:
    oracle, ans = oracle_ans
    for i in range(1, 20):
      result = deutsch_jozsa(oracle, i) == ans
      if not result:
        print('oracle: {}, expected ={}, actual = {}'.format(oracle.__name__, ans, i))
        all_passed = False
  if all_passed:
    print('All passed!')
  