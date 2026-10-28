# Automated Student Grouping System

A Python system that forms student groups using survey responses, configurable scoring criteria, and interchangeable grouping algorithms.

The project models the full workflow: enrol students in a course, collect and validate their answers, define what makes a good group, and compare the resulting groupings. It demonstrates object-oriented design, polymorphism, and heuristic optimisation.

## Features

- **Four question types:** multiple choice, numeric, yes/no, and checkbox questions, each with its own answer validation and similarity calculation.
- **Configurable criteria:** favour similar answers, favour different answers, or penalise groups where a member has a unique answer.
- **Question weights:** give selected survey questions more influence over the group score.
- **Three grouping strategies:** alphabetical grouping, greedy construction, and simulated annealing.
- **Group evaluation:** calculate scores for individual groups and complete groupings.
- **Student tracking:** prevent duplicate student IDs during course enrolment and duplicate membership across groups.

## Getting started

Use Python 3.10 or newer. The core modules use only the Python standard library.

```bash
git clone https://github.com/LucasWHJ/Automated-Student-Grouping-System.git
cd Automated-Student-Grouping-System
```

This repository exposes Python classes rather than a standalone application. Save the following example as `demo.py` in the repository root, then run `python demo.py`.

```python
from course import Course, Student
from criterion import HomogeneousCriterion
from grouper import AlphaGrouper, GreedyGrouper, SimulatedAnnealingGrouper
from survey import Answer, MultipleChoiceQuestion, Survey

question = MultipleChoiceQuestion(
    1, "Preferred meeting time?", ["Morning", "Evening"]
)
survey = Survey([question])
survey.set_criterion(HomogeneousCriterion(), question)

course = Course("Project Workshop")
responses = [
    (1, "Alice", "Morning"),
    (2, "Bob", "Evening"),
    (3, "Carol", "Morning"),
    (4, "David", "Evening"),
]

for student_id, name, response in responses:
    student = Student(student_id, name)
    student.set_answer(question, Answer(response))
    course.enroll_students([student])

assert course.all_answered(survey)

strategies = [
    AlphaGrouper(group_size=2),
    GreedyGrouper(group_size=2),
    SimulatedAnnealingGrouper(group_size=2, iterations=1000),
]

for strategy in strategies:
    grouping = strategy.make_grouping(course, survey)
    print(f"\n{type(strategy).__name__}")
    print(grouping)
    print(f"Score: {survey.score_grouping(grouping):.2f}")
```

With these responses, alphabetical grouping pairs students with different meeting preferences, while greedy grouping pairs Alice with Carol and Bob with David.

## Grouping strategies

| Strategy | Approach | Purpose |
| --- | --- | --- |
| `AlphaGrouper` | Sort students by name and divide them into groups. | Simple baseline independent of survey scores. |
| `GreedyGrouper` | Start with the lowest remaining student ID and repeatedly add the candidate with the highest resulting group score. | Build groups using local score improvements. |
| `SimulatedAnnealingGrouper` | Swap students between groups, sometimes accept lower scores as the temperature decreases, and retain the best grouping found. | Search beyond the initial grouping. |

The simulated annealing implementation uses iteration-based random seeds and a linear cooling schedule. Neither greedy construction nor simulated annealing guarantees a globally optimal solution.

Group sizes never exceed the requested size; the final group may be smaller when the class size is not divisible by it. Follow the documented preconditions: `group_size > 1` and the course has more students than `group_size`.

## Scoring and customisation

Each question supplies an answer similarity measure:

- **Multiple choice / yes-no:** `1.0` for equal answers, otherwise `0.0`.
- **Numeric:** similarity decreases with the distance between answers, relative to the question's allowed range.
- **Checkbox:** Jaccard similarity, calculated as intersection size divided by union size.

A criterion converts those answers into a group score:

| Criterion | Higher scores favour |
| --- | --- |
| `HomogeneousCriterion` | Similar answers, averaged over all distinct pairs. |
| `HeterogeneousCriterion` | Different answers, using one minus average similarity. |
| `LonelyMemberCriterion` | Groups where every answer has an identical match from another member. |

For example, to prioritise diversity on a question:

```python
from criterion import HeterogeneousCriterion

survey.set_criterion(HeterogeneousCriterion(), question)
survey.set_weight(2, question)
```

For a survey with `n` questions, the group score is:

```text
group score = sum(question weight × criterion score) / n
```

The denominator is the number of questions, so weights greater than one can produce scores above `1.0`. A grouping's score is the unweighted average of its group scores. New questions default to `HomogeneousCriterion` with weight `1`.

Provide valid answers to every survey question before grouping. An empty survey scores `0.0`.

## Project structure

```text
.
├── course.py      # Student records, answers, and course enrolment
├── survey.py      # Question types, answer validation, and survey scoring
├── criterion.py   # Abstract criterion and three concrete scoring policies
├── grouper.py     # Groups, grouping strategies, and optimisation helpers
└── tests.py       # Unit tests
```

The abstract `Question`, `Criterion`, and `Grouper` classes provide extension points for new question formats, scoring policies, and grouping algorithms.

## Tests

Install pytest and explicitly select the test file:

```bash
python -m pip install pytest
python -m pytest tests.py -v
```

The optional `python_ta` imports in the modules' `__main__` blocks are for static analysis; they are not needed when importing the classes or running the example above.
