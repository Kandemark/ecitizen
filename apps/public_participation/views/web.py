from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Consultation, PublicComment, Petition
from core.utils import generate_tracking_id


@login_required
def participation_list(request):
    consultations = Consultation.objects.filter(is_active=True).select_related('ministry').order_by('-start_date')
    petitions = Petition.objects.filter(user=request.user).order_by('-created_at')
    public_petitions = Petition.objects.filter(status='collecting_signatures').order_by('-created_at')[:10]
    return render(request, 'public_participation/list.html', {
        'consultations': consultations,
        'my_petitions': petitions,
        'public_petitions': public_petitions,
    })


@login_required
def consultation_detail(request, pk):
    consultation = get_object_or_404(
        Consultation.objects.filter(is_active=True).select_related('ministry'), pk=pk
    )
    comments = consultation.comments.filter(is_approved=True).select_related('user').order_by('-created_at')

    show_form = not consultation.comments.filter(user=request.user).exists()

    if request.method == 'POST' and show_form:
        comment = PublicComment(
            consultation=consultation,
            user=request.user,
            comment=request.POST.get('comment', ''),
        )
        comment.save()
        messages.success(request, 'Your comment has been submitted for review.')
        return redirect('participation_consultation', pk=pk)

    return render(request, 'public_participation/consultation_detail.html', {
        'consultation': consultation, 'comments': comments, 'show_form': show_form,
    })


@login_required
def petition_create(request):
    if request.method == 'POST':
        petition = Petition(
            user=request.user,
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            target_ministry_id=request.POST.get('target_ministry'),
            threshold=request.POST.get('threshold', 1000),
            status='collecting_signatures',
        )
        petition.save()
        from apps.applications.helpers import create_workflow_application
        create_workflow_application(petition, request.user)
        messages.success(request, f'Petition {petition.reference} created and is now collecting signatures.')
        return redirect('participation_petition_detail', ref=petition.reference)

    from apps.ministries.models import Ministry
    return render(request, 'public_participation/petition_apply.html', {
        'ministries': Ministry.objects.all(),
    })


@login_required
def petition_detail(request, ref):
    petition = get_object_or_404(Petition.objects.select_related('target_ministry'), reference=ref)

    if request.method == 'POST' and petition.status == 'collecting_signatures':
        if request.user != petition.user:
            petition.signature_count += 1
            petition.save()
            messages.success(request, 'You have signed this petition.')
        else:
            messages.error(request, 'You cannot sign your own petition.')

    return render(request, 'public_participation/petition_detail.html', {
        'petition': petition,
    })
