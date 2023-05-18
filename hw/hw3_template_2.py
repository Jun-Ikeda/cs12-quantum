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

# TODO: finish this function
def distinguish(bell_qc):
    
    # write your code here, adding onto bell_qc given
    

    # load backend
    backend = get_backend('qasm_simulator', ibmq=False)

    # run experiment
    job = execute(bell_qc, backend=backend, shots=8192, optimization_level=3)
    job_monitor(job)

    # get results
    result = job.result()
    counts = result.get_counts(qc)

    # TODO
    return 0

if __name__ == '__main__':
    # testing code
    qc = QuantumCircuit(2, 2)

    # TODO: create Bell state
    
    print(distinguish(qc))
