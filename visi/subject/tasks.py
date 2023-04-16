import datetime
import logging

from celery import shared_task
from django.core.mail import send_mail

from visi.subject.models import SubjectTimetable, ReminderMailQueue


logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=5)
def generate_mail_reminder(self):
    try:
        timetables = SubjectTimetable.objects.filter(
                                                    start_time__year=datetime.datetime.today().year,
                                                    start_time__month=datetime.datetime.today().month,
                                                    start_time__day=datetime.datetime.today().day
                                                    )

        list_reminder = []
        for timetable in timetables:
            reminder = ReminderMailQueue.objects.filter(subject_timetable=timetable)

            if reminder.count() > 0:
                if reminder.count() < 2:
                    if reminder[0].type == ReminderMailQueue.TYPE.start:
                        list_reminder.append(ReminderMailQueue(**{
                            "subject_timetable": timetable,
                            "sent_on": timetable.end_time - datetime.timedelta(minutes=5),
                            "type": ReminderMailQueue.TYPE.end,
                            "status": ReminderMailQueue.STATUS.queue
                        }))
                    elif reminder[0].type == ReminderMailQueue.TYPE.end:
                        list_reminder.append(ReminderMailQueue(**{
                            "subject_timetable": timetable,
                            "sent_on": timetable.start_time - datetime.timedelta(minutes=5),
                            "type": ReminderMailQueue.TYPE.start,
                            "status": ReminderMailQueue.STATUS.queue
                        }))
            else:
                list_reminder.append(ReminderMailQueue(**{
                    "subject_timetable": timetable,
                    "sent_on": timetable.start_time - datetime.timedelta(minutes=5),
                    "type": ReminderMailQueue.TYPE.start,
                    "status": ReminderMailQueue.STATUS.queue
                }))
                list_reminder.append(ReminderMailQueue(**{
                    "subject_timetable": timetable,
                    "sent_on": timetable.end_time - datetime.timedelta(minutes=5),
                    "type": ReminderMailQueue.TYPE.end,
                    "status": ReminderMailQueue.STATUS.queue
                }))
        ReminderMailQueue.objects.bulk_create(list_reminder)
    except Exception as e:
        logger.warning(f"[GENERATE EMAIL EXCEPTION] - {e}")


@shared_task(bind=True, max_retries=5)
def sent_mail(self):
    try:
        today_datetime = datetime.datetime(
            datetime.datetime.today().year,
            datetime.datetime.today().month,
            datetime.datetime.today().day,
            datetime.datetime.today().hour,
            datetime.datetime.today().minute,
            tzinfo=datetime.timezone.utc
        )
        reminders = ReminderMailQueue.objects.filter(sent_on__lte=today_datetime, status=ReminderMailQueue.STATUS.queue)

        for reminder in reminders:
            reminder.status = ReminderMailQueue.STATUS.process
            reminder.save()

            time = reminder.subject_timetable.start_time if reminder.type == "start" else reminder.subject_timetable.start_time
            time = time.strftime("%d/%m/%Y %H:%M:%S")
            send_mail(
                subject=f"Reminder for {reminder.type} classes",
                message=f"Please start the classes for \n Subject : {reminder.subject_timetable.subject.name} \n time {time}",
                from_email="admin@example.com",
                recipient_list=[reminder.subject_timetable.teacher.email]
            )
            reminder.status = ReminderMailQueue.STATUS.sent
    except Exception as e:
        reminder.status = ReminderMailQueue.STATUS.process
        logger.warning(f"[SENT EMAIL EXCEPTION] - {e}")
