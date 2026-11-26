from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.db.models import Q, F
from django.core.paginator import Paginator
from .models import Article, Category, Event


def home(request):
    """
    Landing page showcasing featured spotlight, dynamic search & filtering,
    category navigation pills, and paginated article listings.
    """
    search_query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    
    articles = Article.objects.select_related('category').all()
    categories = Category.objects.all()

    # Search filter
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(short_desc__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    # Category filter
    active_category = None
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            articles = articles.filter(category=active_category)

    # Featured spotlight (only on default unfiltered first page)
    featured_article = None
    if not search_query and not category_slug and request.GET.get('page', '1') == '1':
        featured_article = Article.objects.filter(is_featured=True).first()
        if not featured_article and articles.exists():
            featured_article = articles.first()

    # Pagination: 6 articles per page
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    trending_articles = Article.objects.order_by('-views_count')[:4]

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'active_category': active_category,
        'search_query': search_query,
        'featured_article': featured_article,
        'trending_articles': trending_articles,
        'total_count': paginator.count,
    }
    return render(request, 'home.html', context)


def read(request, slug):
    """
    In-depth reading view with view count tracking and category recommendations.
    """
    article = get_object_or_404(Article.objects.select_related('category'), slug=slug)

    # Atomic view count increment
    Article.objects.filter(pk=article.pk).update(views_count=F('views_count') + 1)
    article.refresh_from_db(fields=['views_count'])

    # Related articles recommendation
    related_articles = Article.objects.filter(category=article.category).exclude(pk=article.pk)[:3]
    if related_articles.count() < 3:
        supplementary = Article.objects.exclude(pk=article.pk).exclude(pk__in=related_articles.values_list('pk', flat=True))[:3 - related_articles.count()]
        related_articles = list(related_articles) + list(supplementary)

    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'read.html', context)


def read_by_id(request, id):
    """Backward-compatible lookup by numeric ID that redirects to the canonical slug."""
    article = get_object_or_404(Article, pk=id)
    return redirect('read', slug=article.slug)


from .services import fetch_live_tech_news, SUPPORTED_TOPICS


def news(request):
    """
    Live technology news aggregator pulling real-time dispatches from developer APIs
    with in-memory caching and topic filtering.
    """
    topic = request.GET.get('topic', 'all').lower().strip()
    if topic not in SUPPORTED_TOPICS:
        topic = 'all'
    force_refresh = request.GET.get('refresh') == 'true'

    live_news_data = fetch_live_tech_news(topic=topic, limit=12, force_refresh=force_refresh)
    latest_articles = Article.objects.select_related('category').order_by('-published_at')[:4]

    topics = [
        ('all', 'Global Wire (All)'),
        ('ai', 'Artificial Intelligence'),
        ('python', 'Python & Backends'),
        ('cloud', 'Cloud Architecture'),
        ('security', 'Cybersecurity'),
        ('devops', 'DevOps & SRE'),
    ]

    context = {
        'live_news': live_news_data['items'],
        'is_live': live_news_data['is_live'],
        'source': live_news_data['source'],
        'current_topic': topic,
        'topics': topics,
        'latest_articles': latest_articles,
    }
    return render(request, 'news.html', context)


def live_news_api(request):
    """JSON API endpoint for real-time news retrieval and live topic switching."""
    topic = request.GET.get('topic', 'all').lower().strip()
    force_refresh = request.GET.get('refresh') == 'true'
    data = fetch_live_tech_news(topic=topic, limit=12, force_refresh=force_refresh)
    return JsonResponse(data)


def events(request):
    """Upcoming global technology expos, summits, and symposiums."""
    all_events = Event.objects.all()
    context = {
        'events': all_events,
        'total_events': all_events.count(),
    }
    return render(request, 'events.html', context)


def about(request):
    """About page highlighting mission, tech stack, and architectural overview."""
    total_articles = Article.objects.count()
    total_categories = Category.objects.count()
    total_events = Event.objects.count()
    
    context = {
        'total_articles': total_articles,
        'total_categories': total_categories,
        'total_events': total_events,
    }
    return render(request, 'about.html', context)


def newsletter_subscribe(request):
    """Simple JSON response endpoint for simulated newsletter subscription."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email and '@' in email:
            return JsonResponse({'status': 'success', 'message': f'Thank you for subscribing with {email}!'})
        return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
