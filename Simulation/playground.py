
from qiskit import * 
from qiskit.tools.visualization import plot_histogram
from IPython.display import display

qc = QuantumCircuit(2,1)
qc.h(0)
qc.x(0)
qc.measure(0,0)

aer_sim = Aer.get_backend('aer_simulator')
job = aer_sim.run(qc)
print(job.result().get_counts())
print(qc)
