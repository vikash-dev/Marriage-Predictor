from datetime import datetime
import math

# -----------------------------------
# INPUTS
# -----------------------------------
venus_house = int(input("venus - in which house (1-12): "))
jupitar_house = int(input("jupitar - in which house (1-12): "))
saturn_house = int(input("saturn - in which house (1-12): "))

month = int(input("Which month you are born: "))
year = int(input("Which year you are born: "))

# -----------------------------------
# FUNCTIONS
# -----------------------------------
def normalize(house):
    return ((house - 1) % 12) + 1

# Distance count including the starting house
def distance(source, target):
    count = 1  # Starts at 1 to include saturn's house
    current = source

    while current != target:
        current = normalize(current + 1)
        count += 1

    return count

def get_venus_houses(base):
    return {
        normalize(base),       # same
        normalize(base + 4),   # 5th
        normalize(base + 6),   # 7th
        normalize(base + 8)    # 9th
    }

# -----------------------------------
# INITIAL
# -----------------------------------
venus_houses = get_venus_houses(venus_house)
print("\nvenus owns houses:", sorted(venus_houses))

results = []

# -----------------------------------
# MAIN LOOP
# -----------------------------------
for years in range(1, 101):

    # jupitar MOVEMENT
    jupitar_current = normalize(jupitar_house + years)

    if jupitar_current not in venus_houses:
        continue

    # saturn MOVEMENT
    saturn_moves = math.ceil(years / 2.5)
    saturn_current = normalize(saturn_house + saturn_moves)

    target_year = year + years

    # DISTANCES FROM saturn (Inclusive Counting)
    dv = distance(saturn_current, venus_house)
    dj = distance(saturn_current, jupitar_current)
    d7 = distance(saturn_current, 7)

    # ELIMINATION RULES
    # Dangerous counts updated to: 1, 3, 7, 10
    dangerous = [1, 3, 7, 10]

    eliminated = False
    reasons = []

    if dv in dangerous:
        eliminated = True
        reasons.append(f"venus at dangerous distance {dv}")

    if dj in dangerous:
        eliminated = True
        reasons.append(f"jupitar at dangerous distance {dj}")

    if d7 in dangerous:
        eliminated = True
        reasons.append(f"7th house at dangerous distance {d7}")

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

# -----------------------------------
# FILTER CURRENT/FUTURE
# -----------------------------------
current = datetime.now()
future_results = []

for r in results:
    m, y = map(int, r["date"].split("-"))
    if y > current.year or (y == current.year and m >= current.month):
        future_results.append(r)

# -----------------------------------
# OUTPUT
# -----------------------------------
print("\n------------------")
print("FINAL OUTPUT")
print("------------------")

labels = ["Post-current year", "Consecutive 1", "Consecutive 2", "Consecutive 3"]
final_answer = None

for i, r in enumerate(future_results[:4]):
    status = "ELIMINATED" if r["eliminated"] else "PASS"
    
    print(f"\n{labels[i]} : {r['date']}")
    print(f"venus House  : {r['venus']}")
    print(f"jupitar House : {r['jupitar']}")
    print(f"saturn House  : {r['saturn']}")
    print("\nDistances from saturn:")
    print(f"To venus     : {r['dv']}")
    print(f"To jupitar    : {r['dj']}")
    print(f"To 7th House  : {r['d7']}")
    print(f"\nStatus : {status}")

    for reason in r["reasons"]:
        print("Reason:", reason)

# Scan through all future records chronologically for the final answer
for r in future_results:
    if not r["eliminated"]:
        final_answer = r["date"]
        break

print("\n------------------")
if final_answer:
    print("FINAL OUTPUT:", final_answer)
else:
    print("FINAL OUTPUT: NULL")
