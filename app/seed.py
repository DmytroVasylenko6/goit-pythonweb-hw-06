import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Group, Teacher, Subject, Grade
from pprint import pprint
from colorama import init, Fore, Style
import logging

init(autoreset=True)

fake = Faker()

DATABASE_URL = "postgresql+psycopg2://postgres:2020202020@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

NUM_GROUPS = 3
NUM_TEACHERS = 5
NUM_SUBJECTS = 8
NUM_STUDENTS = 50
MAX_GRADES_PER_STUDENT = 20

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


def seed_data():
    try:
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()

        groups = []
        for i in range(NUM_GROUPS):
            group_name = f"Group {i+1}"
            groups.append(Group(name=group_name))

        session.add_all(groups)
        session.commit()

        logger.info(
            f"Groups: {', '.join([group.name for group in groups])} successfully added!"
        )

        teachers = [Teacher(name=fake.name()) for _ in range(NUM_TEACHERS)]
        session.add_all(teachers)
        session.commit()

        logger.info(
            f"Teachers: {', '.join([teacher.name for teacher in teachers])} successfully added!"
        )

        subjects = [
            Subject(name=fake.word().capitalize(), teacher=random.choice(teachers))
            for _ in range(NUM_SUBJECTS)
        ]
        session.add_all(subjects)
        session.commit()

        logger.info(
            f"Subjects: {', '.join([subject.name for subject in subjects])} successfully added!"
        )

        students = [
            Student(name=fake.name(), group=random.choice(groups))
            for _ in range(NUM_STUDENTS)
        ]
        session.add_all(students)
        session.commit()

        logger.info("Students:")
        for student_name in [student.name for student in students]:
            logger.info(student_name)

        grades = []
        for student in students:
            for _ in range(random.randint(1, MAX_GRADES_PER_STUDENT)):
                grade = Grade(
                    student=student,
                    subject=random.choice(subjects),
                    grade=random.uniform(1.0, 5.0),
                    date_received=fake.date_between(start_date="-2y", end_date="today"),
                )
                grades.append(grade)

        session.add_all(grades)
        session.commit()

        logger.info("Grades for students successfully added!")

        logger.info("Data successfully added to database!")
    except Exception as e:
        session.rollback()
        logger.error(f"Error while seeding database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()
