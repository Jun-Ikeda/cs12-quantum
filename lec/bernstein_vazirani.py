from qiskit import QuantumCircuit, execute, BasicAer

# implements f_s(x) = x \cdot s
def oracle(s, qc):
    n = qc.num_qubits

    for i in range(n - 1):
        if s[i] == '1':
            qc.cx(i, n - 1)

# bernstein-vazirani algorithm
def bernstein_vazirani(oracle, qc):
    n = qc.num_qubits

    # phase qubit
    qc.x(n - 1)
    qc.h(n - 1)

    # Hadamard
    qc.h(range(n - 1))

    # apply oracle
    oracle(qc)

    # Hadamard
    qc.h(range(n - 1))

    qc.measure(range(n - 1), range(n - 1))

    print(qc)

    backend = BasicAer.get_backend('qasm_simulator')
    job = execute(qc, backend=backend, shots=8192)
    
    result = job.result()
    counts = result.get_counts(qc)

    return list(counts.keys())[0][::-1]

if __name__ == '__main__':
    n = 3
    s = '101'

    qc = QuantumCircuit(n + 1, n)

    print(bernstein_vazirani(lambda x : oracle(s, x), qc))