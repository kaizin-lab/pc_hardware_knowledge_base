'''
Skill 4: evaluate_marginal_value
Приоритет №4 — предотвращение переплат за бренд.

LLM не умеют делить и считать проценты. Этот навык реализует
правило AR-03: MV = ΔPerf% / ΔPrice%.

Verdict:
- MV ≥ 1.0 → EXCELLENT (прирост быстрее цены)
- 0.5 ≤ MV < 1.0 → ACCEPTABLE
- MV < 0.5 → REJECT (переплата не оправдана)
'''

import json, sys


def evaluate(base_price: float, base_score: float,
             candidate_price: float, candidate_score: float) -> dict:
    price_delta_pct = ((candidate_price - base_price) / base_price) * 100
    perf_delta_pct = ((candidate_score - base_score) / base_score) * 100

    if price_delta_pct == 0:
        mv = float('inf') if perf_delta_pct > 0 else 0.0
    else:
        mv = perf_delta_pct / price_delta_pct

    if mv >= 1.0:
        verdict = "EXCELLENT"
    elif mv >= 0.5:
        verdict = "ACCEPTABLE"
    else:
        verdict = "REJECT"

    return {
        "base": {"price": base_price, "score": base_score},
        "candidate": {"price": candidate_price, "score": candidate_score},
        "price_delta_pct": round(price_delta_pct, 1),
        "perf_delta_pct": round(perf_delta_pct, 1),
        "marginal_value": round(mv, 2) if mv != float('inf') else "∞",
        "verdict": verdict,
        "interpretation": {
            "EXCELLENT": "Прирост производительности опережает рост цены. Покупка рациональна.",
            "ACCEPTABLE": "Прирост сравним с ростом цены. Допустимо, но не обязательно.",
            "REJECT": "Переплата не оправдана. Базовый вариант эффективнее.",
        }[verdict],
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        data = json.load(sys.stdin)
    else:
        data = json.loads(sys.argv[1])
    result = evaluate(**data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
