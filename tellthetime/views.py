# Create your views here.
from datetime import datetime
from django.http import HttpResponse

def get_time(request):

    def httpdate(dt):
        """Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d" % (weekday, dt.day, month,
            dt.year, dt.hour, dt.minute, dt.second)

    now = httpdate(datetime.now())
    if 'CONTENT_TYPE' in request.META and request.META['CONTENT_TYPE'] == 'application/json':
        return HttpResponse('{"time": {0}}'.format(now))
    return HttpResponse(now)

