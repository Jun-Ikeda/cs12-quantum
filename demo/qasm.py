from qiskit import QuantumCircuit, execute, BasicAer

n = 2
qc = QuantumCircuit(n, n)

qc.h(0)
qc.measure(range(n), range(n))
print(qc)
backend = BasicAer.get_backend('qasm_simulator')
job = execute(qc, backend = backend, shots=8192)
result = job.result()
counts = result.get_counts(qc)
print(counts)

# from qiskit import QuantumCircuit, execute, IBMQ

# n = 2
# qc = QuantumCircuit(n, n)

# qc.h(0)
# qc.measure(range(n), range(n))
# print(qc)
# backend = IBMQ.load_account().get_backend('ibmq_qasm_simulator')
# job = execute(qc, backend = backend, shots=8192)
# result = job.result()
# counts = result.get_counts(qc)
# print(counts)

