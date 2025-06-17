import csv
from pathlib import Path
import random
import time
from utilities import read_explanations, checkResponse, get_input_with_timeout


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


# Function to determine whether a problem is completed during time limit
def timer(time_limit):
    start = time.time()
    print(f"You have {time_limit} minutes to solve "
          f"this problem. Starting now!")

    finished = get_input_with_timeout("Type something or press enter "
                                      "to mark finished. Type "
                                      "quit to skip: ", 60 * time_limit)

    if finished == 'quit':
        return False
    if finished or finished == '':
        end = time.time()
        print(f"That took you {(int)(end-start).__round__(3)} second "
              f"({((int)(end-start)/60).__round__(3)} minutes)")
        return True
    return False


def behavioral_questions():
    print("We are now going to move to some behavioral questions. \n")

    num_questions = random.randint(2, 4)
     
    problems = []
    with open(Path(__file__).resolve().parent.parent / "data" / "behavioral.csv",
              newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            problem = {
                'question': row['question'],
                'guideline': row['guideline'],
            }
            
            problems.append(problem)
    problems = random.sample(problems, num_questions)
    for i in range(num_questions):
        print(f"Question {i+1}: {problems[i]['question']}")
        print(f"Guideline: {problems[i]['guideline']}\n")
        print("\n")


# Mock interview session
def mock_interview(problems):
    print("\nWelcome to Mock Interview Mode!")

    while True:
        try:
            num_prob = int(input(f"How many problems would you like to "
                                 f"attempt? (Choose an integer "
                                 f"1-{len(problems)}) ").strip())
            if num_prob <= 0 or num_prob > len(problems):
                print(f"Number of questions must be greater than 0 and "
                      f"less than {len(problems)}.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    while True:
        try:
            time_limit = float(input("Set a time limit per problem "
                                     "(in minutes): ").strip())
            if time_limit <= 0:
                print("Time limit must be greater than zero.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    session_problems = adjust_difficulty_distribution(problems, num_prob)

    attempted = []
    for idx, prob in enumerate(session_problems, start=1):
        print(f"\nProblem {idx}/{num_prob}: {prob['name']} "
              f"({prob['difficulty']})")
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

    review = input("\nWould you like to review explanations for any "
                   "problems? (y/yes): ")
    if checkResponse(review):
        for name, _ in attempted:
            print(f"\nExplanation for {name}:")
            read_explanations(name)
    
    behavioral_questions()
