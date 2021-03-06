# from msilib.schema import LockPermissions
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import News
from .forms import UserAppealForm
from django.contrib import messages
from django.core.mail import send_mail



class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        ctx = super(ShowNewsView, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница'
        return ctx



class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 3
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username') )
        return News.objects.filter(avtor=user).order_by('-date')
    
    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)
        ctx['title'] = f"Статьи от пользователя {self.kwargs.get('username')}"
        return ctx



class NewsDetailView(DetailView):
    model = News
    
    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)
        ctx['title'] = News.objects.get(pk=self.kwargs['pk'])
        return ctx
  
    
    
class UpdateNewsView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):
    model = News
    template_name = 'blog/create_news.html'
    fields = ['title', 'text']
    
    def get_context_data(self, **kwards):
        ctx = super(UpdateNewsView, self).get_context_data(**kwards)
        ctx['title'] = 'Обновление статьи'
        ctx['btn_text'] = 'Обновить статью'
        return ctx
    
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        return False
    
    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)



class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/'
    template_name = 'blog/delete-news.html'
    
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        return False



class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'blog/create_news.html'
    
    fields = ['title', 'text']
    
    def get_context_data(self, **kwards):
        ctx = super(CreateNewsView, self).get_context_data(**kwards)   
        ctx['title'] = 'Добавление статьи'
        ctx['btn_text'] = 'Добавить статью'
        return ctx
    
    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)
    


def contacti(request):
    if request.method == "POST":
        form = UserAppealForm(request.POST)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data.get('subject')
            plain_message = form.cleaned_data.get('text')
            from_email = f'From <{form.cleaned_data.get("email")}>'
            to = 'sgrigerc@gmail.com'
            send_mail(subject, plain_message, from_email, [to])
            messages.success(request, 'Сообщение было успешно отправлено!')
            return redirect('home')
    else:
        form = UserAppealForm()
        return render(request, 'blog/contacti.html', {'title':'Страница про нас', 'form': form})



def uslugi(request):
    servs = [
        {
            'title': 'Страница с услугами',
            'table_n_1': 'Быстро',
            'table_n_2': 'Дешево',
            'table_n_3': 'Качественно',
            'clmn_1': 'Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            'clmn_2': 'Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            'clmn_3': 'Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
        }
    ]  
    
    return render(request, 'blog/uslugi.html', {'servs': servs,'title': 'Услуги'})