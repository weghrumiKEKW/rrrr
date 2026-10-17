
EXCELLENT_SCORE = 90
GOOD_SCORE = 80
AVERAGE_SCORE = 70
PASSING_SCORE = 60


def calculate_grade(score):
    """Tələbənin balına əsasən qiymət dərəcəsini qaytarır."""

    if score >= EXCELLENT_SCORE:
        return "A"
    elif score >= GOOD_SCORE:
        return "B"
    elif score >= AVERAGE_SCORE:
        return "C"
    elif score >= PASSING_SCORE:
        return "D"
    else:
        return "F"


def calculate_statistics(students):
    """Tələbələrin ümumi sayını və bal statistikalarını hesablayır."""

    if not students:
        return {
            "total_students": 0,
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0
        }

    scores = [student["Score"] for student in students]

    total_students = len(students)
    average_score = round(sum(scores) / total_students, 1)
    highest_score = max(scores)
    lowest_score = min(scores)

    return {
        "total_students": total_students,
        "average_score": average_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score
    }