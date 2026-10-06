"""Independent symbolic audit; requires SymPy, no measurement or fitter.

Outputs exact identities in ../docs/audit_data/symbolic_checks.json.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

x, y, omega, true_R, epsilon, shift, kappa = sp.symbols("i_d i_q omega R_true epsilon_R h kappa", nonzero=True, real=True)
pd, pq = sp.symbols("psi_d psi_q", real=True)
ud, uq = true_R*x-omega*pq, true_R*y+omega*pd
used_R = true_R+epsilon
error_d = sp.simplify((uq-used_R*y)/omega-pd)
error_q = sp.simplify((used_R*x-ud)/omega-pq)
assert error_d == -epsilon*y/omega
assert error_q == epsilon*x/omega
curl = sp.diff(error_q, x)-sp.diff(error_d, y)
t = sp.symbols("t", real=True)
wa = sp.integrate(error_d.subs({x:t, y:0}), (t, 0, x))+sp.integrate(error_q.subs(y,t), (t, 0, y))
wb = sp.integrate(error_q.subs({x:0, y:t}), (t, 0, y))+sp.integrate(error_d.subs(x,t), (t, 0, x))
delta = sp.simplify(wa-wb)
area = sp.integrate(curl, (x, 0, x), (y, 0, y))
assert sp.simplify(delta-area) == 0
assert delta == 2*epsilon*x*y/omega
assert sp.simplify(omega*(kappa*delta)/(2*kappa*x*y)-epsilon) == 0
req = used_R-omega*delta/(2*x*y)
changed_req = used_R+shift-omega*(delta+2*shift*x*y/omega)/(2*x*y)
assert sp.simplify(changed_req-req) == 0
W = sp.Rational(4,5)*x+x*x/2+sp.Rational(13,20)*y*y-x**4/50-y**4/40-sp.Rational(3,100)*x*x*y*y+x*y*y/50
gradient = sp.Matrix([sp.diff(W,x), sp.diff(W,y)])
assert sp.simplify(sp.diff(gradient[1],x)-sp.diff(gradient[0],y)) == 0
assert sp.simplify(gradient[0]-gradient[0].subs(y,-y)) == 0
assert sp.simplify(gradient[1]+gradient[1].subs(y,-y)) == 0
# Independent illustrative constant-core-loss branch, no dataset attribution.
c, ld, lq = sp.symbols("c L_d L_q", positive=True)
L, J = sp.diag(ld,lq), sp.Matrix([[0,-1],[1,0]])
terminal_jacobian = sp.simplify(L*(sp.eye(2)+c*J*L).inv())
terminal_curl = sp.simplify(terminal_jacobian[1,0]-terminal_jacobian[0,1])
assert terminal_curl == -2*c*ld*lq/(1+c*c*ld*lq)
root = Path(__file__).resolve().parents[1]/"docs"/"audit_data"
root.mkdir(parents=True, exist_ok=True)
checks = {"SymPy": sp.__version__, "flux_error_d": str(error_d), "flux_error_q": str(error_q),
          "curl": str(curl), "delta_W": str(delta), "R_eq_path": str(sp.simplify(req)),
          "arbitrary_R_invariance_difference": str(sp.simplify(changed_req-req)),
          "nonlinear_potential": str(W), "illustrative_core_loss_curl": str(terminal_curl),
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(root/"symbolic_checks.json").write_text(json.dumps(checks,indent=2)+"\n", encoding="utf-8")
print("All independent symbolic identities passed.")
