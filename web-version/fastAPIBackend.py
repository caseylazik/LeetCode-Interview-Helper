from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from shared.utilities import read_problems, read_explanations
import csv
import os
import random


# Create the FastAPI application
app = FastAPI()

# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,  # (Cross-Origin Resource Sharing) - allow different origin
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
completed_probs = set()


# Normal function: get all available problems
def get_problems():
    problems_path = os.path.join("data", "problems.csv")
    problems = read_problems(problems_path, completed_probs)
    return problems


# Define the data we expect from the frontend
class PracticeRequest(BaseModel):
    difficulty: list[str] = []
    topic: Optional[str] = None


class InterviewRequest(BaseModel):
    company: Optional[str] = None
    questionCount: int = 3


# Filter problems by topic and difficulty
def filter_problems(data):
    difficulties = data.difficulty
    topic = data.topic

    problems = get_problems()
    filtered_problems = problems

    if topic:
        filtered_problems = [
            p for p in filtered_problems
            if p["topic"].lower() == topic.lower()
        ]

    if difficulties:
        filtered_problems = [
            p for p in filtered_problems
            if p["difficulty"].lower()
            in [d.lower() for d in difficulties]
        ]

    return filtered_problems


# Filter problems by company
def filter_company_problems(problems, company):
    company_filters = {
        "amazon": lambda p: p["difficulty"] in ["medium", "hard"]
        and p["topic"] in [
            "arrays", "strings", "trees", "graphs",
            "hashmap", "linked-list"
        ],

        "google": lambda p: p["difficulty"] in ["medium", "hard"]
        and p["topic"] in [
            "algorithms", "data structures",
            "dynamic programming", "recursion", "binary-search"
        ],

        "meta": lambda p: p["difficulty"] in ["medium", "hard"]
        and p["topic"] in [
            "arrays", "strings", "trees", "hashmap", "linked-list"
        ],

        "microsoft": lambda p: p["difficulty"] in ["medium", "hard"]
        and p["topic"] in [
            "arrays", "strings", "linked lists", "trees", "hashmap"
        ],

        "apple": lambda p: p["difficulty"] in ["medium", "hard"]
        and p["topic"] in [
            "arrays", "strings", "trees", "linked-list"
        ],
    }

    if company and company.lower() in company_filters:
        return [
            p for p in problems
            if company_filters[company.lower()](p)
        ]

    return problems


# Get an explanation for a problem
@app.get("/api/problems/explanation/{problem_name}")
def get_explanation(problem_name: str):
    explanations_path = os.path.join("data", "explanations.csv")
    explanation = read_explanations(
        explanations_path, problem_name
    )

    if explanation is None:
        raise HTTPException(
            status_code=404,
            detail="Explanation not found"
        )

    return {"explanation": explanation}


# Get completed problems
@app.get("/api/problems/completed")
def get_completed_problems():
    return list(completed_probs)


# Get all available topics
@app.get("/api/problems/topics")
def get_topics():
    problems_path = os.path.join("data", "problems.csv")
    problems = read_problems(problems_path, set())

    topics = sorted(set(p["topic"] for p in problems))
    return topics


# Get a random practice problem
@app.post("/api/practice/random")
def get_random_practice_problem(data: PracticeRequest):
    filtered_problems = filter_problems(data)

    if not filtered_problems:
        raise HTTPException(
            status_code=404,
            detail="No problems found with the given criteria"
        )

    chosen = random.choice(filtered_problems)
    completed_probs.add(chosen["name"])

    return chosen


# Start a coding mock interview
@app.post("/api/mock-interview/start")
def start_mock_interview(data: InterviewRequest):
    problems = get_problems()

    company_problems = filter_company_problems(
        problems, data.company
    )

    if not company_problems:
        company_problems = problems

    selected_problems = random.sample(
        company_problems,
        min(data.questionCount, len(company_problems))
    )

    for problem in selected_problems:
        completed_probs.add(problem["name"])

    return {"problems": selected_problems}


# Get random behavioral interview questions
@app.get("/api/mock-interview/behavioral")
def get_behavioral_questions():
    behavioral_path = os.path.join("data", "behavioral.csv")

    with open(
        behavioral_path, newline="", encoding="utf-8"
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)

    num_questions = random.randint(2, 4)

    selected_questions = random.sample(
        questions, min(num_questions, len(questions))
    )

    return {"questions": selected_questions}
