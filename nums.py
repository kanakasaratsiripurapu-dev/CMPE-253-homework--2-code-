import numpy as np
from scipy.stats import norm
np.set_printoptions(suppress=True)
print("NQ1/2")
g={'C':(72,18,140,30),'D':(50,40,90,20)}
M={}
for k,(tp,fp,tn,fn) in g.items():
    N=tp+fp+tn+fn
    M[k]=dict(N=N,sel=(tp+fp)/N,tpr=tp/(tp+fn),fpr=fp/(fp+tn),prec=tp/(tp+fp),n_sel=N,n_tpr=tp+fn,n_fpr=fp+tn,n_prec=tp+fp)
    print(k,M[k])
for m in ['sel','tpr','fpr','prec']:
    p1,p2=M['C'][m],M['D'][m]; n1,n2=M['C']['n_'+m],M['D']['n_'+m]
    se=np.sqrt(p1*(1-p1)/n1+p2*(1-p2)/n2); gap=p2-p1; z=gap/se; p=2*norm.sf(abs(z))
    print(m, round(gap,4), round(se,4), round(z,3), p, gap-1.96*se, gap+1.96*se)
print("NQ3")
for tpr,fpr in [(0.65,0.2),(0.55,0.15)]:
    r=[]
    for pi in [0.45,0.30]:
        num=pi*tpr; den=num+(1-pi)*fpr; r.append(num/den); print(pi,num,(1-pi)*fpr,den,num/den)
    print('gap',r[0]-r[1])
print("NQ4")
obs={('E','A'):90,('E','R'):160,('F','A'):70,('F','R'):130}
pg={'E':250/450,'F':200/450}; pl={'A':160/450,'R':290/450}
print(pg,pl)
for (G,L),o in obs.items():
    e=pg[G]*pl[L]*450; print(G,L,o,e,e/o)
print("NQ5")
lo,hi=0.0,1.0
for i in range(5):
    mid=(lo+hi)/2; t=1-mid**1.5
    mv='lo' if t>0.8 else 'hi'
    print(i+1,lo,hi,mid,round(t,4),mv)
    if t>0.8: lo=mid
    else: hi=mid
print('final',lo,hi,(lo+hi)/2,'exact',0.2**(2/3))
print("NQ6")
e=np.array([.15,.25,.3,.2,.1]); a=np.array([.1,.2,.28,.24,.18])
d=a-e; l=np.log(a/e); print(d, l.round(4), (d*l).round(4), (d*l).sum())
ce=np.cumsum(e); ca=np.cumsum(a); print(ce,ca,np.abs(ca-ce)); print('crit',1.36*np.sqrt(2/800))
print("NQ7")
X=np.array([[1,1],[-1,0],[0,-1]]);y=np.array([1,0,0]);w=np.zeros(2);b=0.
sig=lambda z:1/(1+np.exp(-z))
for t in range(4):
    z=X@w+b;p=sig(z);J=-np.mean(y*np.log(p)+(1-y)*np.log(1-p))
    gw=(p-y)@X/3;gb=np.mean(p-y)
    print(t,w.round(4),round(b,4),'z',z.round(4),'p',p.round(4),'J',round(J,4),'gw',gw.round(4),'gb',round(gb,4))
    w=w-gw;b=b-gb
print("NQ8")
w8=np.array([1,2]);b8=-.1;x0=np.array([.3,.2]);x=x0.copy()
for t in range(5):
    f=w8@x+b8;p=sig(f);print(t,x.round(4),round(f,4),round(p,4),round(-np.log(p),4))
    gx=(p-1)*w8; x=np.clip(x+.1*np.sign(gx),x0-.4,x0+.4)
print("NQ9")
for eps in [2,1,.5]: print(eps, np.sqrt(2*np.log(1.25e5))/eps, np.log(1.25e5), np.sqrt(2*np.log(1.25e5)))
k=1.5/10;print('k',k)
for T in [100,200,300,400,500]: print(T,T*.03,k*np.sqrt(T),T*.03/(k*np.sqrt(T)))
print("NQ10")
pi=2e-4;n=2e6
for f in [.05,.01,.005,.001]:
    ppv=pi*.9/(pi*.9+(1-pi)*f); ta=n*pi*.9; fa=n*(1-pi)*f; print(f,ppv,ta,fa,(ta+fa)*3/60)
fc=.05*.02; rc=.95*.98; print('cascade',fc,rc)
for tpr in [.9,rc]: print(tpr, pi*tpr/(pi*tpr+(1-pi)*fc))
