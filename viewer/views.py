from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from venv.Planner.models import Meeting, MeetingMinute
from venv.Planner.forms import MeetingMinuteForm  # Zakładając, że utworzymy formularze

@login_required
def create_meeting_minute(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        form = MeetingMinuteForm(request.POST)
        if form.is_valid():
            minute = form.save(commit=False)
            minute.meeting = meeting
            minute.user = request.user
            minute.save()
            return redirect('meeting_detail', meeting_id=meeting.id)
    else:
        form = MeetingMinuteForm()
    return render(request, 'myapp/meeting_minute_form.html', {'form': form, 'meeting': meeting})

@login_required
def update_meeting_minute(request, minute_id):
    minute = get_object_or_404(MeetingMinute, id=minute_id)
    if request.method == 'POST':
        form = MeetingMinuteForm(request.POST, instance=minute)
        if form.is_valid():
            form.save()
            return redirect('meeting_detail', meeting_id=minute.meeting.id)
    else:
        form = MeetingMinuteForm(instance=minute)
    return render(request, 'myapp/meeting_minute_form.html', {'form': form, 'meeting': minute.meeting})

@login_required
def delete_meeting_minute(request, minute_id):
    minute = get_object_or_404(MeetingMinute, id=minute_id)
    meeting_id = minute.meeting.id
    if request.method == 'POST':
        minute.delete()
        return redirect('meeting_detail', meeting_id=meeting_id)
    return render(request, 'myapp/meeting_minute_confirm_delete.html', {'minute': minute})

@login_required
def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    minutes = MeetingMinute.objects.filter(meeting=meeting)
    return render(request, 'myapp/meeting_detail.html', {'meeting': meeting, 'minutes': minutes})

