import csv
import os
import threading


# Read problem data
def read_problems(file_path, completed_probs):
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
def read_explanations(probName):
    file_path = os.path.join('data', 'explanations.csv')

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['problem_name']
            if name == probName:
                print(row['explanation'])
                return


# Check yes or no response
def checkResponse(input):
    input = input.strip().lower()
    return input == 'y' or input == 'yes'


# Need threading library to make this work
def get_input_with_timeout(prompt, timeout):
    user_input = None

    def get_input():
        nonlocal user_input
        user_input = input(prompt)

    thread = threading.Thread(target=get_input)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("\nTime is up!")
        thread.join()  # Wait for the thread to finish before exiting
        return None

    return user_input
