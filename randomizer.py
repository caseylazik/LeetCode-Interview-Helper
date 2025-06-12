import csv
import os
import random
import time

completed_probs = set()


# Read problem data
def read_problems(file_path):
    problems = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            problem = {
                'name': row['problem_name'],
                'url': row['url'],
                'difficulty': row['difficulty'],
                'topic': row['topic']
            }
            # Check if already completed in this session
            if problem['name'] not in completed_probs:
                problems.append(problem)
    return problems


# Read problem explanations
def read_explanations(file_path, probName):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['problem_name']
            if name == probName:
                print(row['explanation'])
                return


# Choose difficultt for problems
def chooseDifficulties():
    chooseDifficulty = input("Enter difficulty levels to practice (e.g., easy, medium, hard): ").lower().strip()
    difficulties = set()

    for difficulty in chooseDifficulty.split(','):
        diff = difficulty.strip()
        if diff != 'easy' and diff != 'medium' and diff != 'hard':
            return chooseDifficulties()
        difficulties.add(diff)
    return difficulties


# Check yes or no response
def checkResponse(input):
    input = input.strip().lower()
    return input == 'y' or input == 'yes'


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
                choice = int(input(f'Which problem would you like to choose? (pick a valid number between 1 and {len(probs)}): '))
                if 1 <= choice <= len(probs):
                    chosen = probs[choice - 1]
                    return chosen  # Exit the loop when a valid choice is made
                else:
                    print(f"Invalid number! Please choose a number between 1 and {len(probs)}.")
            # Error message
            except ValueError:
                print("Invalid input! Please enter a number.")


def timer1():
    chooseToTime = input('Do you want to time yourself?(y/yes)')

    if checkResponse(chooseToTime):
        input('Type anything to begin!! GLL    ')
        start = time.time()

        end = input('Type anything to finish')
        end = time.time()

        print()
        print(f'That took {((end - start) / 60).__round__(2)} minutes',
              f'or {(end - start).__round__(2)} seconds')


def timer(time_limit):
    print(f"You have {time_limit} minutes to solve this problem. Starting now!")
    start = time.time()
    while True:
        elapsed = (time.time() - start) / 60
        if elapsed >= time_limit:
            print("\nTime's up!")
            return False
        user_input = input("Press Enter when you finish (or type 'quit' to stop): ").strip().lower()
        if user_input == 'quit':
            print("Exiting early.")
            return True
        if user_input == '':
            print(f"You finished in {elapsed:.2f} minutes.")
            return True

# Main program
def main():
    # Initial

    problems_path = os.path.join("data", 'problems.csv')
    bank = read_problems(problems_path) 
    probs = bank

    print()
    print("Hello,")
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

    timer1()

    print()

    explanation = input('Do you want an explanation?(y/yes)')
    print()

    if (checkResponse(explanation)):
        explanations_path = os.path.join('data', 'explanations.csv')
        read_explanations(explanations_path, chosen['name'])
        print()

    runItBack = input('Do you want to do another problem?(y/yes)')
    if (checkResponse(runItBack)):
        main()
        return

    print()
    runDiagnostics = input('Do you want to run diagnostics? (y/yes)')
    if checkResponse(runDiagnostics):
        print("Current companies to lookout for are Amazon, Google, BlueOrigin, Meta,")

        print("Important topics:")

        # Tree Traversals
        print("- Tree Traversals:")
        print("  1. Inorder (Left-Root-Right): Visits left subtree, root, "
            "then right subtree. For BST in retrieving in sorted order.")
        print("     Example: For tree A -> B, C (left, right): Inorder = 'B A C'")
        print("  2. Preorder (Root-Left-Right): Visits root, left subtree, then right subtree.")
        print("     Example: Preorder = 'A B C'")
        print("  3. Postorder (Left-Right-Root): Visits left subtree, right subtree, then root.")
        print("     Example: Postorder = 'B C A'")

        # Dynamic Programming
        print("- Dynamic Programming Approaches:")
        print("  1. Top-Down (Memoization):")
        print("     - Solves problems recursively and stores results of subproblems.")
        print("     - Lazy computation: Computes only what is needed.")
        print("     - Example: Fibonacci using recursion with memoization.")
        print("  2. Bottom-Up (Tabulation):")
        print("     - Solves problems iteratively from smallest subproblems to largest.")
        print("     - Eager computation: Precomputes all subproblems.")
        print("     - Example: Fibonacci using a DP table and iteration.")

        # Comparison
        print("- Key Comparison:")
        print("  - Top-Down: Recursive, uses memoization, simpler but can be slower.")
        print("  - Bottom-Up: Iterative, uses tabulation, faster but less intuitive.")        


    # Potential TODOs:

    # Improve interface
    # Behavioral questions!

# Adjust problem difficulty distribution
def adjust_difficulty_distribution(problems, num_questions):
    typical_distributions = {
        1: {'easy': 1, 'medium': 0, 'hard': 0},
        2: {'easy': 1, 'medium': 1, 'hard': 0},
        3: {'easy': 1, 'medium': 1, 'hard': 1},
        4: {'easy': 1, 'medium': 2, 'hard': 1},
        5: {'easy': 2, 'medium': 2, 'hard': 1},
        6: {'easy': 2, 'medium': 3, 'hard': 1},
        7: {'easy': 2, 'medium': 4, 'hard': 1},
        8: {'easy': 2, 'medium': 4, 'hard': 2},
        9: {'easy': 3, 'medium': 4, 'hard': 2},
        10: {'easy': 3, 'medium': 5, 'hard': 2},
    }

    # Handle cases outside of 1-10 range with a default distribution
    if num_questions > 10:
        random.shuffle(problems)
        return problems[:num_questions]
    
    distribution = typical_distributions[num_questions]

    # Separate problems by difficulty
    easy_problems = [p for p in problems if p['difficulty'] == 'easy']
    medium_problems = [p for p in problems if p['difficulty'] == 'medium']
    hard_problems = [p for p in problems if p['difficulty'] == 'hard']

    # Randomly sample problems based on the distribution
    session_problems = []
    session_problems += random.sample(easy_problems, distribution['easy'])
    session_problems += random.sample(medium_problems, distribution['medium'])
    session_problems += random.sample(hard_problems, distribution['hard'])

    # Shuffle the selected problems to mix difficulties
    # random.shuffle(session_problems)

    return session_problems


# Mock interview session
def mock_interview():
    problems = read_problems('problems.csv') 
    print("\nWelcome to Mock Interview Mode!")

    while True:
        try:
            num_questions = int(input(f"How many problems would you like to attempt? (Choose an integer 1-{len(problems)}) ").strip())
            if num_questions <= 0 or num_questions > len(problems):
                print(f"Number of questions must be greater than 0 and less than {len(problems)}.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    while True:
        try:
            time_limit = float(input("Set a time limit per problem (in minutes): ").strip())
            if time_limit <= 0:
                print("Time limit must be greater than zero.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive number.")



    session_problems  = adjust_difficulty_distribution(problems, num_questions)
 

    attempted = []
    for idx, prob in enumerate(session_problems, start=1):
        print(f"\nProblem {idx}/{num_questions}: {prob['name']} ({prob['difficulty']})")
        print(f"URL: {prob['url']}")

        completed = timer(time_limit)
        attempted.append((prob['name'], completed))

        if not completed:
            print("You didn't finish this problem within the time limit.")

        print("\n--- Moving to the next problem ---")

    print("\nSession Complete! Here's how you did:")
    for idx, (name, completed) in enumerate(attempted, start=1):
        status = "Completed" if completed else "Not Completed"
        print(f"{idx}. {name} - {status}")

    review = input("\nWould you like to review explanations for any problems? (y/yes): ")
    if checkResponse(review):
        for name, _ in attempted:
            print(f"\nExplanation for {name}:")
            read_explanations('explanations.csv', name)


if __name__ == '__main__':
    print()
    print("SESSION START:")
    print()

    mode = input("Choose a mode: (1) Normal Practice (2) Mock Interview: ").strip()
    if mode == '1':
        print("\nStarting normal practice mode...")
        # Call normal practice flow (existing functionality)
        main()
        print()
        print(f"Problems Completed: {len(completed_probs)}")
    elif mode == '2':
        print("\nStarting mock interview mode...")
        mock_interview()
    else:
        print("Invalid choice. Exiting.")
