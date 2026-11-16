#!/usr/bin/env python3
"""Print-friendly vector plot; no hand-picked colors."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
k=4
m=list(range(2,14))
plots=[
    ('Unshared, 3 clean',lambda x:x*(2*k+2),':'),
    ('Shared data-borrow, 3 clean',lambda x:2*(k-1)+4*x,'-'),
    ('Recycled prefix, 3 clean',lambda x:4*k-6+3*x,'--'),
    ('Shared with extra clean, 4 clean',lambda x:2*(k-1)+3*x,'-.'),
]
fig,ax=plt.subplots(figsize=(6.6,3.6))
for lbl,fun,style in plots:
    ax.plot(m,[fun(v) for v in m],linestyle=style,marker='.',label=lbl)
ax.set(xlabel='Number of distinct suffix terms $m$ (prefix size $k=4$)',
       ylabel='Number of CCZ gates',xlim=(1.8,13.2))
ax.grid(alpha=0.2)
ax.legend(loc='upper left',fontsize=8,frameon=False)
fig.tight_layout()
fig.savefig(p/'resource_tradeoff.pdf',bbox_inches='tight')
print('generated vector figure')