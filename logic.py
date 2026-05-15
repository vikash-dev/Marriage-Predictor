from datetime import datetime
import math


# -----------------------------------
# FUNCTIONS
# -----------------------------------

# Keep house between 1-12

def normalize(house):
    return ((house - 1) % 12) + 1


# Distance count including starting house
# same house = 1

def distance(source, target):

    count = 1
    current = source

    while current != target:
        current = normalize(current + 1)
        count += 1

    return count


# Venus owned houses
# same, 5th, 7th, 9th

def get_venus_houses(base):

    return {
        normalize(base),
        normalize(base + 4),
        normalize(base + 6),
        normalize(base + 8)
    }


# -----------------------------------
# MAIN CALCULATION FUNCTION
# -----------------------------------


def calculate_prediction(
    venus_house,
    jupitar_house,
    saturn_house,
    month,
    year
):

    venus_houses = get_venus_houses(venus_house)

    results = []

    for years in range(1, 101):

        # Jupitar movement
        jupitar_current = normalize(
            jupitar_house + years
        )

        # Candidate year only if jupitar
        # enters venus houses
        if jupitar_current not in venus_houses:
            continue

        # Saturn movement
        saturn_moves = math.ceil(years / 2.5)

        saturn_current = normalize(
            saturn_house + saturn_moves
        )

        target_year = year + years

        # Distances
        dv = distance(
            saturn_current,
            venus_house
        )

        dj = distance(
            saturn_current,
            jupitar_current
        )

        d7 = distance(
            saturn_current,
            7
        )

        # Elimination rules
        dangerous = [1, 3, 7, 10]

        eliminated = False
        reasons = []

        if dv in dangerous:
            eliminated = True
            reasons.append(
                f"Venus at dangerous distance {dv}"
            )

        if dj in dangerous:
            eliminated = True
            reasons.append(
                f"Jupitar at dangerous distance {dj}"
            )

        if d7 in dangerous:
            eliminated = True
            reasons.append(
                f"7th house at dangerous distance {d7}"
            )

        results.append({
            "date": f"{month}-{target_year}",
            "venus": venus_house,
            "jupitar": jupitar_current,
            "saturn": saturn_current,
            "dv": dv,
            "dj": dj,
            "d7": d7,
            "eliminated": eliminated,
            "reasons": reasons
        })

    # Filter future years
    current = datetime.now()

    future_results = []

    for r in results:

        m, y = map(int, r["date"].split("-"))

        if y > current.year or (
            y == current.year and m >= current.month
        ):
            future_results.append(r)

    # Final answer
    final_answer = None

    for r in future_results:
        if not r["eliminated"]:
            final_answer = r["date"]
            break

    return {
        "venus_houses": sorted(venus_houses),
        "future_results": future_results,
        "final_answer": final_answer
    }
