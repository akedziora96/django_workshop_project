import datetime


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from conference_room_app.models import Room, Reservation


class SearchRoom(View):

    def get(self, request):
        room_name = request.GET.get('room_name', '')
        room_capacity = 0 if request.GET.get('room_capacity', '0') == '' else int(request.GET.get('room_capacity', '0'))
        is_projector = request.GET.get('is_projector', '')

        rooms = Room.objects.order_by('capacity').filter().exclude(reservation__date=datetime.date.today())
        rooms = rooms.filter(name__icontains=room_name)
        rooms = rooms.filter(capacity__gte=room_capacity)
        if is_projector == 'True' or is_projector == 'False':
            rooms = rooms.filter(projector=is_projector)
        if not rooms.exists():
            return HttpResponse("Brak dostępnych sal o podanych parametrach.")
        return render(request, 'base.html', {'rooms': rooms})

class AddRoom(View):

    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        room_name = request.POST.get('room_name')
        room_capacity = 0 if request.POST.get('room_capacity') == '' else int(request.POST.get('room_capacity'))
        is_projector = request.POST.get('is_projector')

        if not room_name:
            return HttpResponse("Nie podano nazwy sali")
        if room_capacity <= 0:
            return HttpResponse("Podano złą pojemność")
        if Room.objects.filter(name=room_name).exists():
            return HttpResponse("Sala o podanej nazwie juz istnieje w systemie")

        Room.objects.create(name=room_name, capacity=room_capacity, projector=is_projector)
        return redirect('/')


class DisplayRooms(View):

    def get(self, request):
        rooms = Room.objects.all().order_by('capacity')
        return render(request, 'display_rooms.html', {'rooms': rooms })


class DeleteRoom(View):

    def get(self, request, room_id):
        Room.objects.get(id=room_id).delete()
        return redirect('/rooms/')


class EditRoom(View):

    def get(self, request, room_id):
        edited_room = Room.objects.get(id=room_id)
        return render(request, 'edit_room.html', {'edited_room': edited_room})

    def post(self, request, room_id):
        edited_room = Room.objects.get(id=room_id)

        room_new_name = request.POST.get('room_new_name')
        room_new_capacity = request.POST.get('room_new_capacity')
        room_new_capacity = 0 if room_new_name == '' else int(room_new_capacity)
        is_projector_new = request.POST.get('is_projector_new')

        if not room_new_name:
            return HttpResponse("Nie podano nazwy sali")
        if room_new_capacity <= 0:
            return HttpResponse("Podano złą pojemność")
        if Room.objects.filter(name=room_new_name).first() and room_new_name != edited_room.name:
            return HttpResponse("Sala o podanej nazwie juz istnieje w systemie")

        edited_room.name = room_new_name
        edited_room.capacity = room_new_capacity
        edited_room.projector = is_projector_new
        edited_room.save()
        return redirect('/rooms/')


class ReserveRoom(View):

    def get(self, request, room_id):
        room_to_reserve = Room.objects.get(id=room_id)
        room_reservations = room_to_reserve.reservation_set.all().order_by('date')
        return render(
                        request, 'reserve_room.html',
                        {'room_to_reserve': room_to_reserve, 'room_reservations': room_reservations}
                     )

    def post(self, request, room_id):
        room_to_reserve = Room.objects.get(id=room_id)
        date = request.POST.get('date')
        comment = request.POST.get('comment')

        if date < str(datetime.date.today().isoformat()):
            return HttpResponse("Data jest z przeszłości")
        if Reservation.objects.filter(room_id=room_to_reserve, date=date).first():
            return HttpResponse("W podanym dniu sala jest już zarezerwowana")

        Reservation.objects.create(room_id=room_to_reserve, date=date, comment=comment)
        return redirect('/rooms/')


class RoomDetails(View):

    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room_reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, 'room_details.html', {'room': room, 'room_reservations': room_reservations})