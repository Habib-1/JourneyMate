from django.shortcuts import render
from JMapp.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from core.forms import MessageForm
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os


# Create your views here.
def home(request):
    return render(request, 'home.html')

def SearchTrain(request):
    if request.method == 'GET':
        departure = request.GET.get('departure')
        destination = request.GET.get('destination')
        date = request.GET.get('date')
       
        if departure and destination and date:
            trains = Train_route.objects.filter(station__station_name=departure).filter(station__station_name=destination).filter(available_date=date)
            schedules = Schedule.objects.filter(start_station__station_name__iexact=departure).filter(end_station__station_name__iexact=destination)
            context = {
                'trains': trains,
                'schedules': schedules,
                'date': date,
                'departure':departure,
                'destination' : destination,
            }
            return render(request, 'search_results.html', context)
        return HttpResponse("Invalid input. Please fill all fields.")

def SeatPlan(request):
    if request.method == 'GET':
        selected_train = request.GET.get('selectTrain')
        date = request.GET.get('date')
        departure=request.GET.get('departure')
        destination=request.GET.get('destination')
        seats = Seat.objects.filter(train__train_name__iexact=selected_train, date=date)
        context = {
            'seats': seats,
            'departure' : departure,
            'destination' : destination,
            'date' : date,
            'train' :selected_train,
        }
      
        return render(request, 'available_seat.html', context)



def train_info(request):
    schedules=Schedule.objects.all()
    context={
        'schedules':schedules
    }
    return render(request,'train_info.html',context)

def contact_us(request):
    if request.method =='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Message send successful")
            return redirect('home')
        
    else:
        form=MessageForm()
       
    return render(request,'contact.html',{'form':form})

def BuyTicket(request):
    if request.method == "POST":
        selected_seats = request.POST.get('selected_seats', '')  # Get comma-separated string
        selected_seats_list = selected_seats.split(',') if selected_seats else [] 
         # Convert to list
        total_seat = len(selected_seats_list)
        train = request.POST.get('train')
        date = request.POST.get('date')
        departure = request.POST.get('departure')
        destination = request.POST.get('destination')
        
        try:
            fare = Fare.objects.get(
                train__train_name=train,
                start_station__station_name=departure,
                end_station__station_name=destination,
            )
        except ObjectDoesNotExist:
            fare = None
           
        except MultipleObjectsReturned:
            fare = None
      
        total_fare=total_seat * fare.fare_amount
        context = {
            'selected_seats': selected_seats_list,
            'departure': departure,
            'destination': destination,
            'date': date,
            'train': train,
            'fare': fare,
            'total_fare': total_fare,
        }
        
        return render(request, 'ticket_details.html', context)
    

@login_required(login_url='login')
def ticket(request):
    if request.method == "POST":
        train = request.POST.get('train')
        date = request.POST.get('date')
        departure = request.POST.get('departure')
        destination = request.POST.get('destination')
        seats = request.POST.getlist('seats')  # Use getlist to fetch multiple seat values
        seat = ','.join(seats)  
        total_fare = request.POST.get('total_fare')
        
        try:
            schedule = Schedule.objects.get(
                train__train_name=train,
                start_station__station_name=departure,
                end_station__station_name=destination,
            )
            start_time = schedule.start_time
        except ObjectDoesNotExist:
            start_time = None
        except MultipleObjectsReturned:
            start_time = None
        
        # Iterate through the seat list and print each element
        
        
        Ticket.objects.create(
            user=request.user,
            train_name=train,
            departure=departure,
            arrival=destination,
            journey_date=date,
            start_time=start_time,
            seats=seat,
            total_fare=total_fare,
        )
        context={
           'train_name':train,
            'departure':departure,
            'arrival' :destination,
            'journey_date' :date,
            'start_time':start_time,
            'seats':seat,
            'total_fare' : total_fare,
       }
        
        actual_list = eval(seats[0])
        for s in actual_list:
            seats = Seat.objects.filter(
                train__train_name=train,
                date=date,
                seat_number=s,
                is_available=True,
            )
            for seat in seats:
                seat.is_available = False
                seat.save()

        return render(request, 'ticket.html',context)
    

@login_required(login_url='login')
def generate_ticket_pdf(request):
    if request.method == "POST":
        first_name=request.POST.get('user_first_name') 
        last_name=request.POST.get('user_last_name')
        phone_number=request.POST.get('user_phone_number')
        email=request.POST.get('user_email')
        train = request.POST.get('train_name')
        date = request.POST.get('journey_date')
        start_time = request.POST.get('start_time')
        departure = request.POST.get('departure')
        destination = request.POST.get('arrival')
        seats = request.POST.getlist('seats') 
        seat = ', '.join(seats)  
        total_fare = request.POST.get('total_fare')
        
        try:
            schedule = Schedule.objects.get(
                train__train_name=train,
                start_station__station_name=departure,
                end_station__station_name=destination,
            )
            start_time = schedule.start_time
        except ObjectDoesNotExist:
            start_time = "Not Available"
        except MultipleObjectsReturned:
            start_time = "Multiple Schedules Found"

        # Context for HTML Template
        context = {
            'first_name':first_name,
            'last_name':last_name,
            'phone_number':phone_number,
            'email':email,
            'train_name': train,
            'departure': departure,
            'arrival': destination,
            'journey_date': date,
            'start_time': start_time,
            'seats': seat,
            'total_fare': total_fare,
        }
        print(context)
        # Render HTML Template
        html = render_to_string('pdf.html', context)
        print(html)  # Debugging HTML Content

        # Create PDF Response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            print(pisa_status.err)  # Debugging Errors
            return HttpResponse('PDF creation failed. Please try again.', content_type='text/plain')
        
        return response
    
    return HttpResponse('Invalid request method. Use POST instead.', content_type='text/plain')
