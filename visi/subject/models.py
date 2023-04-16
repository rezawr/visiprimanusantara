from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

from visi.teacher.models import Teacher


class Subject(models.Model):
    name = models.CharField(
        _("name"),
        max_length=120
    )

    def __str__(self):
        return self.name


class SubjectTimetable(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))

    def __str__(self):
        return f"{self.subject.name} - {self.teacher.name}"


class ReminderMailQueue(models.Model):
    STATUS = Choices(
        ("queue", _("Queue")),
        ("process", _("Process")),
        ("sent", _("Sent")),
        ("error", _("Error")),
    )

    TYPE = Choices(
        ("start", _("Start")),
        ("end", _("end"))
    )

    subject_timetable = models.ForeignKey(
        SubjectTimetable,
        on_delete=models.CASCADE,
        related_name="subject_timetable"
    )
    sent_on = models.DateTimeField(_('sent reminder email on'))
    type = models.CharField(
        _("Reminder type"),
        choices=TYPE,
        max_length=6
    )
    status = models.CharField(
        _("Status"),
        choices=STATUS,
        default=STATUS.queue,
        max_length=10
    )

    class Meta:
        unique_together = (('subject_timetable', 'type'),)

    def __str__(self):
        return f"{self.subject_timetable.subject.name} - {self.subject_timetable.teacher.name}"
