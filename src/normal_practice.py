from pathlib import Path
from utilities import checkResponse, read_explanations, read_problems
import random
import time

completed_probs = set()


# Choose difficultt for problems
def chooseDifficulties():
    chooseDifficulty = input("Enter difficulty levels to practice (any, "
                             "easy, medium, hard): ").lower().strip()
    difficulties = set()

    for difficulty in chooseDifficulty.split(','):
        diff = difficulty.strip()
        if diff == 'any':
            return {"easy", "medium", "hard"}
        if diff != 'easy' and diff != 'medium' and diff != 'hard':
            return chooseDifficulties()
        difficulties.add(diff)
    return difficulties


# Find problems of chosen topic
def chooseTopic(probs):
    chooseTopic = input("\nWould you like to pick "
                        "a topic to practice? (y/yes): ")
    print()

    if not checkResponse(chooseTopic):
        return probs

    topics = set()
    for prob in probs:
        top = prob['topic']
        topics.add(top)
    topics = sorted(topics)  # Alphabetical

    print('Here are the following topics:')
    num = 1
    for topic in topics:
        print(f" {num}. {topic}")
        num += 1

    topic = input("\nEnter a topic you want to practice: ").lower().strip()

    temp = []

    for prob in probs:
        if prob['topic'] == topic:
            temp.append(prob)

    while not temp:
        print("Invalid topic chosen!")
        print("Choose a valid topic or type q to randomly select!")

        topic = input("\nEnter a topic you want"
                      "to practice (q to escape): ").lower().strip()
        if topic == 'q':
            return probs
        if topic in topics:
            for prob in probs:
                if prob['topic'] == topic:
                    temp.append(prob)
            return temp

    return temp


# Handle whether a random problem is chosen or not
def chooseRandom(probs):
    chooseRandom = input("\nWould you like to random pick? (y/yes): ")

    if checkResponse(chooseRandom):
        chosen = random.choice(probs)
        print(chosen)
        return chosen
    else:
        count = 1
        for prob in probs:
            print(f" {count}. {prob['name'], prob['url']}")
            count += 1
        print()
        # Up to user
        while True:
            # If NAN value is chosen we throw error
            try:
                choice = int(input(f'Which problem would you like '
                                   f'to choose? (pick a valid number between '
                                   f'1 and {len(probs)}): '))
                if 1 <= choice <= len(probs):
                    chosen = probs[choice - 1]
                    return chosen  # Exit the loop when a valid choice is made
                else:
                    print(f"Invalid number! Please choose a number between 1 "
                          f"and {len(probs)}.")
            # Error message
            except ValueError:
                print("Invalid input! Please enter a number.")


# Determine and act on whether the current problem is timed.
def timer():
    chooseToTime = input('Do you want to time yourself?(y/yes)')

    if checkResponse(chooseToTime):
        input('Type anything to begin!! GLL    ')
        start = time.time()

        end = input('Type anything to finish')
        end = time.time()

        print()
        print(f'That took {((end - start) / 60).__round__(2)} minutes',
              f'or {(end - start).__round__(2)} seconds')


# Main function for problem choosing
def problem_chooser():
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Handles different os
    problems_path = BASE_DIR / "data" / "problems.csv"

    probs = read_problems(problems_path, completed_probs)

    # Leetcode problems already completed
    completed = len(completed_probs)
    if completed:
        print(
              f"You have {len(probs)} Leetcode problems to choose from "
              f"({completed} completed this session)"
            )
    else:
        print(f"You have {len(probs)} Leetcode problems to choose from...")

    probs = chooseTopic(probs)

    difficulties = chooseDifficulties()

    temp = []
    for prob in probs:
        diff = prob['difficulty']
        if diff in difficulties:
            temp.append(prob)

    probs = temp

    length = len(probs)

    # No problems are valid
    if length == 0:
        print('Sorry no problems available for the given difficulty and topic')
        return
    # We have more than one problem so ask if you want random
    elif length > 1:
        chosen = chooseRandom(probs)
    # Only one problem so don't ask if want random
    else:
        print("Here's the only problem!")
        print(f"{probs[0]['name'], probs[0]['url']}")
        chosen = probs[0]
    completed_probs.add(chosen['name'])

    print()

    timer()

    print()

    explanation = input('Do you want an explanation?(y/yes)')
    print()

    if (checkResponse(explanation)):
        read_explanations(chosen['name'])
        print()

    runItBack = input('Do you want to do another problem?(y/yes)')
    if (checkResponse(runItBack)):
        problem_chooser()
        return
    else:
        print(f"Problems Completed: {len(completed_probs)}")

    print()
    runDiagnostics = input('Do you want to run diagnostics? (y/yes)')
    if checkResponse(runDiagnostics):
        print("Current companies to lookout for are Amazon, Google, "
              "BlueOrigin, Meta,")

        print("Important topics:")

        # Tree Traversals
        print("- Tree Traversals:")
        print("  1. Inorder (Left-Root-Right): Visits left subtree, root, "
              "then right subtree. For BST in retrieving in sorted order.")
        print("     Example: For tree A -> B, C (left, right): Inorder = "
              "'B A C'")
        print("  2. Preorder (Root-Left-Right): Visits root, left subtree, "
              "then right subtree.")
        print("     Example: Preorder = 'A B C'")
        print("  3. Postorder (Left-Right-Root): Visits left subtree, right "
              "subtree, then root.")
        print("     Example: Postorder = 'B C A'")

        # Dynamic Programming
        print("- Dynamic Programming Approaches:")
        print("  1. Top-Down (Memoization):")
        print("     - Solves problems recursively and stores results of "
              "subproblems.")
        print("     - Lazy computation: Computes only what is needed.")
        print("     - Example: Fibonacci using recursion with memoization.")
        print("  2. Bottom-Up (Tabulation):")
        print("     - Solves problems iteratively from smallest subproblems "
              "to largest.")
        print("     - Eager computation: Precomputes all subproblems.")
        print("     - Example: Fibonacci using a DP table and iteration.")

        # Comparison
        print("- Key Comparison:")
        print("  - Top-Down: Recursive, uses memoization, simpler but can be "
              "slower.")
        print("  - Bottom-Up: Iterative, uses tabulation, faster but less "
              "intuitive.")
