from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Document


@login_required
def document_list(request):
    documents = Document.objects.filter(user=request.user).order_by('-created_at')
    total_size = sum(d.file_size for d in documents if d.file_size)
    return render(request, 'documents/list.html', {
        'documents': documents,
        'total_size': total_size,
    })


@login_required
def document_upload(request):
    if request.method == 'POST':
        uploaded = request.FILES.get('file')
        name = request.POST.get('name', '')
        if not uploaded:
            messages.error(request, 'Please select a file to upload.')
            return redirect('document_list')

        doc = Document.objects.create(
            user=request.user,
            name=name or uploaded.name,
            file=uploaded,
            file_size=uploaded.size,
            mime_type=uploaded.content_type or '',
            tags=request.POST.get('tags', '').split(',') if request.POST.get('tags') else [],
        )
        messages.success(request, f'"{doc.name}" uploaded successfully.')
        return redirect('document_list')

    return redirect('document_list')


@login_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    name = doc.name
    doc.file.delete(save=False)
    doc.delete()
    messages.success(request, f'"{name}" deleted.')
    return redirect('document_list')
