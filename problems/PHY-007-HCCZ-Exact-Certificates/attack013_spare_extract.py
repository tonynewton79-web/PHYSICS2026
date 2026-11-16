#!/usr/bin/env python3
"""Non-invasive SPARE 2025 capture. Original compile/post_rewrite_compile unchanged."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np,cirq,pydot
import rewriter.compile_rewrite_graphs as spare
from replacement_lib.replace_qubit_circ import replace_qubit_circuit

def save_lowered(circuit,path,dotfile,source_commit):
    lowered=replace_qubit_circuit(circuit)
    dag=pydot.graph_from_dot_file(str(dotfile))[0]
    roots=[n for n in dag.get_nodes() if 'op=in' in str(n.get('label'))]
    width=len(roots)
    clean=sorted(int(n.get('qubits').strip('"')) for n in roots if n.get('ancilla').lower()=='true')
    gates=[]
    for op in lowered.all_operations():
        qs=[]
        for q in op.qubits:
            if not hasattr(q,'x'):raise TypeError(f'Unsupported qubit locator {q!r}')
            qs.append(int(q.x))
        U=cirq.unitary(op,default=None)
        if U is None:raise TypeError(f'Non-unitary operation emitted: {op!r}')
        U=np.asarray(U,dtype=np.complex128)
        if U.shape!=(2**len(qs),2**len(qs)):raise TypeError(f'Non-qubit operation {op!r}: {U.shape}')
        gates.append({'gate':repr(op),'qubits':qs,'real':U.real.tolist(),'imag':U.imag.tolist()})
    payload={'schema':'PHY007-SPARE-LOWERED-UNITARY-v1','source_commit':source_commit,
       'origin':'Authentic SPARE compiled circuit captured through published replace_qubit_circuit',
       'width':width,'clean':clean,'gates':gates,'prelowering_cirq_text':str(circuit),
       'dot_sha256':hashlib.sha256(dotfile.read_bytes()).hexdigest()}
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,indent=2))
    print('SPARE_CAPTURE',path,'OPERATIONS',len(gates),'WIDTH',width,'CLEAN',clean,flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--test-name',required=True)
    p.add_argument('--json-name',required=True)
    p.add_argument('--capture',required=True)
    p.add_argument('--compile-mode',default='optimized_qubit')
    p.add_argument('--runs',default=1,type=int)
    a=p.parse_args()
    source='9cbe0b09d6c99d7c6e423eeb53dd4cb4c9b81fc4'
    original=spare.post_rewrite_compile
    def hooked(circuit,qutrits,*args,**kwargs):
        save_lowered(circuit,Path(a.capture),Path(a.test_name+'.dot'),source)
        return original(circuit,qutrits,*args,**kwargs)
    spare.post_rewrite_compile=hooked
    ns=argparse.Namespace(use_lifted=False,test_name=a.test_name,json_name=a.json_name,
      compile_mode=a.compile_mode,runs=a.runs,seed=0,dimension=2,dont_final_replace=True,
      qubit_sim=False,run_sim=False,verify_en=False,loaded=False,no_rccx_lowering=False)
    spare.compile(ns,{})
if __name__=='__main__':main()
