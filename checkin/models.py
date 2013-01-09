from django.db import models
import datetime

# Create your models here.
class Block(models.Model):
    name = models.CharField(max_length=5, blank=True)
    start_at = models.TimeField('beginning of block')
    end_at = models.TimeField('end of block')
    def __unicode__(self):
        if self.name == '':
            return "{0} to {1}".format(
                    self.start_at.strftime("%I:%M %p"),
                    self.end_at.strftime("%I:%M %p"))
        else:
            return self.name

class Employee(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Period(models.Model):
    name = models.CharField(max_length=10, blank=True)
    start_at = models.DateTimeField('beginning of period')
    end_at = models.DateTimeField('end of period')
    def __unicode__(self):
        if self.name == '':
            return "{0} to {1}".format(
                    self.start_at.strftime("%Y-%m-%d"),
                    self.end_at.strftime("%Y-%m-%d"))
        else:
            return self.name

class Shift(models.Model):
    WEEKDAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'), 
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    block = models.ForeignKey(Block)
    weekday = models.IntegerField(choices = WEEKDAY_CHOICES)
    def wkday(self):
        return dict(Shift.WEEKDAY_CHOICES)[self.weekday]
    def __unicode__(self):
        return "{0} {1}".format( self.wkday(), self.block)

class ShiftEmployees(models.Model):
    period = models.ForeignKey(Period)
    shift = models.ForeignKey(Shift)
    employee = models.ForeignKey(Employee)
    def __unicode__(self):
        return "{0} in {1}".format(self.employee, self.shift)

class Log(models.Model):
    logout_at = models.TimeField('logout time',null=True)
    date = models.DateTimeField('log date')
    absent = models.BooleanField()
    shiftemployees = models.ForeignKey(ShiftEmployees)
    ordering = ['date']
    weeknumber = models.IntegerField('week number',null=True)
    def __unicode__(self):
        return "{0} in {1} at {2} ({3})".format(
            self.shiftemployees.employee,
            self.date.strftime("%Y-%m-%d"),
            self.date.strftime("%I:%M %p"),
            self.shiftemployees.shift.block
            )
    def status(self):
        T = self.shiftemployees.shift.block.start_at 
        fulldate = datetime.datetime(1,1,1,T.hour, T.minute, 0)
        late_limit = fulldate + datetime.timedelta(0,900)
        absent_limit = fulldate + datetime.timedelta(0,1800)
        if self.absent:
            return "Absent"
        else:
            if self.date.time() < late_limit.time():
                if not self.logout_at:
                    return "Ok + No Logout"
                else:
                    return "OK"
            else:
                if self.date.time() < absent_limit.time():
                    if not self.logout_at:
                        return "Late + No Logout"
                    else:
                        return "Late"
                else:
                    return "Absent"


