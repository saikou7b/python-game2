import math
import random

SECRET_CHOICES = [1, 3, 5, 7, 9]
MAX_TRIES = 6


def choose_secret():
    return random.choice(SECRET_CHOICES)


def parity_clue(value):
    return "odd" if value % 2 else "even"


def detail_clue(value):
    if value == 1:
        return "The number is neither even nor composite."
    if value % 3 == 0:
        return "The number is a multiple of 3."
    return "The number is not a multiple of 3."


def update_bounds(guess, secret, low, high):
    if guess < secret:
        low = max(low, math.floor(guess) + 1)
    else:
        high = min(high, math.ceil(guess) - 1)
    return low, high


def maybe_shift_secret(secret, tries):
    if tries > 1 and random.random() < 0.2:
        choices = [x for x in SECRET_CHOICES if x != secret]
        new_secret = random.choice(choices)
        print(random.choice([
            "Something just… changed.",
            "You felt that, right?",
            "The number got bored of you.",
            "Reality adjusted slightly. Cope.",
        ]))
        return new_secret
    return secret


def temperature_hint(guess, secret, previous_diff):
    diff = abs(guess - secret)

    if previous_diff is None:
        return diff, None

    if random.random() < 0.5:
        if diff < previous_diff:
            return diff, "Colder."
        elif diff > previous_diff:
            return diff, "Warmer."
        else:
            return diff, "…sure."

    if diff < previous_diff:
        return diff, "Warmer."
    if diff > previous_diff:
        return diff, "Colder."
    return diff, "Same temperature. How are you managing that?"


def mock_guess(guess, secret):
    if guess == secret:
        return None

    responses = [
        "Bold of you to think that was correct.",
        "Interesting. Not good. But interesting.",
        "You really woke up and chose that number, huh?",
        "Statistically embarrassing.",
        "That guess had confidence. Misplaced, but confidence.",
        "I've seen worse. Not today though.",
        "You’re not even circling it anymore.",
        "You’re playing like the number insulted your family.",
    ]

    if abs(guess - secret) >= 5:
        responses.append("That’s not even in the same universe.")

    return random.choice(responses)


def pressure_line(tries):
    lines = {
        3: "You're running out of luck.",
        4: "This is where people start spiraling.",
        5: "Last chance. Make it count. Or don’t.",
    }
    return lines.get(tries)



secret = choose_secret()
tries = 0
history = []
low, high = 1, 10
previous_diff = None

print("Guess the number (1–10). Or don’t. I’m not your supervisor.")

while True:
    try:
        guess = float(input("Your guess: "))
    except ValueError:
        print(random.choice([
            "That’s not even a number. Impressive.",
            "Try again. Preferably with digits this time.",
            "I’m going to pretend you didn’t just type that.",
        ]))
        continue

    tries += 1
    history.append(guess)

    secret = maybe_shift_secret(secret, tries)

    if guess == secret:
        print(random.choice([
            "…You got it. That feels wrong.",
            "Correct. Against all odds.",
            "Well done. I hate that for me.",
        ]))
        print(f"You got it in {tries} tries.")
        break

    if tries >= MAX_TRIES:
        print(random.choice([
            "You failed. Spectacularly.",
            "That was painful to watch.",
            "Game over. The number wins.",
        ]), secret)
        break


    if guess < low or guess > high:
        print("That guess is outside the 'safe' range. Not that you care.")

    low, high = update_bounds(guess, secret, low, high)

    previous_diff, msg = temperature_hint(guess, secret, previous_diff)
    if msg:
        print(msg)

    print("Too low." if guess < secret else "Too high.")
    print(mock_guess(guess, secret))

    if random.random() < 0.2:
        fake = "even" if parity_clue(secret) == "odd" else "odd"
        print(f"The number is {fake} in parity.")
    else:
        print(f"The number is {parity_clue(secret)} in parity.")

  
    if tries % 2 == 0:
        print(detail_clue(secret))

   
    if len(history) >= 3:
        formatted = ", ".join(
            str(int(x)) if x.is_integer() else str(x) for x in history
        )
        print(f"History: {formatted}")
        if random.random() < 0.3:
            print("Seeing it written out like that isn’t helping, is it?")

   
    line = pressure_line(tries)
    if line:
        print(line)

  
    if random.random() < 0.15:
        fake_low = max(1, low - random.randint(0, 2))
        fake_high = min(10, high + random.randint(0, 2))
        print(f"Range is now {fake_low}-{fake_high}")
    else:
        print(f"Range is now {low}-{high}")