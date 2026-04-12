"""
=== Module Description ===

This file contains a class that describes a survey as well as classes that
describe different types of questions that can be asked on a survey.
"""
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from criterion import HomogeneousCriterion
if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """An abstract class representing a question used in a survey

    This class should not be instantiated directly.

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize this question with the text <text>.

        Preconditions:
        - len(text) > 0
        """
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        return f"{self.id}: {self.text}"

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.
        """
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question
        """
        raise NotImplementedError


class MultipleChoiceQuestion(Question):
    """A question whose answers can be one of several options

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Private Attribute:
    - _options: the possible answers

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str
    _options: list

    def __init__(self, id_: int, text: str, options: list) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.

        Preconditions:
        - len(text) > 0
        - len(options) >= 2
        - len(set(options)) == len(options)
        """
        super().__init__(id_, text)
        self._options = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        result = self.text
        i = 1
        for opt in self._options:
            result += '\n' + str(i) + '. ' + str(opt)
            i += 1
        return result

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the answer options for this
        question.
        """
        if answer.content not in self._options:
            return False
        return type(answer.content) is type(self._options[0])

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question.
        """
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class NumericQuestion(Question):
    """A question whose answer can be an integer between some minimum and
    maximum value (inclusive).

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Private Attributes:
    - _min: the minimum integer
    - _max: the maximum integer

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str
    _min: int
    _max: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        Precondition:
        - len(text) > 0
        - min_ < max_
        """
        super().__init__(id_, text)
        self._min = min_
        self._max = max_

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return f"{self.id}: {self.text} (Range: {self._min} to {self._max})"

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        return (isinstance(answer.content, int)
                and (self._min <= answer.content <= self._max))

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity is calculated as follows:
        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximum
           and minimum possible answers.
        3. subtract the value of step 2 from 1.0

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question
        """
        abs_diff = abs(answer1.content - answer2.content)
        t_range = self._max - self._min
        return 1.0 - (abs_diff / t_range)


class YesNoQuestion(MultipleChoiceQuestion):
    """A question whose answer is either yes (represented by True) or
    no (represented by False).

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Representation Invariants:
     - len(self.text) > 0
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize a question with the text <text> and id <id>.
        """
        super().__init__(id_, text, [True, False])


class CheckboxQuestion(Question):
    """A question whose answers can be one or more of several options

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Private Attribute:
    - _options: the possible answers

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str
    _options: list

    def __init__(self, id_: int, text: str, options: list[str]) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.
        """
        super().__init__(id_, text)
        self._options = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        result = f"{self.id}: {self.text}\nSelect one or more:"
        for opt in self._options:
            result += f"\n  - {opt}"
        return result

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid iff:
            * It is a non-empty list.
            * It has no duplicate entries.
            * Every item in it is one of the answer options for this question.
        """
        if not isinstance(answer.content, list) or len(answer.content) == 0:
            return False
        content_set = set(answer.content)
        if len(content_set) != len(answer.content):
            return False
        for item in answer.content:
            if item not in self._options:
                return False
        return True

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content.
        If there are zero unique strings in <answer1>.content and
        <answer2>.content combined, return 1.0

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer2>.content == ['c', 'b', 'd'], there are 2 strings common to
        both: 'c' and 'b'; and there are 4 unique strings that appear in both:
        'a', 'b', 'c', and 'd'. Therefore, the similarity between these two
        answers is 2/4 = 0.5.

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question
        """
        set1 = set(answer1.content)
        set2 = set(answer2.content)
        num_intersection = len(set1.intersection(set2))
        num_union = len(set1.union(set2))
        if num_union == 0:
            return 1.0
        return num_intersection / num_union


class Answer:
    """An answer to a question used in a survey

    Public Attributes:
    - content: an answer to a single question
    """
    content: Any

    def __init__(self, content: Any) -> None:
        """Initialize this answer with content <content>"""
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff this answer is a valid answer to <question>"""
        return question.validate_answer(self)


class Survey:
    """A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    Representation Invariants:
    - No two questions on this survey have the same id

    NOTE: The weights associated with the questions in a survey do NOT have to
          sum up to any particular amount.
    """
    # Private Attributes:
    # - _questions: a dictionary mapping a question's id to the question itself
    # - _criteria: a dictionary mapping a question's id to its associated
    #   criterion
    # - _weights: a dictionary mapping a question's id to a weight -- an integer
    # representing the importance of this criteria.
    #
    # Representation Invariants - for Private Attributes:
    # - Each key in _questions equals the id attribute of its value
    # - The dictionaries _questions, _criteria, and _weights all have the same
    #   keys
    # - Each value in _weights is greater than 0
    _questions: dict[int, Question]
    _criteria: dict[int, Criterion]
    _weights: dict[int, int]

    def __init__(self, questions: list[Question]) -> None:
        """Initialize a new survey that contains every question in <questions>.

        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        self._questions = {}
        self._criteria = {}
        self._weights = {}

        for question in questions:
            self._questions[question.id] = question
            self._criteria[question.id] = HomogeneousCriterion()
            self._weights[question.id] = 1

    def __len__(self) -> int:
        """Return the number of questions in this survey"""
        return len(self._questions)

    def __contains__(self, question: Question) -> bool:
        """Return True iff there is a question in this survey with the same
        id as <question>.
        """
        return question.id in self._questions

    def __str__(self) -> str:
        """Return a string containing the string representation of all
        questions in this survey.

        You can choose the precise format of this string.
        """
        result = ''
        for question in self._questions.values():
            result += str(question) + '\n'
        return result.strip()

    def get_questions(self) -> list[Question]:
        """Return a list of all questions in this survey"""
        return list(self._questions.values())

    def _get_criterion(self, question: Question) -> Criterion:
        """Return the criterion associated with <question> in this survey.

        Precondition:
        - <question>.id occurs in this survey
        """
        return self._criteria[question.id]

    def _get_weight(self, question: Question) -> int:
        """Return the weight associated with <question> in this survey.

        Precondition:
        - <question>.id occurs in this survey
        """
        return self._weights[question.id]

    def set_weight(self, weight: int, question: Question) -> bool:
        """Set the weight associated with <question> to <weight> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.

        Precondition:
        - weight > 0
        """
        if question.id not in self._questions:
            return False
        self._weights[question.id] = weight
        return True

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """Set the criterion associated with <question> to <criterion> and
        return True.

        If <question>.id does not occur in this survey,
        do not set the <criterion> and return False instead.
        """
        if question.id not in self._questions:
            return False
        self._criteria[question.id] = criterion
        return True

    def score_students(self, students: list[Student]) -> float:
        """Return a quality score for <students> calculated based on their
        answers to the questions in this survey, and the associated criterion
        and weight for each question.

        The score is determined using the following algorithm:
        1. For each question in this survey, find the question's associated
           criterion (do we want homogeneous answers, for instance), weight,
           and <students> answers to the question. Use the score_answers method
           for its criterion to calculate how well the <students> answers
           satisfy the criterion. Multiply this quality score by the question's
           weight.
        2. Find the average of all quality scores from step 1.

        This method should NOT throw an InvalidAnswerError. If one occurs
        during the execution of this method or if there are no questions in
        <self>, return zero.

        Precondition:
        - All students in <students> have an answer to all questions in this
            survey
        - len(students) > 0
        """
        if not self._questions:
            return 0.0
        total_weighted_score = 0.0

        for q_id in self._questions:
            question = self._questions[q_id]
            criterion = self._criteria[q_id]
            weight = self._weights[q_id]

            answers = []
            for student in students:
                ans = student.get_answer(question)
                if ans is None or not ans.is_valid(question):
                    return 0.0
                answers.append(ans)

            score = criterion.score_answers(question, answers)
            total_weighted_score += score * weight
        return total_weighted_score / len(self._questions)

    def score_grouping(self, grouping: Grouping) -> float:
        """Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> return 0.0. Otherwise, the score
        is determined using the following algorithm:
        1. For each group in <grouping>, calculate the score for the members of
           this group based on their answers to the questions in this survey.
        2. Return the average of all the scores calculated in step 1.

        Precondition:
        - All students in the groups in <grouping> have an answer to all
        questions in this survey
        """
        groups = grouping.get_groups()
        if not groups:
            return 0.0
        total_score = 0.0
        for group in groups:
            total_score += self.score_students(group.get_members())
        return total_score / len(groups)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper'],
                                'disable': ['E9992']})
