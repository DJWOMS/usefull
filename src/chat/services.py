from rest_framework import exceptions

from src.chat.models import Room
from src.profiles.models import Profile
from src.team.models import TeamMember


def create_room(request):
    """ Creating new room and add members """
    member1 = Profile.objects.get(id=request.user.id)
    member2 = Profile.objects.get(id=request.data.get("member"))
    if not Room.objects.filter(member=member1).filter(member=member2).exists():
        new_room = Room.objects.create(name=f'{member1} + {member2}', user=member1)
        new_room.member.add(member1, member2)
        new_room.save()
    else:
        raise exceptions.APIException(detail='Chat already created')


# def create_team_room(request):
#     """ Creating new room and add members of team """
#     if not Room.objects.filter(user=request.user, team=request.data.get('team')).exists():
#         new_room = Room.objects.create(user=request.user, team=request.data.get('team'))
#         new_room.member.add(*TeamMember.objects.filter(team=request.data.get('team')))
#         new_room.save()
#     else:
#         raise exceptions.APIException(detail='Chat already created')
