from venv import logger
from django.shortcuts import render
from.models import *
from django.shortcuts import redirect
from.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse


from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

import requests
from datetime import datetime
from django.shortcuts import render
from .models import ClientTestimonial
from .forms import TestimonialForm
from django.shortcuts import render
from django.shortcuts import render
from .models import Owner_work
from django.shortcuts import render
from .models import Owner_work
from .forms import OwnerWorkForm
from .models import Owner_work
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Owner_work, Bookmark








@login_required
def owner(request):
    usr = request.user

    all_booked = Booked.objects.filter(b_Owner=request.user)
    b_wrk = Booked.objects.filter(b_Owner=usr)

    return render (request,'owner.html',{'b_work':b_wrk,'allb':all_booked})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid(): 
                form.save();
                username = form.cleaned_data.get('username')
                usr = User.objects.filter(username=username).first()
                if username.isdigit():
                    worker(user=usr,contact=username).save()
                else:
                    usr.email = username
                    usr.save()
                    worker(user=usr).save()
                messages.success(request, f'Account is Created for {username}')
                return redirect('signup_worker')
        else:
            form = UserRegisterForm()
    return render(request, 'signup.html', {'form':form, 'title':'Sign Up'})


def register_owner(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = OwnerRegisterForm(request.POST)
            if form.is_valid():
                form.save();
                username = form.cleaned_data.get('username')
                usr = User.objects.filter(username=username).first()
                usr.is_staff = True
                usr.save()
                if username.isdigit():
                    Owner(user=usr,contact=username).save()
                else:
                    usr.email = username
                    usr.save()
                    Owner(user=usr).save()
                messages.success(request, f'Account is Created for {username}')
                return redirect('signup')
        else:
            form = OwnerRegisterForm()
    return render(request, 'register_owner.html', {'form':form, 'title':'Sign Up'})



@login_required
def account_settings(request):
    if request.user.is_staff:
        return redirect("owner")
    else:
        if request.method == 'POST':
            # User Details Update
            s_form = UpdateUserDetailForm(request.POST, request.FILES, instance=request.user.worker)
            u_form = UserUpdateForm(request.POST, instance=request.user)

            if s_form.is_valid() and u_form.is_valid():
                s_form.save()
                u_form.save()
                print('success')
                messages.success(request, f'Your Account has been Updated!')
                return redirect("account_settings")
            else:
                messages.error(request, 'Please correct the error ')
            # Change Password
            pass_change_form = PasswordChangeForm(request.user, request.POST)
            if pass_change_form.is_valid():
                user = pass_change_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('worker')
            else:
                messages.error(request, 'Please correct the error below.')

        else:
            s_form = UpdateUserDetailForm(instance=request.user.worker)
            u_form = UserUpdateForm(instance=request.user)
            pass_change_form = PasswordChangeForm(request.user)
        detl = {
            'u_form': u_form,
            's_form': s_form,
            'pass_change_form': pass_change_form,
            'title': 'User Account Settings',
        }
        return render(request, 'work_account.html', detl)


def get_work(request):
    all_booked = Booked.objects.filter(b_Owner=request.user)
    print(all_booked)
    return render(request, 'booked.html',{'allb':all_booked})


@login_required
def booked_single(request, id):

    if request.method == "POST":
        wkt = request.POST.get('work_type')
        ownam = request.POST.get('person_name')
        wrk_id = request.POST.get('worker_id')
        workernm = request.user

        apply = Booked(b_woker=workernm, b_Owner=ownam, b_work=wkt,b_woker_id=wrk_id)
        apply.save()

    all_b = Booked.objects.all()

    bkd = Owner_work.objects.filter(id=id)
    all_w = str(request.user.id)
    return render(request, 'single_booked.html', {'work': bkd[0],'all_b':all_b,'w':all_w})





def worker_single(request,id):
    b_wrk = Booked.objects.filter(id=id)
    return render(request, 'single_worker_booked.html', {'work': b_wrk[0]})

########start email here
@login_required
def worker_action(request):

    if request.method == 'GET':
        wrk_id = request.GET.get('act')
        st = request.GET.get('st')
        if st == 'Accept':
            o = Booked.objects.filter(id=wrk_id).first()
            o.action = 'Accept'
            o.save()
        if st == 'Reject':
            o = Booked.objects.filter(id=wrk_id).first()
            o. action = 'Reject'
            o.save()
    return render(request, 'owner.html')

# from django.core.mail import send_mail
# from django.core.mail import send_mail

# def worker_action(request):
#     if request.method == 'GET':
#         wrk_id = request.GET.get('act')
#         st = request.GET.get('st')
#         if st == 'Accept':
#             o = Booked.objects.filter(id=wrk_id).first()
#             o.action = 'Accept'
#             o.save()

#             # Sending email when accepted
#             subject = 'Your Booking Request Has Been Accepted'
#             message = 'Dear {},\n\nWe are pleased to inform you that your booking request has been accepted.\n\nThank you for choosing our services!\n\nBest regards,\nYour Company Name'.format(o.client_name)
#             from_email = 'your_company@example.com'
#             recipient_list = [o.client_email]
#             send_mail(subject, message, from_email, recipient_list)

#         if st == 'Reject':
#             o = Booked.objects.filter(id=wrk_id).first()
#             o.action = 'Reject'
#             o.save()

#             # Sending email when rejected
#             subject = 'Your Booking Request Has Been Rejected'
#             message = 'Dear {},\n\nWe regret to inform you that your booking request has been rejected.\n\nThank you for considering our services.\n\nBest regards,\nYour Company Name'.format(o.client_name)
#             from_email = 'your_company@example.com'
#             recipient_list = [o.client_email]
#             send_mail(subject, message, from_email, recipient_list)

#     return render(request, 'owner.html')


####end email here

@login_required
def worker_profile(request,id):

    worker_pro = worker.objects.filter(user_id=id)
    return render(request, 'worker_profile.html', {'worker': worker_pro[0]})


@login_required
def my_profile(request,id):

    worker_pro = worker.objects.filter(user_id=id)
    return render(request, 'worker_profile.html', {'worker': worker_pro[0]})

@login_required
def accept_work(request):
    accept_wrk = Booked.objects.filter(b_woker_id=request.user.id)
    return render(request, 'accept_worked.html', {'worker': accept_wrk})


def home(request):
    if request.user.is_staff:
        usr = request.user

        all_booked = Booked.objects.filter(b_Owner=request.user)
        b_wrk = Booked.objects.filter(b_Owner=usr)

        return render(request, 'owner.html', {'b_work': b_wrk, 'allb': all_booked})
    else:
        all_wo = Owner_work.objects.all()
        accept_wrk = Booked.objects.filter(b_woker_id=request.user.id)
        return render(request, 'home.html', {'all_wo': all_wo,'worker': accept_wrk})

@login_required
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def notify_telegram(person_name, desc, work_type, time, place, charge_per_day, experience_level, vacancies, applicants_needed, deadline, bot_token, chat_id):
    message = f"""
    New job posted!

    Person Name: {person_name}
    Description: {desc}
    Work Type: {work_type}
    Time: {time}
    Place: {place}
    Charge per Day: {charge_per_day}
    Experience Level: {experience_level}
    Vacancies: {vacancies}
    Applicants Needed: {applicants_needed}
    Deadline: {deadline.strftime('%Y-%m-%d')}
    """

    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": str(chat_id),
        "text": message
    }
    response = requests.post(telegram_api_url, data=data)
    # Check if the message was sent successfully
    if response.status_code != 200:
        print("Failed to send notification to Telegram.")
        print(response.json())
    else:
        print("Notification sent successfully.")




# def job_post(request):
#     if request.user.is_staff:
#         if request.method == 'POST':
#             person_name = request.POST.get('person_name')
#             desc = request.POST.get('desc')
#             work_type = request.POST.get('work_type')
#             time = request.POST.get('time')
#             place = request.POST.get('place')
#             charge_per_day = request.POST.get('charge_per_day')
#             job = Owner_work.objects.create(person_name=person_name, work_dec=desc, work_type=work_type, time=time, place=place,
#                                             pay_for_work=charge_per_day)
            
#             bot_token = '6237939466:AAHxB6WdRQ14g9o_5oWD-JyV_qZ4tQG8QyE'
#             chat_id = '-1001972802427'

#             #bot_token = '6127184828:AAFbZuMr33t5pjipM8jHC098n5cv2NaS6lM'
#             #chat_id = '-1001942597050'
#             notify_telegram(person_name, desc, work_type, time, place, charge_per_day, bot_token, chat_id)
             
#             job.save()
            
#         all_work = work.objects.all()
#         return render(request, 'post_jobs.html', {'work': all_work})
#     else:
#          return render(request, 'home.html')


@login_required
def job_post(request):
    if request.user.is_staff:
        if request.method == 'POST':
            person_name = request.POST.get('person_name')
            desc = request.POST.get('desc')
            work_type = request.POST.get('work_type')
            time = request.POST.get('time')
            place = request.POST.get('place')
            charge_per_day = request.POST.get('charge_per_day')
            
            experience_level = request.POST.get('experience_level')
            vacancies = int(request.POST.get('vacancies'))
            applicants_needed = request.POST.get('applicants_needed')
            deadline = datetime.strptime(request.POST.get('deadline'), "%Y-%m-%d").date()

            job = Owner_work.objects.create(
                person_name=person_name, 
                work_dec=desc, 
                work_type=work_type, 
                time=time, 
                place=place,
                pay_for_work=charge_per_day,
                experience_level=experience_level,
                vacancies=vacancies,
                applicants_needed=applicants_needed,
                deadline=deadline
            )
            
            bot_token = '6237939466:AAHxB6WdRQ14g9o_5oWD-JyV_qZ4tQG8QyE'
            chat_id = '-1001972802427'
            
            notify_telegram(
                person_name, 
                desc, 
                work_type, 
                time, 
                place, 
                charge_per_day,
                experience_level,
                vacancies,
                applicants_needed,
                deadline,
                bot_token, 
                chat_id
            )
             
            job.save()
            
        all_work = work.objects.all()
        return render(request, 'post_jobs.html', {'work': all_work})
    else:
         return render(request, 'home.html')

#######end hear

 

        
##search
def search(request):
    query = request.GET.get('query','')
    qu = request.GET.get('query1','')
    print("qr",query)
    job = []
    for jb in [i for i in Owner_work.objects.all()]:
        if query.lower() in jb.work_type.lower() and qu.lower() in jb.place.lower():
            job.append(jb)
    params = {
        'job':job,


        }
    print(params)
    return render(request, 'find_job.html', params)


#views.py

@login_required
def posted_jobs(request):
    # Fetch all the posted jobs
    all_jobs = Owner_work.objects.all()
    return render(request, 'posted_job.html', {'all_jobs': all_jobs})




#Update View
def job_update(request, job_id):
    job = get_object_or_404(Owner_work, id=job_id)
    if request.method == "POST":
        form = OwnerWorkForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('posted_jobs') 
    else:
        form = OwnerWorkForm(instance=job)
    return render(request, 'job_update.html', {'form': form})

#Delete View
def job_delete(request, job_id):
    job = get_object_or_404(Owner_work, id=job_id)
    if request.method == "POST":
        job.delete()
        return redirect('posted_jobs')
    return render(request, 'job_delete_confirm.html', {'job': job})


#####bookmarked job view



@login_required
def add_bookmark(request, job_id):
    job = get_object_or_404(Owner_work, id=job_id)
    Bookmark.objects.get_or_create(user=request.user, job=job)
    return redirect('home')  # assuming you have a job_detail view

@login_required
def remove_bookmark(request, job_id):
    job = get_object_or_404(Owner_work, id=job_id)
    Bookmark.objects.filter(user=request.user, job=job).delete()
    return redirect('bookmarked_jobs')

@login_required
def bookmarked_jobs(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'bookmarked_jobs.html', {'bookmarks': bookmarks})

#####end hear

##about section
def about(request):
    return render(request, 'about.html')
def empty_view(request):
    return HttpResponse(status=204)
##job applicants

def job_applicants(request):
    # Assume 'allb' is a list of worker objects fetched from the database
    allb = Booked.objects.all()
    return render(request, 'job_applicants.html', {'allb': allb})



def testimonials(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = TestimonialForm()
    testimonials = ClientTestimonial.objects.all()
    return render(request, 'testimonials.html', {'form': form, 'testimonials': testimonials})
