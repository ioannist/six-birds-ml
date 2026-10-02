"""Fixed, train-only-standardized categorical readers for r11 audits."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


LINEAR_SETTINGS = {"standardization": "training_mean_and_population_scale",
                   "estimator": "torch_multinomial_logistic",
                   "C": 10.0, "class_weight": "balanced",
                   "tol": 1e-5, "max_iter": 5000,
                   "solver": "LBFGS_strong_wolfe", "fit_device": "cpu",
                   "fit_threads": 1}
MLP_SETTINGS = {"width": 64, "updates": 100, "learning_rate": .03,
                "fit_device": "audit_device"}


def standardize(train: torch.Tensor, heldout: torch.Tensor):
    mean = train.mean(0)
    scale = train.std(0, unbiased=False)
    scale = torch.where(scale == 0, torch.ones_like(scale), scale)
    return (train - mean) / scale, (heldout - mean) / scale, mean, scale


def fit_reader(train_x: torch.Tensor, train_y: torch.Tensor,
               heldout_x: torch.Tensor, heldout_y: torch.Tensor, *,
               family: str, seed: int, max_iter: int = 5000) -> dict:
    """Fit on training boards only; return predictions and convergence evidence."""
    device = train_x.device
    x, z, _, _ = standardize(train_x.float(), heldout_x.float())
    y = train_y.long()
    test = heldout_y.long()
    classes = torch.unique(y, sorted=True)
    k = len(classes)
    if k < 2:
        raise ValueError("probe training has fewer than two classes")
    labels = torch.searchsorted(classes, y.contiguous())
    counts = torch.bincount(labels, minlength=k).float()
    balanced = len(y) / (k * counts[labels])
    if family == "linear":
        # CUDA vector dot is unavailable on the study host. Standardization
        # remains on the audit device; only this fit and its scoring use CPU.
        torch.set_num_threads(1)
        x, z = x.cpu(), z.cpu()
        labels, balanced = labels.cpu(), balanced.cpu()
        classes, test = classes.cpu(), test.cpu()
        fit_device = torch.device("cpu")
        # sklearn's multinomial C=10 objective is weighted mean CE plus
        # ||W||²/(2*C*sum(sample_weight)); intercept is unpenalized.
        weight = nn.Parameter(torch.zeros((k, x.shape[1]), device=fit_device))
        bias = nn.Parameter(torch.zeros(k, device=fit_device))
        optimizer = torch.optim.LBFGS((weight, bias), lr=1.0,
                                       max_iter=max_iter, tolerance_grad=1e-5,
                                       tolerance_change=1e-9,
                                       line_search_fn="strong_wolfe")
        calls = 0

        def closure():
            nonlocal calls
            optimizer.zero_grad(set_to_none=True)
            logits = F.linear(x, weight, bias)
            loss = (F.cross_entropy(logits, labels, reduction="none") * balanced).sum()
            loss = loss / balanced.sum() + weight.square().sum() / (
                2 * 10.0 * balanced.sum())
            loss.backward()
            calls += 1
            return loss

        optimizer.step(closure)
        with torch.no_grad():
            gradient = max(float(weight.grad.abs().max()), float(bias.grad.abs().max()))
            steps = int(optimizer.state[weight]["n_iter"])
            # Like the registered sklearn fit, accept an optimizer stop by
            # either gradient or objective change before the iteration limit.
            converged = steps < max_iter
            logits = F.linear(z, weight, bias)
    elif family == "mlp64":
        fit_device = device
        with torch.random.fork_rng(devices=[device] if device.type == "cuda" else []):
            torch.manual_seed(seed)
            reader = nn.Sequential(nn.Linear(x.shape[1], 64), nn.ReLU(),
                                   nn.Linear(64, k)).to(device)
        optimizer = torch.optim.Adam(reader.parameters(), lr=.03)
        for _ in range(100):
            optimizer.zero_grad(set_to_none=True)
            F.cross_entropy(reader(x), labels).backward()
            optimizer.step()
        with torch.no_grad():
            logits = reader(z)
        steps, calls, converged, gradient = 100, 100, None, None
    else:
        raise ValueError("probe family differs")
    prediction = classes[logits.argmax(-1)]
    correct = int((prediction == test).sum())
    return {"accuracy": correct / len(test), "correct": correct, "total": len(test),
            "predictions": prediction.cpu().tolist(), "n_iter": [steps],
            "closure_calls": calls, "converged": converged,
            "fit_device": fit_device.type, "score_device": logits.device.type,
            "fit_threads": torch.get_num_threads(),
            "convergence_warnings": ([] if converged is not False else [
                f"gradient={gradient:.6g}; iterations={steps}"]),
            "cross_entropy_nats": float(F.cross_entropy(
                logits, torch.searchsorted(classes, test.contiguous())).detach())}
