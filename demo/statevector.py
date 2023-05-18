from qiskit import QuantumCircuit, execute, BasicAer

n = 2
qc = QuantumCircuit(n, n)

qc.h(0)
print(qc)
backend = BasicAer.get_backend('statevector_simulator')
job = execute(qc, backend = backend, shots=8192)
result = job.result()
state = result.get_statevector(qc)
print(state)