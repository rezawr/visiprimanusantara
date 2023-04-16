import names
import random
import sys
import datetime

from django.core.management.base import BaseCommand, CommandError
from py_calendars import calendar

from visi.teacher.models import Teacher
from visi.subject.models import Subject, SubjectTimetable


class Command(BaseCommand):
    help = "Randomize teacher, subject and assigning timetable to teacher"
    requires_migrations_checks = True
    stealth_options = ('stdin',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TeacherModel = Teacher
        self.SubjectModel = Subject
        self.SubjectTimetableModel = SubjectTimetable

    def add_arguments(self, parser):
        parser.add_argument(
            '--number_of_teacher',
            dest='number_of_teacher', default=None,
            help='Specifies the number of generated teacher.',
        )

        parser.add_argument(
            '--number_of_subject',
            dest='number_of_subject', default=None,
            help='Specifies the number of generated subject.',
        )

        parser.add_argument(
            '--number_of_timetable',
            dest='number_of_timetable', default=None,
            help='Specifies the number of generated time tables per week.',
        )

        parser.add_argument(
            '--month',
            dest='month', default=None,
            help='Specifies the month and year [1, 2, ...]',
        )

        parser.add_argument(
            '--year',
            dest='year', default=None,
            help='Specifies the month and year [2000, 2001, ...]',
        )

    def handle(self, *args, **options):
        number_of_teacher = options['number_of_teacher']
        number_of_subject = options['number_of_subject']
        number_of_timetable = int(options['number_of_timetable'])
        month = int(options['month'])
        year = int(options['year'])

        if None in [number_of_teacher, number_of_subject, number_of_timetable, month, year]:
            raise CommandError("You must use --number_of_teacher --number_of_subject --number_of_timetable --month --year")

        teachers = []
        subjects = []
        for x in range(int(number_of_teacher)):
            name = str(names.get_full_name())
            email = '%s@example.com' %name.replace(' ', '_').lower()

            teachers.append(self.TeacherModel(**{
                "name": name,
                "email": email
            }))

        for x in range(int(number_of_subject)):
            subjects.append(self.SubjectModel(**{
                "name": f"subject-{random.randint(111,999)}"
            }))

        self.TeacherModel.objects.bulk_create(teachers)
        self.SubjectModel.objects.bulk_create(subjects)

        if month + 1 < 13:
            new_month = month + 1
            new_year = year
        else:
            new_month = (month + 1) % 12
            new_year = year + 1

        first_day = datetime.datetime(year, month, 1)
        last_day = datetime.datetime(new_year, new_month, 1) - datetime.timedelta(days=1)
        
        weekdays = [6,7]
        list_weekdays = []
        for dt in self.daterange(first_day, last_day):
            if dt.isoweekday() not in weekdays:
                list_weekdays.append(dt)

        # Make the slot and randomize teacher
        list_weekdays_per_week = [[]]
        count = 0
        week = 0

        for lw in list_weekdays:
            if count == 5:
                week += 1
                count = 0
                list_weekdays_per_week.append([])

            list_weekdays_per_week[week].append(lw)
            count += 1

        teachers = self.TeacherModel.objects.all()
        subjects = self.SubjectModel.objects.all()

        timetables = []
        for lw in list_weekdays_per_week:
            for x in range(number_of_timetable):
                h = random.randint(7,15)
                m = random.randint(0,60)
                random_timetable = random.choice(lw)

                start = random_timetable + datetime.timedelta(hours=h, minutes=m)
                end = start + datetime.timedelta(hours=1)

                timetables.append(self.SubjectTimetableModel(**{
                    "teacher": random.choice(teachers),
                    "subject": random.choice(subjects),
                    "start_time": start,
                    "end_time": end
                }))

        self.SubjectTimetableModel.objects.bulk_create(timetables)

    def daterange(self, date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + datetime.timedelta(n)
