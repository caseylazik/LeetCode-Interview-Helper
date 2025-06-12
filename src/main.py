from utilities import read_problems
from pathlib import Path

from mock_interview import mock_interview
from normal_practice import problem_chooser


# Main program
def main():

    BASE_DIR = Path(__file__).resolve().parent.parent

    # Handles different os
    problems_path = BASE_DIR / "data" / "problems.csv"
    explanations_path = BASE_DIR / "data" / "explanations.csv"

    # Check for needed files
    if not problems_path.exists() or not explanations_path.exists():
        print("Error: Missing required data files!")
        print(f"Expected files:\n  - {problems_path}\n  - {explanations_path}")
        return

    print()
    print("SESSION START:")
    print()

    print()
    print("Hello,")
    print("Welcome to the LeetCode Helper/Randomizer!")

    mode = input("Choose a mode: (1) Normal Practice "
                 "(2) Mock Interview: ").strip()

    if mode == '1':
        print("\nStarting normal practice mode...")
        # Call normal practice flow (existing functionality)
        problem_chooser()
    elif mode == '2':
        print("\nStarting mock interview mode...")
        probs = read_problems(problems_path, set())
        mock_interview(probs)
    else:
        print("Invalid choice. Exiting.")

    # Potential TODOs:

    # Improve interface
    # Behavioral questions!


if __name__ == '__main__':
    main()
