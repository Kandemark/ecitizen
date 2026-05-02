from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q, Count, Prefetch
from ..models import Chapter, Article, Schedule


def constitution_browse(request):
    chapters = Chapter.objects.prefetch_related(
        Prefetch('articles', queryset=Article.objects.order_by('order'))
    ).order_by('order')
    schedules = Schedule.objects.order_by('order')
    return render(request, 'constitution/browse.html', {
        'chapters': chapters,
        'schedules': schedules,
    })


def constitution_chapter(request, number):
    chapter = get_object_or_404(
        Chapter.objects.prefetch_related(
            Prefetch('articles', queryset=Article.objects.order_by('order'))
        ),
        number=number,
    )
    all_chapters = Chapter.objects.only('number', 'title').order_by('order')
    return render(request, 'constitution/chapter.html', {
        'chapter': chapter,
        'articles': chapter.articles.all(),
        'chapters': all_chapters,
    })


def constitution_article(request, number):
    article = get_object_or_404(
        Article.objects.select_related('chapter'),
        number=number,
    )
    all_chapters = Chapter.objects.only('number', 'title').order_by('order')
    return render(request, 'constitution/article.html', {
        'article': article,
        'chapters': all_chapters,
    })


def constitution_schedules(request):
    schedules = Schedule.objects.order_by('order')
    chapters = Chapter.objects.only('number', 'title').order_by('order')
    return render(request, 'constitution/schedules.html', {
        'schedules': schedules,
        'chapters': chapters,
    })


def constitution_search(request):
    q = request.GET.get('q', '').strip()
    chapters = Chapter.objects.only('number', 'title').order_by('order')
    results = []
    if q:
        try:
            vector = SearchVector('title', weight='A', config='english') + \
                     SearchVector('content', weight='B', config='english')
            query = SearchQuery(q, config='english')
            results = Article.objects.annotate(
                rank=SearchRank(vector, query)
            ).filter(rank__gte=0.05).select_related('chapter').order_by('-rank')[:50]
        except Exception:
            results = Article.objects.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            ).select_related('chapter')[:50]
    return render(request, 'constitution/search.html', {
        'query': q,
        'results': results,
        'chapters': chapters,
    })
