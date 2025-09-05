from datetime import timedelta


def calculate_streak(completions):
    if not completions:
        return 0

    streak = 1

    for i in range(1, len(completions)):
        prev = completions[i - 1]
        curr = completions[i]

        if curr == prev + timedelta(days=1):
            streak += 1
        elif curr == prev:
            continue
        else:
            streak = 1

    return streak
