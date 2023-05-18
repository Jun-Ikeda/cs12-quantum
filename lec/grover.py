from qiskit import QuantumCircuit, execute, BasicAer
from qiskit.circuit.library import MCXGate
import numpy as np

# helper to convert integer into binary (little endian notation)
def to_binary(n, num_bits):
    return list(reversed([int((n & (2**i)) > 0) for i in range(num_bits)]))[::-1]

# marks n, i.e. f(n) = 1
def oracle(n, qc):
    num_qubits = qc.num_qubits
    binary = to_binary(n, num_qubits - 1)

    # flip any 0s in bitstring
    for i in range(num_qubits - 1):
        if not binary[i]:
            qc.x(i)
    
    # controlled on this number, flip the phase qubit
    qc.append(MCXGate(num_qubits - 1), list(range(num_qubits)))

    # unflip any 0s in bitstring
    for i in range(num_qubits - 1):
        if not binary[i]:
            qc.x(i)

# grover's algorithm
def grover(m, oracle, qc):
    n = qc.num_qubits
    num_iters = int(np.sqrt(2**(n - 1)))

    # phase qubit
    qc.x(n - 1)

    # Hadamards
    qc.h(range(n))

    for i in range(num_iters):
        # oracle query
        oracle(m, qc)
        
        # diffusion
        qc.h(range(n - 1))
        oracle(0, qc)
        qc.h(range(n - 1))
    
    qc.measure(range(n - 1), range(n - 1))

    backend = BasicAer.get_backend('qasm_simulator')
    job = execute(qc, backend=backend, shots=8192)
    result = job.result()
    counts = result.get_counts(qc)
    
    # take most frequently occurring bitstring as answer
    res = max(counts, key=counts.get)
    return int(res, base=2)

if __name__ == '__main__':
    n = 8
    m = 212
    qc = QuantumCircuit(n + 1, n)

    print(grover(m, oracle, qc))