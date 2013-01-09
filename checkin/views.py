from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext
from checkin.models import Log, Shift, Period, Employee, Block, ShiftEmployees
from django.core.urlresolvers import reverse
import datetime
from datetime import date
import time
# Create your views here.

def checkin(request):
  #gets the period
    try:
        P = Period.objects.filter(start_at__lte=date.today()).filter(end_at__gte=date.today())[0]
    except IndexError:
        P = None
    D = date.today().weekday()+1 #Gets Weekday
    T = datetime.time(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec) #Localtime
    B = Block.objects.filter(start_at__lte=T).filter(end_at__gte=T)#Block according to localtime
    if B:
        S = Shift.objects.filter(weekday=D).filter(block=B[0]) #Gets the actual shift
        if S:
            S = S[0]
        else:
            template = loader.get_template('noshifts.html')
            c = RequestContext(request,{})
            return HttpResponse(template.render(c))
        #get employees in the shift
        SE = ShiftEmployees.objects.filter(shift=S).filter(period=P)
        try:
            L = Log.objects.filter(date__gte=date.today()).filter(shiftemployees__in = SE)
        except:
            L = []
        if len(L):
          emps = L.values('shiftemployees')
        else:
          emps = []
        
        Lless = SE.exclude(id__in = emps) 
        
        #10 minute interval for checkout
        fulldate = datetime.datetime(1,1,1,B[0].end_at.hour, B[0].end_at.minute, 0)
        fulldate2 = fulldate + datetime.timedelta(0,-600)
        fulldate2.time()
        Lgout=False
        if fulldate2.time() < T:
            Lgout=True        

        template = loader.get_template('index.html')
        c = RequestContext(request, {
            'Shift': S,
            'ShiftEmployees': SE,
            'Logs': L,
            'Logless': Lless,
            'logout_time': Lgout,
            })
        return HttpResponse(template.render(c))
    else:
        template = loader.get_template('noshifts.html')
        c = RequestContext(request,{})
        return HttpResponse(template.render(c))
    endif

def log(request):
    L = Log.objects.all().order_by('-weeknumber','date')
    template = loader.get_template('log.html')
    c = Context({
        'Log': L,
        })
    return HttpResponse(template.render(c))
def check(request):
    try:
        S = Shift.objects.filter(id=request.POST['shft'])
        P = Period.objects.filter(start_at__lte=date.today()).filter(end_at__gte=date.today())[0]
        E = Employee.objects.filter(id=request.POST['emp'])
        SE = ShiftEmployees.objects.get(shift=S,employee=E,period=P)
        L = Log(shiftemployees=SE, date=datetime.datetime.now(), absent=False)
	day = datetime.datetime.now()
	b = S[0].block
	Sdate = datetime.datetime(day.year, day.month, day.day,b.start_at.hour,b.start_at.minute,0)
        Edate = datetime.datetime(day.year, day.month, day.day,b.end_at.hour,b.end_at.minute,0)
        if not Log.objects.filter(shiftemployees=SE, absent=False, date__range=(Sdate,Edate)):
            L. weeknumber = L.date.isocalendar()[1]
    	    L.save()
    except (KeyError, Shift.DoesNotExist):
        return HttpResponseRedirect(reverse('checkin.views.checkin'))
    else:
        return HttpResponseRedirect(reverse('checkin.views.checkin'))

def uncheck(request):
    try:
        S = Shift.objects.filter(id=request.POST['shft'])
        P = Period.objects.filter(start_at__lte=date.today()).filter(end_at__gte=date.today())[0]
        E = Employee.objects.filter(id=request.POST['emp'])
        SE = ShiftEmployees.objects.get(shift=S,employee=E,period=P)
        L = Log.objects.filter(date__gte=date.today()).filter(shiftemployees=SE)[0]#gets today's shift
        L.logout_at=datetime.datetime.now()
        L.save()
    except (KeyError, Shift.DoesNotExist):
        return HttpResponseRedirect(reverse('checkin.views.checkin'))
    else:
        return HttpResponseRedirect(reverse('checkin.views.checkin'))

def absences(request):
    #since beggining of period till now: find absences and create absent logs
    P = Period.objects.filter(start_at__lte=date.today()).filter(end_at__gte=date.today())
    B = Block.objects.all()
    S = Shift.objects.all()
    L = Log.objects.all()
    difference = (datetime.datetime.now() - P[0].start_at).days
    start_day = datetime.datetime(P[0].start_at.year, P[0].start_at.month, P[0].start_at.day,0,0,0)
    for d in range(difference+1):
        day = start_day + datetime.timedelta(d)
        if day.weekday() < 5: #if its a week day
            for b in B:
                s = S.filter(block=b).get(weekday=day.weekday()+1)
                SE = ShiftEmployees.objects.filter(shift=s).filter(period=P[0])
                Adate = datetime.datetime(day.year, day.month, day.day,b.start_at.hour,b.start_at.minute,0)
                Ndate = datetime.datetime(day.year, day.month, day.day,b.end_at.hour,b.end_at.minute,0)
                for se in SE:
                    if not L.filter(date__range=(Adate,Ndate)).filter(shiftemployees=se): #if the log for that block  in the day wasnt created
                        Lnew = Log(shiftemployees=se, date=Ndate, absent=True, weeknumber=Ndate.isocalendar()[1])
                        Lnew.save()
    return HttpResponseRedirect(reverse('checkin.views.log'))

def schedule(request):
    #gets the period

    blocks = _schedule()
    if schedule == None:
        return HttpResponse(loader.get_template ('no-schedule.html').render(Context(None)))
    else:
        template = loader.get_template('schedule.html')
        return HttpResponse(template.render(Context({'blocks': blocks})))

def _schedule():
  #gets the period
    periods = Period.objects.filter(
        start_at__lte=date.today()).filter(end_at__gte=date.today())

    if periods.count() == 0:
        return None
    
    blocks = Block.objects.all().order_by('start_at')
    all_shift_employees = [item for sublist in 
            [period.shiftemployees_set.all() for period in periods]
            for item in sublist] # plain list of every shiftEmployee in every active period
    
    for b in blocks:
        b.schedule = []
        shifts_in_block = [shift for shift in all_shift_employees if shift.shift.block == b]
        for d in range(0, 6):
            b.schedule.append([])
            b.schedule[d] = [shift.employee.name for shift in shifts_in_block if shift.shift.weekday == d + 1]

    for b in blocks:
        print b.schedule
    return [b for b in blocks]

