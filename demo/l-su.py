from qiskit import QuantumCircuit, execute, IBMQ
from qiskit import BasicAer
# IBMQ.save_account("c782d3f857e1450cc8cb4495ea0c7ad0c4382c344fc02cd023ff713044cba930db187e664712881f012d12b43f0338120ad5a7b229eeb99065432e35f6836dac")

n = 2
qc = QuantumCircuit(n, n)

# qc.h(0)
# qc.measure(range(n), range(n))
# print(qc)
# backend = IBMQ.load_account().get_backend('ibmq_qasm_simulator')
# job = execute(qc, backend = backend, shots=8192)
# result = job.result()
# counts = result.get_counts(qc)
# print(counts)

qc.h(0)
# qc.save_statevector()
print(qc)
backend = BasicAer.get_backend('statevector_simulator')
# backend = IBMQ.load_account().get_backend('simulator_statevector')
job = execute(qc, backend = backend, shots=8192)
result = job.result()
state = result.get_statevector(qc)
print(state)

# import numpy as np
# from qiskit import QuantumCircuit, execute, IBMQ
# from qiskit.visualization import plot_bloch_multivector

# n = 2
# qc = QuantumCircuit(n, n)
# qc.ry(np.pi / 3, 0)
# backend = IBMQ.load_account().get_backend('simulator_statevector')
# job = execute(qc, backend=backend, shots=8192)
# result = job.result()
# state = result.get_statevector()
# print(state)

# import qiskit
# from qiskit import IBMQ
# from qiskit_aer import AerSimulator

# # Generate 3-qubit GHZ state
# circ = qiskit.QuantumCircuit(3)
# circ.h(0)
# circ.cx(0, 1)
# circ.cx(1, 2)
# circ.measure_all()

# # Construct an ideal simulator
# aersim = AerSimulator()

# # Perform an ideal simulation
# result_ideal = qiskit.execute(circ, aersim).result()
# counts_ideal = result_ideal.get_counts(0)
# print('Counts(ideal):', counts_ideal)
# # Counts(ideal): {'000': 493, '111': 531}

# # # Construct a noisy simulator backend from an IBMQ backend
# # # This simulator backend will be automatically configured
# # # using the device configuration and noise model 
# # provider = IBMQ.load_account()
# # backend = provider.get_backend('ibmq_athens')
# # aersim_backend = AerSimulator.from_backend(backend)

# # # Perform noisy simulation
# # result_noise = qiskit.execute(circ, aersim_backend).result()
# # counts_noise = result_noise.get_counts(0)

# # print('Counts(noise):', counts_noise)