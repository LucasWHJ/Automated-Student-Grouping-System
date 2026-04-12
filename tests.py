from course import Student, Course
from survey import (Answer, YesNoQuestion, Survey, NumericQuestion,
                    MultipleChoiceQuestion, CheckboxQuestion)
from criterion import HomogeneousCriterion
from grouper import Group, Grouping, AlphaGrouper, GreedyGrouper


###############################################################################
# Task 2 Test cases
###############################################################################


def test_student_has_answer() -> None:
    """Test Student.has_answer returns True only after an answer is set."""
    s = Student(1, "Alice")
    q = YesNoQuestion(1, "Is it cold?")
    assert s.has_answer(q) is False
    s.set_answer(q, Answer(True))
    assert s.has_answer(q) is True


def test_student_get_answer() -> None:
    """Test Student.get_answer retrieves the correct recorded answer."""
    s = Student(1, "Alice")
    q = YesNoQuestion(1, "Question")
    ans = Answer(True)
    s.set_answer(q, ans)
    assert s.get_answer(q).content is True


###############################################################################
# Task 3 Test cases
###############################################################################


def test_course_enroll_students() -> None:
    """Test Course.enroll_students adds students to the course."""
    c = Course("CSC148")
    s1 = Student(1, "Alice")
    c.enroll_students([s1])
    assert len(c.get_students()) == 1


def test_course_all_answered() -> None:
    """Test Course.all_answered checks
    if all students answered all questions.
    """
    c = Course("CSC148")
    s1 = Student(1, "Alice")
    q = YesNoQuestion(1, "Q")
    c.enroll_students([s1])
    survey = Survey([q])
    assert c.all_answered(survey) is False
    s1.set_answer(q, Answer(True))
    assert c.all_answered(survey) is True


def test_course_get_students() -> None:
    """Test Course.get_students returns a tuple sorted by student ID."""
    c = Course("CSC148")
    s1 = Student(10, "Zoe")
    s2 = Student(1, "Adam")
    c.enroll_students([s1, s2])
    students = c.get_students()
    assert isinstance(students, tuple)
    assert students[0].id == 1


###############################################################################
# Task 4 Test cases
###############################################################################


def test_validate_answer() -> None:
    """Test inherited validate_answer in YesNoQuestion."""
    q = YesNoQuestion(1, "Q")
    assert q.validate_answer(Answer(True)) is True
    assert q.validate_answer(Answer("Not Boolean")) is False


def test_get_similarity() -> None:
    """Test inherited get_similarity in YesNoQuestion."""
    q = YesNoQuestion(1, "Q")
    a1, a2 = Answer(True), Answer(False)
    assert q.get_similarity(a1, a1) == 1.0
    assert q.get_similarity(a1, a2) == 0.0


def test_answer_is_valid() -> None:
    """Test Answer.is_valid method against a question."""
    q = YesNoQuestion(1, "Q")
    assert Answer(True).is_valid(q) is True
    assert Answer(99).is_valid(q) is False


###############################################################################
# Task 5 Test cases
###############################################################################


def test_answer_is_valid_yes_no() -> None:
    """Test Answer.is_valid with a YesNoQuestion."""
    q = YesNoQuestion(1, "Are you OK?")
    # Valid boolean answers
    assert Answer(True).is_valid(q)
    assert Answer(False).is_valid(q)
    # Invalid types
    assert not Answer("Yes").is_valid(q)
    assert not Answer(1).is_valid(q)


def test_answer_is_valid_numeric() -> None:
    """Test Answer.is_valid with a NumericQuestion (range 1-10)."""
    q = NumericQuestion(2, "Rate your stress", 1, 10)
    # Valid boundaries and middle
    assert Answer(1).is_valid(q)
    assert Answer(10).is_valid(q)
    assert Answer(5).is_valid(q)
    # Invalid values (out of range or wrong type)
    assert not Answer(0).is_valid(q)
    assert not Answer(11).is_valid(q)
    assert not Answer(5.5).is_valid(q)


def test_answer_is_valid_multiple() -> None:
    """Test Answer.is_valid with a MultipleChoiceQuestion."""
    options = ["Apple", "Banana", "Cherry"]
    q = MultipleChoiceQuestion(3, "Pick a fruit", options)
    # Valid options
    assert Answer("Apple").is_valid(q)
    assert Answer("Cherry").is_valid(q)
    # Invalid options (not in list or wrong type)
    assert not Answer("Date").is_valid(q)
    assert not Answer(1).is_valid(q)


def test_answer_is_valid_checkbox() -> None:
    """Test Answer.is_valid with a CheckboxQuestion."""
    options = ["Python", "Java", "C++"]
    q = CheckboxQuestion(4, "Languages known", options)
    # Valid: single, multiple, or all options
    assert Answer(["Python"]).is_valid(q)
    assert Answer(["Python", "C++"]).is_valid(q)
    assert Answer(["Python", "Java", "C++"]).is_valid(q)
    # Invalid: empty list, duplicates, or non-existent options
    assert not Answer([]).is_valid(q)
    assert not Answer(["Python", "Python"]).is_valid(q)
    assert not Answer(["Ruby"]).is_valid(q)
    assert not Answer(["Python", "Ruby"]).is_valid(q)


###############################################################################
# Task 6 Test cases
###############################################################################


def test_criterion_score_answers() -> None:
    """Test HomogeneousCriterion.score_answers with a simple group."""
    q = YesNoQuestion(1, "Q")
    c = HomogeneousCriterion()
    ans = [Answer(True), Answer(True)]
    assert c.score_answers(q, ans) == 1.0


###############################################################################
# Task 7 Test cases
###############################################################################


def test_group_methods() -> None:
    """Test Group methods: len, contains, and get_members."""
    s1 = Student(1, "A")
    g = Group([s1])
    assert len(g) == 1
    assert s1 in g
    assert g.get_members() == [s1]


###############################################################################
# Task 8 Test cases
###############################################################################


def test_grouping_add_group() -> None:
    """Test Grouping.add_group and its ID uniqueness enforcement."""
    s1 = Student(1, "A")
    g1 = Group([s1])
    grouping = Grouping()
    assert grouping.add_group(g1) is True
    # Should return False when adding a student already in the grouping
    assert grouping.add_group(Group([s1])) is False


###############################################################################
# Task 9 Test cases
###############################################################################


def test_survey_get_questions() -> None:
    """Test Survey.get_questions returns the list of questions."""
    q = YesNoQuestion(1, "Q")
    s = Survey([q])
    assert s.get_questions() == [q]


def test_survey_set_w_and_c() -> None:
    """Test Survey weight and criterion setters."""
    q = YesNoQuestion(1, "Q")
    s = Survey([q])
    assert s.set_weight(10, q) is True
    assert s.set_criterion(HomogeneousCriterion(), q) is True


def test_survey_score_students() -> None:
    """Test Survey.score_students with matching answers."""
    q = YesNoQuestion(1, "Q")
    s1, s2 = Student(1, "A"), Student(2, "B")
    s1.set_answer(q, Answer(True))
    s2.set_answer(q, Answer(True))
    survey = Survey([q])
    assert survey.score_students([s1, s2]) == 1.0


def test_survey_score_grouping() -> None:
    """Test Survey.score_grouping averages group scores."""
    q = YesNoQuestion(1, "Q")
    s1, s2 = Student(1, "A"), Student(2, "B")
    s1.set_answer(q, Answer(True))
    s2.set_answer(q, Answer(True))
    survey = Survey([q])
    grouping = Grouping()
    grouping.add_group(Group([s1, s2]))
    assert survey.score_grouping(grouping) == 1.0


###############################################################################
# Task 10 Test cases
###############################################################################


def test_alpha_make_grouping() -> None:
    """Test AlphaGrouper groups students by name."""
    c = Course("C")
    s1, s2 = Student(1, "Zebra"), Student(2, "Apple")
    c.enroll_students([s1, s2])
    g = AlphaGrouper(1).make_grouping(c, Survey([]))
    assert g.get_groups()[0].get_members()[0].name == "Apple"


def test_greedy_make_grouping() -> None:
    """Test GreedyGrouper uses lowest ID as initial student."""
    c = Course("C")
    s1, s2 = Student(10, "A"), Student(5, "B")
    c.enroll_students([s1, s2])
    g = GreedyGrouper(2).make_grouping(c, Survey([]))
    assert g.get_groups()[0].get_members()[0].id == 5
