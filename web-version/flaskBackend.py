from flask import Flask, jsonify, request
from flask_cors import CORS
from shared.utilities import read_problems, read_explanations
import csv
import os
import random


app = Flask(__name__)
CORS(app)

# Global variables
completed_probs = set()


# Normal function
def get_problems():
    problems_path = os.path.join("data", 'problems.csv')
    problems = read_problems(problems_path, completed_probs)
    return problems


# Filter on given topic
def filter_problems():
    data = request.json
    difficulties = data.get('difficulty', [])
    topic = data.get('topic')

    problems = get_problems()

    filtered_problems = problems

    if topic:
        filtered_problems = [p for p in filtered_problems if
                             p['topic'].lower() == topic.lower()]

    if difficulties:
        filtered_problems = [p for p in filtered_problems if
                             p['difficulty'].lower() in [d.lower()
                                                         for d in
                                                         difficulties]]

    return filtered_problems


def filter_company_problems(problems, company):
    # Company-specific problem filtering logic
    company_filters = {
        'amazon': lambda p: p['difficulty'] in ['medium', 'hard'] and
        p['topic'] in ['arrays', 'strings', 'trees', 'graphs', 'hashmap',
                       'linked-list'],
        'google': lambda p: p['difficulty'] in ['medium', 'hard'] and
        p['topic'] in ['algorithms', 'data structures', 'dynamic programming',
                       'recursion', 'binary-search'],
        'meta': lambda p: p['difficulty'] in ['medium', 'hard'] and
        p['topic'] in ['arrays', 'strings', 'trees', 'hashmap', 'linked-list'],
        'microsoft': lambda p: p['difficulty'] in ['medium', 'hard']
        and p['topic']
        in ['arrays', 'strings', 'linked lists', 'trees', 'hashmap'],
        'apple': lambda p: p['difficulty'] in ['medium', 'hard'] and p['topic']
        in ['arrays', 'strings', 'trees', 'linked-list']
    }

    if company in company_filters:
        return [p for p in problems if company_filters[company](p)]

    # If company not found in filters, return all problems
    return problems


@app.route('/api/problems/explanation/<problem_name>', methods=['GET'])
def get_explanation(problem_name):
    explanations_path = os.path.join('data', 'explanations.csv')
    explanation = read_explanations(explanations_path, problem_name)

    if explanation is None:
        return jsonify({'error': 'Explanation not found'}), 404

    return jsonify({'explanation': explanation})


@app.route('/api/problems/completed', methods=['GET'])
def get_completed_problems():
    return jsonify(list(completed_probs))


@app.route('/api/problems/topics', methods=['GET'])
def get_topics():
    problems_path = os.path.join("data", 'problems.csv')
    problems = read_problems(problems_path, set())
    topics = sorted(set(p['topic'] for p in problems))
    return jsonify(topics)


@app.route('/api/practice/random', methods=['POST'])
def get_random_practice_problem():
    filtered_problems = filter_problems()

    if not filtered_problems:
        return jsonify({'error': 'No problems found with the'
                        ' given criteria'}), 404

    chosen = random.choice(filtered_problems)
    completed_probs.add(chosen['name'])

    return jsonify(chosen)


# Route handlers are called by frontend code compared to normal helper function
# You decide what "HTTP" method *can* be used: Get, Post, Put, Patch, Delete,
# etc. In the backend, you decide what can be accepted from frontend,
# In this case, only accepts post, if accepted more than 1, likely need cases
# for each. GET: Retrieve data from the backend without changing it.
# POST: Send data to the backend or trigger an operation.
# PUT: Replace an existing resource (any data or thing you have) entirely.
# PATCH: Partially update an existing resource.
# DELETE: Remove an existing resource.
# Use post since you aren't updating, just operating on filtered data
@app.route('/api/mock-interview/start', methods=['POST'])
def start_mock_interview():
    data = request.json
    company = data.get('company')
    question_count = data.get('questionCount', 3)

    problems = get_problems()

    # Filter problems based on company preferences
    company_problems = filter_company_problems(problems, company)

    if not company_problems:
        # If no company-specific problems found, fall back to all problems
        company_problems = problems

    # Select random problems
    selected_problems = random.sample(company_problems,
                                      min(question_count,
                                          len(company_problems)))

    # Mark problems as completed
    for problem in selected_problems:
        completed_probs.add(problem['name'])

    return jsonify({'problems': selected_problems})


@app.route('/api/mock-interview/behavioral', methods=['GET'])
def get_behavioral_questions():
    behavioral_path = os.path.join("data", 'behavioral.csv')
    questions = []

    with open(behavioral_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)

    # Select 2-4 random questions
    num_questions = random.randint(2, 4)
    selected_questions = random.sample(questions, min(num_questions,
                                                      len(questions)))

    return jsonify({'questions': selected_questions})


if __name__ == '__main__':
    app.run(debug=True)
