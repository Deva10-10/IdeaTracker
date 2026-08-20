
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


STATUS_LABELS = {
    'draft': 'Draft',
    'in_progress': 'In Progress',
    'completed': 'Completed',
}


class Tag:
    def __init__(self, name):
        self.name = name


class TagList:
    def __init__(self, names):
        self.all = [Tag(name) for name in names]


class IdeaItem:
    def __init__(self, pk, title, description, status='draft', tags=None, rating=3, is_favorite=False, ai_summary=''):
        self.pk = pk
        self.title = title
        self.description = description
        self.status = status
        self.is_favorite = is_favorite
        self.rating = int(rating)
        self.ai_summary = ai_summary
        self.tags = TagList(tags or [])

    def get_status_display(self):
        return STATUS_LABELS.get(self.status, self.status)


def _get_session_ideas(request):
    ideas = request.session.get('ideas', [])
    return ideas


def _save_session_ideas(request, ideas):
    request.session['ideas'] = ideas
    request.session.modified = True


def _idea_from_session(item):
    return IdeaItem(
        pk=item.get('pk'),
        title=item.get('title', ''),
        description=item.get('description', ''),
        status=item.get('status', 'draft'),
        tags=item.get('tags', []),
        rating=item.get('rating', 3),
        is_favorite=item.get('is_favorite', False),
        ai_summary=item.get('ai_summary', ''),
    )


def home(request):
    return render(request, 'idea_list.html', {'ideas': _get_session_ideas(request)})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('idea_list')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not email or not password:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def idea_list(request):
    ideas = [
        _idea_from_session(item)
        for item in _get_session_ideas(request)
    ]
    return render(request, 'idea_list.html', {'ideas': ideas})


def idea_create(request):
    if request.method == 'POST':
        ideas = _get_session_ideas(request)
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', 'draft')
        tags = [tag.strip() for tag in request.POST.get('tags', '').split(',') if tag.strip()]
        rating = request.POST.get('rating', 3)

        if title and description:
            new_idea = {
                'pk': len(ideas) + 1,
                'title': title,
                'description': description,
                'status': status,
                'tags': tags,
                'rating': int(rating),
                'is_favorite': False,
                'ai_summary': '',
            }
            ideas.append(new_idea)
            _save_session_ideas(request, ideas)
            return redirect('idea_list')

        messages.error(request, 'Title and description are required.')

    return render(request, 'idea_form.html', {'idea': None})


def idea_edit(request, pk):
    ideas = _get_session_ideas(request)
    idea_data = next((item for item in ideas if item.get('pk') == pk), None)

    if request.method == 'POST' and idea_data:
        idea_data['title'] = request.POST.get('title', '').strip()
        idea_data['description'] = request.POST.get('description', '').strip()
        idea_data['status'] = request.POST.get('status', 'draft')
        idea_data['tags'] = [tag.strip() for tag in request.POST.get('tags', '').split(',') if tag.strip()]
        idea_data['rating'] = int(request.POST.get('rating', idea_data.get('rating', 3)))
        _save_session_ideas(request, ideas)
        return redirect('idea_list')

    if idea_data:
        return render(request, 'idea_form.html', {'idea': _idea_from_session(idea_data)})

    return redirect('idea_list')


def idea_delete(request, pk):
    ideas = _get_session_ideas(request)
    filtered = [item for item in ideas if item.get('pk') != pk]
    _save_session_ideas(request, filtered)
    return redirect('idea_list')


def idea_toggle_favorite(request, pk):
    ideas = _get_session_ideas(request)
    for item in ideas:
        if item.get('pk') == pk:
            item['is_favorite'] = not item.get('is_favorite', False)
            break
    _save_session_ideas(request, ideas)
    return redirect('idea_list')


def idea_summarize(request, pk):
    ideas = _get_session_ideas(request)
    for item in ideas:
        if item.get('pk') == pk:
            description = item.get('description', '')
            item['ai_summary'] = f"Summary: {description[:80]}..." if description else 'Summary: No content available yet.'
            break
    _save_session_ideas(request, ideas)
    return redirect('idea_list')