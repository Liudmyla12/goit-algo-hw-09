from __future__ import annotations

import argparse
import timeit
from typing import Dict, List, Tuple

from task_1 import COINS, find_coins_greedy, find_min_coins


def bench_one(func, amount: int, number: int, repeat: int) -> float:
    """
    Повертає найкращий час (min) з repeat прогонів,
    де кожен прогін виконує func(amount) number разів.
    """
    timer = timeit.Timer(lambda: func(amount))
    results = timer.repeat(repeat=repeat, number=number)
    return min(results)


def run_bench(amounts: List[int], number: int, repeat: int) -> List[Tuple[int, float, float]]:
    rows = []
    for a in amounts:
        t_g = bench_one(find_coins_greedy, a, number=number, repeat=repeat)
        t_dp = bench_one(find_min_coins, a, number=number, repeat=repeat)
        rows.append((a, t_g, t_dp))
    return rows


def print_table(rows: List[Tuple[int, float, float]]) -> None:
    print("COINS:", COINS)
    print("\n| Amount | Greedy (s) | DP (s) | Faster |")
    print("|------:|-----------:|-------:|:------:|")
    for a, tg, tdp in rows:
        faster = "Greedy" if tg < tdp else "DP"
        print(f"| {a:6d} | {tg:10.6f} | {tdp:7.6f} | {faster:^6} |")


def main() -> None:
    parser = argparse.ArgumentParser(description="HW09: Greedy vs DP coin change benchmark")
    parser.add_argument(
        "--amounts",
        type=str,
        default="113,1000,5000,10000,50000",
        help="Comma-separated amounts to test (default: 113,1000,5000,10000,50000)",
    )
    parser.add_argument("--number", type=int, default=200, help="Calls per repeat (default: 200)")
    parser.add_argument("--repeat", type=int, default=5, help="Repeat count (default: 5)")
    args = parser.parse_args()

    amounts = [int(x.strip()) for x in args.amounts.split(",") if x.strip()]
    rows = run_bench(amounts, number=args.number, repeat=args.repeat)

    print("\n=== Performance comparison (timeit) ===")
    print_table(rows)

    # Короткий висновок
    print("\nNotes:")
    print("- Greedy має приблизно O(k) (k = кількість номіналів), дуже швидкий.")
    print("- DP має O(amount * k), тому для великих сум росте помітно повільніше.")
    print("- DP гарантує мінімальну кількість монет для будь-яких наборів монет.")
    print("- Для набору [50,25,10,5,2,1] greedy зазвичай теж дає оптимум, бо система 'канонічна'.")


if __name__ == "__main__":
    main()

