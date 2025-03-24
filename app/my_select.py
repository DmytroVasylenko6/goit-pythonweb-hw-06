import logging
from colorama import Fore, Style, init
from models import Grade, Group, Student, Subject, Teacher, init_db
from sqlalchemy import func
from sqlalchemy.orm import aliased, sessionmaker

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

init(autoreset=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter("%(message)s"))
logger.addHandler(console_handler)


def round_results(results):
    if isinstance(results, tuple):
        return tuple(
            round(value, 2) if isinstance(value, float) else value for value in results
        )
    elif isinstance(results, list):
        return [round_results(result) for result in results]
    return results


def task_1():
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return round_results(result)


def task_2(subject_name):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    if result:
        return round_results([result])[0]
    return result


def select_3(subject_name):
    SubjectAlias = aliased(Subject)

    query = (
        session.query(Group.name, func.avg(Grade.grade).label("average_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade, Grade.student_id == Student.id)
        .join(SubjectAlias, SubjectAlias.id == Grade.subject_id)
        .filter(SubjectAlias.name == subject_name)
        .group_by(Group.name)
        .all()
    )

    return round_results(query)


def select_4():
    result = session.query(func.avg(Grade.grade).label("average_grade")).scalar()
    if result is not None:
        return round(result, 2)
    return result


def select_5(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result


def select_6(group_name):
    result = (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )
    return result


def select_7(group_name, subject_name):
    result = (
        session.query(Student.name, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


def select_8(teacher_name):
    result = (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return round(result, 2) if result is not None else result


def select_9(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .all()
    )
    return result


def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .all()
    )
    return result


def log_query_result(query_result, title):
    logger.info(f"{Style.BRIGHT}{title}")
    if query_result:
        for row in query_result:
            logger.info(str(row))
    else:
        logger.error("No results found.")
    logger.info("\n" + "-" * 50)


if __name__ == "__main__":
    log_query_result(task_1(), "Top 5 Students by Average Grade")

    task_2_result = task_2("Mathematics")
    if task_2_result:
        log_query_result([task_2_result], "Student with Highest Average in Mathematics")
    else:
        logger.error("No student found with the highest average in Mathematics.")

    select_3_result = select_3("Service")
    if select_3_result:
        log_query_result(select_3_result, "Average Grade by Groups in Service")
    else:
        logger.error("No groups found for the subject 'Service'.")

    overall_avg = select_4()
    if overall_avg is not None:
        logger.warning(f"Overall Average Grade: {overall_avg}")
    else:
        logger.error("No average grade found.")

    select_5_result = select_5("Karen Bush")
    if select_5_result:
        log_query_result(select_5_result, "Courses Taught by Karen Bush")
    else:
        logger.error("No courses found taught by Karen Bush.")

    select_6_result = select_6("Group 1")
    if select_6_result:
        log_query_result(select_6_result, "Students in Group 1")
    else:
        logger.error("No students found in Group 1.")

    select_7_result = select_7("Group 1", "Service")
    if select_7_result:
        log_query_result(select_7_result, "Grades in Group 1 for Service")
    else:
        logger.error("No grades found in Group 1 for the 'Service' subject.")

    avg_8 = select_8("Karen Bush")
    if avg_8 is not None:
        logger.warning(f"Karen Bush Average Grade: {avg_8}")
    else:
        logger.error("No average grade found for Karen Bush.")

    select_9_result = select_9("Miguel Wilson")
    if select_9_result:
        log_query_result(select_9_result, "Courses Attended by Miguel Wilson")
    else:
        logger.error("No courses found for Miguel Wilson.")

    select_10_result = select_10("Miguel Wilson", "Karen Bush")
    if select_10_result:
        log_query_result(
            select_10_result, "Courses Taught by Karen Bush to Miguel Wilson"
        )
    else:
        logger.error("No courses found for Miguel Wilson taught by Karen Bush.")
