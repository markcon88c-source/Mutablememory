# organs/eix_detector.py

import math

def safe_norm(value, noise_val, base_val, eps=1e-9):
    """Normalize a metric against noise and baseline, allowing values >> 1."""
    denom = (base_val - noise_val)
    if abs(denom) < eps:
        return 0.0
    return (value - noise_val) / denom


def compute_eix(stats, baseline, noise, prev_emergence,
                alpha=1.0, beta=1.0, gamma=1.0, delta=2.0, Lam=1.0):
    """
    Compute Emergence–Intelligence Index (EIX_t) for this cycle.

    stats: dict with current cycle metrics
    baseline: rolling baseline metrics
    noise: plain-noise baseline metrics
    prev_emergence: E_{t-1} (previous cycle emergence_raw)
    alpha, beta, gamma, delta, Lam: tunable exponents/weights
    """

    # 1) Pull metrics
    W_t = stats.get("weirdness", 0.0)
    N_t = stats.get("novelty", 0.0)
    F_t = stats.get("suffix_structure", 0.0)
    D_t = stats.get("drift", 0.0)
    M_t = stats.get("mutual_info", 0.0)
    A_t = stats.get("attractor_depth", 0.0)
    H_t = stats.get("entropy", 0.0)
    E_t = stats.get("emergence_raw", 0.0)

    W_noise = noise.get("weirdness", 0.0)
    N_noise = noise.get("novelty", 0.0)
    F_noise = noise.get("suffix_structure", 0.0)
    D_noise = noise.get("drift", 0.0)
    M_noise = noise.get("mutual_info", 0.0)
    H_noise = noise.get("entropy", 0.0)
    E_noise = noise.get("emergence_raw", 0.0)

    W_base = baseline.get("weirdness", 1.0)
    N_base = baseline.get("novelty", 1.0)
    F_base = baseline.get("suffix_structure", 1.0)
    D_base = baseline.get("drift", 1.0)
    M_base = baseline.get("mutual_info", 1.0)
    H_base = baseline.get("entropy", 1.0)
    E_base = baseline.get("emergence_raw", 1.0)

    # 2) Normalize fields (can exceed 1.0)
    Wn = safe_norm(W_t, W_noise, W_base)
    Nn = safe_norm(N_t, N_noise, N_base)
    Fn = safe_norm(F_t, F_noise, F_base)
    Dn = safe_norm(D_t, D_noise, D_base)
    Mn = safe_norm(M_t, M_noise, M_base)

    # Attractor depth is already a 0–1 or 0–∞ metric
    An = A_t

    # 3) Order factor from entropy
    O_denom = (H_base - H_noise) if abs(H_base - H_noise) > 1e-9 else 1.0
    O_t = (H_base - H_t) / O_denom

    # 4) Structural Strangeness Φ_t
    Phi = (max(Wn, 0.0) ** alpha) * ((1.0 + max(An, 0.0)) ** beta) * math.exp(Lam * O_t)

    # 5) Structural Growth Ψ_t
    growth_sum = max(Nn, 0.0) + max(Fn, 0.0) + max(Dn, 0.0) + max(Mn, 0.0)
    Psi = (growth_sum ** gamma) if growth_sum > 0.0 else 0.0

    # 6) Structural Acceleration Ω_t
    if E_t <= 0.0:
        E_t = growth_sum

    X_denom = (E_base - E_noise) if abs(E_base - E_noise) > 1e-9 else 1.0
    X_t = (E_t - prev_emergence) / X_denom

    Omega = (1.0 + max(X_t, 0.0)) ** delta

    # 7) Final Emergence–Intelligence Index
    EIX = Phi * Psi * Omega

    return {
        "EIX": EIX,
        "Phi": Phi,
        "Psi": Psi,
        "Omega": Omega,
        "X": X_t,
        "order": O_t,
        "growth_sum": growth_sum,
        "normalized": {
            "W": Wn,
            "N": Nn,
            "F": Fn,
            "D": Dn,
            "M": Mn,
            "A": An,
        },
    }
