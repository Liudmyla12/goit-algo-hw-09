from __future__ import annotations

from typing import Dict, List


COINS: List[int] = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int, coins: List[int] = COINS) -> Dict[int, int]:
    """
    Greedy алгоритм видачі решти.
    Для кожного номіналу бере максимум монет, поки може.

    Повертає: dict {coin: count} тільки для coin, які використані.
    """
    if amount < 0:
        raise ValueError("amount must be >= 0")

    result: Dict[int, int] = {}
    remaining = amount

    for coin in sorted(coins, reverse=True):
        if remaining <= 0:
            break
        cnt = remaining // coin
        if cnt:
            result[coin] = cnt
            remaining -= coin * cnt

    return result


def find_min_coins(amount: int, coins: List[int] = COINS) -> Dict[int, int]:
    """
    DP (динамічне програмування): мінімальна кількість монет для суми amount.
    Класичний "coin change" для мінімізації кількості монет.

    Повертає: dict {coin: count} тільки для coin, які використані.
    """
    if amount < 0:
        raise ValueError("amount must be >= 0")
    if amount == 0:
        return {}

    coins = sorted(coins)
    inf = float("inf")

    # min_count[i] = мін. кількість монет для суми i
    min_count = [0] + [inf] * amount
    # last_coin[i] = яка монета остання використана для суми i
    last_coin = [-1] * (amount + 1)

    for s in range(1, amount + 1):
        for c in coins:
            if c > s:
                break
            if min_count[s - c] + 1 < min_count[s]:
                min_count[s] = min_count[s - c] + 1
                last_coin[s] = c

    if min_count[amount] == inf:
        # Для наших coins це нереально, бо є 1
        raise ValueError("No solution for given coins")

    # Відновлення відповіді
    res: Dict[int, int] = {}
    cur = amount
    while cur > 0:
        c = last_coin[cur]
        if c == -1:
            raise RuntimeError("DP reconstruction failed")
        res[c] = res.get(c, 0) + 1
        cur -= c

    # щоб красиво: за зростанням ключів (як у прикладі ДЗ)
    return dict(sorted(res.items()))


def _format(res: Dict[int, int]) -> str:
    if not res:
        return "{}"
    return "{" + ", ".join(f"{k}: {v}" for k, v in res.items()) + "}"


def main() -> None:
    tests = [0, 1, 6, 11, 31, 113, 999]
    print("COINS:", COINS)
    for amount in tests:
        g = find_coins_greedy(amount)
        dp = find_min_coins(amount)
        print(f"\nAmount = {amount}")
        print("Greedy:", _format(g))
        print("DP    :", _format(dp))


if __name__ == "__main__":
    main()
