import numpy as np
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

# helper to return a backend for IBM Quantum Experience or Aer
def get_backend(backend_name, ibmq=False):
    if ibmq:
        return IBMQ.load_account().get_backend(backend_name)
    else:
        return Aer.get_backend(backend_name)

# number of qubits (adjust as necessary)
n = 3

# create quantum circuit
qc = QuantumCircuit(n, n)

# write your code here
qc.ry(np.pi/3, 0)
qc.h(2)
qc.cx(0, 1)
qc.cz(1, 2)
qc.measure(range(n), range(n))
print(qc)

backend = IBMQ.load_account().get_backend('ibmq_qasm_simulator')
job = execute(qc, backend = backend, shots=8192)
result = job.result()
counts = result.get_counts(qc)
print(counts)

# # load backend
# backend = get_backend('ibmq_qasm_simulator', ibmq=True)

# # run experiment
# job = execute(qc, backend=backend, shots=8192, optimization_level=3)
# job_monitor(job)

# # get results
# result = job.result()
# counts = result.get_counts(qc)

# plot results
plot_histogram(counts).show()
