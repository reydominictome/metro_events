import ctypes
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404
from .forms import *
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
logged_user = {}

def Mbox(title, text, style):
    sty=int(style)+4096
    return ctypes.windll.user32.MessageBoxW(0, title, text, sty)

def prepareAdminNotifications(request_type):
    admin = Administrator.objects.all()

    if request_type == 'request_to_be_an_administrator':
        notif_title = "Request to be an administrator"
        notif_content = "A user requests to be an administrator."
        notif_type = "Request to be an Administrator"

        notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
        notif.save()

        for a in admin:
            user = User.objects.get(pk = a.admin.id)
            user.notification.add(notif.id)
    elif request_type == 'request_to_be_an_organizer':
        notif_title = "Request to be an organizer"
        notif_content = "A user requests to be an organizer"
        notif_type = "Request to be an Organizer"

        notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
        notif.save()

        for a in admin:
            user = User.objects.get(pk = a.admin.id)
            user.notification.add(notif.id)

def requestNotification(request_id, req_type):
    if req_type == 'administrator':
        request = Request.objects.get(pk = request_id)
        if request.isConfirmed == 1:
            notif_title = "Request Acceptance"
            notif_content = "Your request to be an administrator was accepted."
            notif_type = "Administrator response for administrator"

            notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
            notif.save()
    
            user = User.objects.get(pk = request.sender.id)
            user.notification.add(notif.id)
        elif request.isConfirmed == 0:
            notif_title = "Request was Declined"
            notif_content = "Your request to be an administrator was unfortunately declined."
            notif_type = "Administrator response for administrator"

            notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
            notif.save()
    
            user = User.objects.get(pk = request.sender.id)
            user.notification.add(notif.id)
    elif req_type == 'organizer':
        request = Request.objects.get(pk = request_id)
        if request.isConfirmed == 1:
            notif_title = "Request Acceptance"
            notif_content = "Your request to be an event organizer was accepted."
            notif_type = "Administrator response for organizer"

            notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
            notif.save()
    
            user = User.objects.get(pk = request.sender.id)
            user.notification.add(notif.id)
        elif request.isConfirmed == 0:
            notif_title = "Request was Declined"
            notif_content = "Your request to be an event organizer was unfortunately declined."
            notif_type = "Administrator response for organizer"

            notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
            notif.save()
    
            user = User.objects.get(pk = request.sender.id)
            user.notification.add(notif.id)
    elif req_type == 'Request to join event':
        request = EventRequest.objects.get(pk = request_id)
        if request.isConfirmed == 1:
            notif_title = "Request Acceptance"
            notif_content = "Your request join the event " + request.event.event_name + " was accepted."
            notif_type = "Organizer's Response"

            notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
            notif.save()
    
            user = User.objects.get(pk = request.sender.id)
            user.notification.add(notif.id)
        elif request.isConfirmed == 0:
            notif_title = "Request was Declined"
            notif_content = "Your request join the event " + request.event.event_name + " was unfortunately declined."
            notif_type = "Organizer's Response"

            notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
            notif.save()
    
            user = User.objects.get(pk = request.sender.id)
            user.notification.add(notif.id)

def newEventNotification(event_id):
    event = Event.objects.get(pk = event_id)
    user = User.objects.all()

    notif_title =  event.event_name
    notif_content = "A new event has been created. If you are interested go and check it out."
    notif_type = "New Event Announcement"

    notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
    notif.save()

    for u in user:
        u.notification.add(notif.id)

def notifyOrganizer(organizer, event_id):
    event = Event.objects.get(pk = event_id)

    notif_title =  event.event_name
    notif_content = "A user is interested in joining your event."
    notif_type = "Request to Join Event"

    notif = Notification(notif_title = notif_title, notif_content = notif_content, notif_type = notif_type)
    notif.save()

    organizer.organizer.notification.add(notif)


class MetroEventsIndexView(View):
    def get(self, request):
        if request.session.has_key('user'):
            del request.session['user']
        return render(request, 'webapp/Users.html')
    
    def post(self, request):
        if request.method == 'POST':
            if "btnRegister" in request.POST:
                form = RegistrationForm(request.POST)	
                data = request.POST

                password = data.get("password")
                cpassword = data.get("confirm_password")

                if password == cpassword:
                    email = data.get("email")
                    user = User.objects.all()
                    count = 0

                    for u in user:
                        if u.email == email:
                            count = 1

                    if count == 0:
                        username = data.get("username")
                        username_count = 0
                        for u in user:
                            if u.username == username:
                                username_count = 1
                        
                        if username_count == 0:
                            if form.is_valid():
                                firstname = data.get("first_name")
                                midname = data.get("middle_name")
                                lastname = data.get("last_name") 

                                form = User(first_name = firstname, middle_name = midname, last_name = lastname, 
                                    email = email, username = username, password = password)   
                                form.save()
                                form.password = make_password(form.password)
                                form.save()

                                messages.success(request, '<b>' + username + '</b> was registered successfully!')
                                return redirect('webapp:landing')
                                
                        messages.success(request, '<b>' + username + '</b> is in use!')
                        return redirect('webapp:home')

                    messages.success(request, '<b>' + email + '</b> is in use!')
                    return redirect('webapp:home')

                messages.success(request, 'Please make sure that the passwords are the same')
                return redirect('webapp:home')

            elif "btnLogin" in request.POST:   
                data = request.POST

                username = data.get("user_username")
                password = data.get("user_password")

                user = User.objects.all()    

                for u in user:
                    auth = check_password(password,u.password)

                    if auth == True and u.username == username:
                        admin = Administrator.objects.all()
                        isAdmin = 0
                        organizer = Organizer.objects.all()
                        isOrganizer = 0

                        for a in admin:
                            if u.id == a.admin.id:
                                isAdmin = 1
                                break
                        
                        for o in organizer:
                            if u.id == o.organizer.id:
                                isOrganizer = 1
                                break

                        context = {
                            'id': u.id,
                            'first_name': u.first_name,
                            'middle_name': u.middle_name,
                            'last_name': u.last_name,
                            'username': u.username,
                            'email': u.email,
                            'isAdmin': isAdmin,
                            'isOrganizer': isOrganizer,
                        }

                        print(isOrganizer)

                        request.session['user'] = context
                        return redirect('webapp:home')
                        
                print("cannot find btnLogin")
                messages.error(request,'username or password is incorrect')
                return redirect('webapp:landing')
                
        else:
            messages.success(request, 'Something went terribly wrong')
            return redirect('webapp:landing')

class MetroEventsHomeView(View):
    def get(self, request):
        if request.session.has_key('user'):
            user_id = int(request.session['user']['id'])
            user = User.objects.get(pk = user_id)

            notifs = user.notification.all()
            notifs_titles = []
            notifs_dates = []
            notifs_contents = []
            notifs_types = []

            for n in notifs:
                notifs_titles.append(n.notif_title)
                notifs_dates.append(n.notif_date)
                notifs_contents.append(n.notif_content)
                notifs_types.append(n.notif_type)

            return render(request, 'webapp/Home.html', {"notifs_titles":notifs_titles,
                                                        "notifs_dates":notifs_dates, 
                                                        "notifs_contents":notifs_contents,
                                                        "notifs_types": notifs_types})

        return redirect('webapp:landing')

    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnSendRequest' in request.POST:
                    form = RequestForm(request.POST)
                    data = request.POST

                    request_type = data.get("request_type")
                    description = data.get("description")
                    sender = data.get("sender")
                    sender = User.objects.get(pk = sender)
                    
                    requests = Request.objects.filter(sender = sender)
                    count = 0

                    for r in requests:
                        if r.sender == sender:
                            if r.isDeleted == 0:
                                if r.isPending == 1:
                                    if r.isConfirmed == 1:
                                        if r.request_type == request_type:
                                            count = 1
                    if count == 0: 
                        form = Request(description = description, request_type = request_type, sender = sender)
                        form.save()

                        prepareAdminNotifications(request_type)
                        return redirect('webapp:home')

                    print("redundant req")
                    return redirect('webapp:landing')
                print("btnRequest can't be found")
                return redirect('webapp:landing')
            print("No post")
            return redirect('webapp:landing')
        print("No session")
        return redirect('webapp:landing')

class MetroEventsEventsView(View):
    def get(self, request):
        if request.session.has_key('user'):
            events = Event.objects.all()

            return render(request, 'webapp/EventList.html', {"events":events})

        return redirect('webapp:landing')
    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnJoin' in request.POST:
                    data = request.POST
                    user_id = data.get("user_id")
                    event_id = data.get("event_id")

                    event = Event.objects.get(pk = event_id)
                    for u in event.organizer.all():
                        organizer = u

                    user = User.objects.get(pk = user_id)

                    description = "I want to join your event " + event.event_name
                    request_type = "Request to join event"
                    sender = user

                    req = EventRequest.objects.create(event = event)
                    req.save()
                    update = EventRequest.objects.filter(id = req.id).update(description=description, 
                                                                    request_type = request_type, sender = sender)
                    organizer.request.add(req)

                    notifyOrganizer(organizer, event_id)

                    return redirect('webapp:events')
                elif 'btnUpvote' in request.POST:
                    data = request.POST
                    event_id = data.get("event_id")

                    update = Event.objects.get(pk = event_id)
                    update.number_of_upvotes = update.number_of_upvotes + 1
                    update.save()

                    return redirect('webapp:events')
        return redirect('webapp:landing')

class MetroEventsEventsRegistrationView(View):
    def get(self, request):
        if request.session.has_key('user'):

            return render(request, 'webapp/RegisterEvent.html')
        return redirect('webapp/landing')
    
    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnCreate' in request.POST:
                    form = EventCreationForm(request.POST)
                    data = request.POST

                    if form.is_valid():
                        organizer = data.get("organizer")
                        event_name = data.get("event_name")
                        event_description = data.get("event_description")
                        event_type = data.get("event_type")
                        event_fee = data.get("event_fee")
                        start_date = data.get("start_date")
                        end_date = data.get("end_date")
                        start_time = data.get("start_time")
                        end_time = data.get("end_time")

                        user = User.objects.get(pk = organizer)
                        event_organizer = Organizer.objects.get(organizer = user)
                        form = Event(event_name = event_name,
                                    event_description = event_description,
                                    event_type = event_type,
                                    event_fee = event_fee,
                                    start_date = start_date,
                                    end_date = end_date, 
                                    start_time = start_time,
                                    end_time = end_time)
                        form.save()
                        events = Event.objects.get(pk = form.id)
                        event_organizer.events.add(events)

                        event_id = Event.objects.get(pk = form.id).pk

                        newEventNotification(event_id)

                        return redirect('webapp:organizer_requests')
        return redirect('webapp:landing')

class MetroEventsAdministratorView(View):
    def get(self, request):
        if request.session.has_key('user'):
            requests = Request.objects.all()

            return render(request, 'webapp/Request.html', {"requests":requests})

        return redirect('webapp:landing')

    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnDelete' in request.POST:
                    request_id = request.POST.get("request_id")

                    update = Request.objects.filter(id = request_id).update(isDeleted=True)
                    update = Request.objects.filter(id = request_id).update(isPending=False)
                    print(update)

                    return redirect('webapp:administrator')
                elif 'btnAccept' in request.POST:
                    request_id = request.POST.get("request_id")

                    request = Request.objects.get(pk = request_id)
                    user = User.objects.get(pk = request.sender.id)

                    if request.request_type == 'request_to_be_an_administrator':
                        admin = Administrator.objects.create()
                        admin.save()
                        admin_update = Administrator.objects.filter(id = admin.id).update(admin=user)
                        req_type = "administrator"
                    elif request.request_type == 'request_to_be_an_organizer':
                        organizer = Organizer.objects.create()
                        organizer.save()
                        organizer_update = Organizer.objects.filter(id = organizer.id).update(organizer=user)
                        req_type = "organizer"

                    update = Request.objects.filter(id = request_id).update(isConfirmed=True)
                    update = Request.objects.filter(id = request_id).update(isPending=False)

                    requestNotification(request_id, req_type)

                    return redirect('webapp:administrator')
                elif 'btnDecline' in request.POST:
                    request_id = request.POST.get("request_id")

                    request = Request.objects.get(pk = request_id)
                    update = Request.objects.filter(id = request_id).update(isPending=False)
                    update = Request.objects.filter(id = request_id).update(isConfirmed=False)

                    if request.request_type == 'request_to_be_an_administrator':
                        req_type = "administrator"
                    elif request.request_type == 'request_to_be_an_organizer':
                        req_type = "organizer"

                    requestNotification(request_id, req_type)

                    return redirect('webapp:administrator')
                return redirect('webapp:landing')
            return redirect('webapp:landing')
        return redirect('webapp:landing')
    
class MetroEventsAdministratorUsersView(View):
    def get(self, request):
        if request.session.has_key('user'):
            users = User.objects.all()

            return render(request, 'webapp/AllUsers.html', {"user":users})

        return redirect('webapp:landing')

    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnDelete' in request.POST:
                    request_id = request.POST.get("request_id")

                    update = Request.objects.filter(id = request_id).update(isDeleted=True)

                    return redirect('webapp:administrator')
                return redirect('webapp:landing')
            return redirect('webapp:landing')
        return redirect('webapp:landing')
    
class MetroEventsAdministratorEventsView(View):
    def get(self, request):
        if request.session.has_key('user'):
            events = Event.objects.all()

            return render(request, 'webapp/AllEvents.html', {"events":events})

        return redirect('webapp:landing')

    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnDelete' in request.POST:
                    request_id = request.POST.get("request_id")

                    update = Request.objects.filter(id = request_id).update(isDeleted=True)

                    return redirect('webapp:administrator')
                return redirect('webapp:landing')
            return redirect('webapp:landing')
        return redirect('webapp:landing')


class MetroEventsOrganizerView(View):
    def get(self, request):
        if request.session.has_key('user'):
            user_id = int(request.session['user']['id'])
            user = User.objects.get(pk = user_id)

            for u in user.user_organizer.all():
                organizer = u

            return render(request, 'webapp/OrganizedEvents.html', {"organizer":organizer})

        return redirect('webapp:landing')

    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnDelete' in request.POST:
                    form = EventCreationForm(request.POST)
        return redirect('webapp/landing') 

class MetroEventsOrganizerRequestsView(View):
    def get(self, request):
        if request.session.has_key('user'):
            user_id = int(request.session['user']['id'])
            user = User.objects.get(pk = user_id)

            for u in user.user_organizer.all():
                organizer = u

            return render(request, 'webapp/OrganizerRequests.html', {"organizer":organizer})

        return redirect('webapp:landing')

    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnAccept' in request.POST:
                    request_id = request.POST.get("request_id")
                    event_id = request.POST.get("event_id")

                    request = EventRequest.objects.get(pk = request_id)
                    user = User.objects.get(pk = request.sender.id)
                    event = Event.objects.get(pk = event_id)

                    req_type = request.request_type

                    update = EventRequest.objects.filter(id = request_id).update(isConfirmed=True)
                    update = EventRequest.objects.filter(id = request_id).update(isPending=False)

                    event.participants.add(user)
                    event.number_of_participants = event.number_of_participants + 1
                    event.save()

                    requestNotification(request_id, req_type)

                    return redirect('webapp:organizer_requests')
                elif 'btnDecline' in request.POST:
                    request_id = request.POST.get("request_id")

                    request = EventRequest.objects.get(pk = request_id)
                    update = EventRequest.objects.filter(id = request_id).update(isPending=False)
                    update = EventRequest.objects.filter(id = request_id).update(isConfirmed=False)

                    req_type = request.request_type

                    requestNotification(request_id, req_type)

                    return redirect('webapp:organizer_requests')

        return redirect('webapp/landing')    

class MetroEventsNotificationsView(View):
    def get(self, request):
        if request.session.has_key('user'):
            user_id = int(request.session['user']['id'])
            user = User.objects.get(pk = user_id)

            return render(request, 'webapp/AllNotifications.html', {"user": user})

        return redirect('webapp:landing')

    def post(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                if 'btnDelete' in request.POST:
                    form = EventCreationForm(request.POST)
        return redirect('webapp/landing')           