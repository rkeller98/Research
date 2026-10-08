import csv
from pathlib import Path
import numpy as np
from scipy.spatial import Delaunay, cKDTree

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)


def eval_basis(name, X):
    if name == "himmelblau":
        x, y = X[:, 0], X[:, 1]
        return (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2
    if name == "rosenbrock":
        y = np.zeros(X.shape[0])
        for i in range(X.shape[1] - 1):
            y += 100.0 * (X[:, i + 1] - X[:, i] ** 2) ** 2 + (1 - X[:, i]) ** 2
        return y
    if name == "rastrigin":
        d = X.shape[1]
        return 10 * d + np.sum(X**2 - 10 * np.cos(2 * np.pi * X), axis=1)
    if name == "ackley":
        d = X.shape[1]
        a, b, c = 20.0, 0.2, 2 * np.pi
        t1 = -a * np.exp(-b * np.sqrt(np.sum(X**2, axis=1) / d))
        t2 = -np.exp(np.sum(np.cos(c * X), axis=1) / d)
        return t1 + t2 + a + np.exp(1)
    raise ValueError(name)


def domain_limits(name):
    return {
        "himmelblau": (-6.0, 6.0),
        "rosenbrock": (-3.0, 3.0),
        "rastrigin": (-5.12, 5.12),
        "ackley": (-5.0, 5.0),
    }[name]


def simplex_gradients(X, values):
    d = X.shape[1]
    tri = Delaunay(X)
    reps = []
    grads = []
    for simplex in tri.simplices:
        pts = X[simplex]
        A = np.concatenate([pts, np.ones((pts.shape[0], 1))], axis=1)
        if np.linalg.matrix_rank(A) < d + 1:
            continue
        coeff, *_ = np.linalg.lstsq(A, values[simplex], rcond=None)
        g = coeff[:d]
        if np.all(np.isfinite(g)):
            reps.append(np.mean(pts, axis=0))
            grads.append(g)
    return np.asarray(reps), np.asarray(grads)


def iso_points_for_component(P, comp_idx, M=10, max_simplices=2500):
    d = P.shape[1] - 1
    X = P[:, :d]
    v = P[:, d]
    tri = Delaunay(X)
    levels = np.linspace(np.min(v), np.max(v), M)
    pts_all = []
    simplices = tri.simplices
    if len(simplices) > max_simplices:
        idx = np.linspace(0, len(simplices) - 1, max_simplices, dtype=int)
        simplices = simplices[idx]
    for c in levels:
        for simplex in simplices:
            idx = simplex
            vals = v[idx]
            p = X[idx]
            for i in range(len(idx)):
                for j in range(i + 1, len(idx)):
                    vi, vj = vals[i], vals[j]
                    if (vi - c) * (vj - c) > 0 or vi == vj:
                        continue
                    t = (c - vi) / (vj - vi)
                    if 0 <= t <= 1:
                        pts_all.append((1 - t) * p[i] + t * p[j])
    if len(pts_all) == 0:
        return np.empty((0, d))
    return np.asarray(pts_all)


def confidence_score(reps, grads, sigma_factor=1.0):
    d = reps.shape[1]
    all_comp_scores = []
    bw = np.median(np.linalg.norm(reps[np.random.choice(len(reps), min(2000, len(reps)), replace=True)] - reps[np.random.choice(len(reps), min(2000, len(reps)), replace=True)], axis=1))
    bw = max(bw, 1e-3)

    for c in range(grads.shape[1]):
        P = np.concatenate([reps, grads[:, [c]]], axis=1)
        iso_pts = iso_points_for_component(P, c)
        if len(iso_pts) == 0:
            all_comp_scores.append(np.zeros(len(reps)))
            continue
        tree = cKDTree(iso_pts)
        dist, _ = tree.query(reps, k=min(32, len(iso_pts)))
        if dist.ndim == 1:
            dist = dist[:, None]
        s = np.mean(np.exp(-(dist**2) / (2 * bw**2)), axis=1)
        all_comp_scores.append(s)

    comp = np.stack(all_comp_scores, axis=1)
    score = np.exp(np.mean(np.log(comp + 1e-12), axis=1))
    thr = np.mean(score) + sigma_factor * np.std(score)
    pred_out = score < thr
    return score, pred_out, thr


def metrics(gt_out, pred_out):
    tp = int(np.sum(pred_out & gt_out))
    fp = int(np.sum(pred_out & ~gt_out))
    fn = int(np.sum(~pred_out & gt_out))
    tn = int(np.sum(~pred_out & ~gt_out))
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-12)
    return tp, fp, fn, tn, precision, recall, f1


def roc_pr_data(gt_out, score, n=140):
    th = np.linspace(np.min(score), np.max(score), n)
    roc = []
    pr = []
    for t in th:
        pred = score < t
        tp, fp, fn, tn, prec, rec, _ = metrics(gt_out, pred)
        tpr = tp / max(tp + fn, 1)
        fpr = fp / max(fp + tn, 1)
        roc.append((fpr, tpr))
        pr.append((rec, prec))
    return roc, pr


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def run_case(name, d, N=700, noise=0.03, out_frac=0.08, out_strength=1.4, seed=11):
    rng = np.random.default_rng(seed)
    lo, hi = domain_limits(name)
    X = lo + (hi - lo) * rng.random((N, d))
    f_clean = eval_basis(name, X)
    F = f_clean + noise * np.std(f_clean) * rng.standard_normal(N)

    n_out = max(1, int(round(out_frac * N)))
    out_idx = rng.choice(N, size=n_out, replace=False)
    jumps = out_strength * np.std(f_clean) * np.sign(rng.standard_normal(n_out)) * (1 + 0.5 * rng.random(n_out))
    F[out_idx] += jumps
    gt = np.zeros(N, dtype=bool)
    gt[out_idx] = True

    reps, grads = simplex_gradients(X, F)
    nn = cKDTree(X).query(reps, k=1)[1]
    gt_reps = gt[nn]
    score, pred, thr = confidence_score(reps, grads)

    tp, fp, fn, tn, prec, rec, f1 = metrics(gt_reps, pred)
    roc, pr = roc_pr_data(gt_reps, score)
    return {
        "name": name,
        "d": d,
        "N": N,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "threshold": float(thr),
        "score_mean": float(np.mean(score)),
        "score_std": float(np.std(score)),
        "roc": roc,
        "pr": pr,
        "reps": reps,
        "score": score,
        "pred": pred,
        "X": X,
        "gt": gt,
    }


def main():
    cases = [
        ("himmelblau", 2, 750, 11),
        ("rosenbrock", 3, 700, 12),
        ("rastrigin", 4, 700, 13),
        ("ackley", 4, 700, 14),
    ]
    rows = []
    first = None
    for name, d, N, seed in cases:
        out = run_case(name, d, N=N, seed=seed)
        rows.append([
            name,
            d,
            out["N"],
            out["tp"],
            out["fp"],
            out["fn"],
            out["tn"],
            f"{out['precision']:.4f}",
            f"{out['recall']:.4f}",
            f"{out['f1']:.4f}",
        ])
        if first is None:
            first = out

    write_csv(DATA / "benchmark_metrics.csv", ["function", "dimension", "N", "TP", "FP", "FN", "TN", "precision", "recall", "f1"], rows)
    write_csv(DATA / "roc_himmelblau.csv", ["fpr", "tpr"], first["roc"])
    write_csv(DATA / "pr_himmelblau.csv", ["recall", "precision"], first["pr"])

    reps = first["reps"]
    score = first["score"]
    pred = first["pred"]
    write_csv(DATA / "score_scatter_himmelblau.csv", ["x", "y", "score", "pred_out"], np.column_stack([reps[:, 0], reps[:, 1], score, pred.astype(int)]))

    X = first["X"]
    gt = first["gt"]
    write_csv(DATA / "ground_truth_himmelblau.csv", ["x", "y", "gt_out"], np.column_stack([X[:, 0], X[:, 1], gt.astype(int)]))


if __name__ == "__main__":
    main()
