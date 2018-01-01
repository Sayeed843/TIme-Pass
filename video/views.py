from django.views import generic
from django.views.generic.edit import CreateView,  DeleteView,  UpdateView
from django.urls import reverse_lazy
from .models import Video, UserFeedback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, FormView
from .forms import UserForm, UserLogin, AddVideoForm, UserFeedbackForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
# from myapplication.essay.models import Essay
# from django.contrib import admin


class IndexView(generic.ListView):
    model = User
    template_name = 'video/index.html'

    def get_queryset(self):
        return Video.objects.all()


def details(request, video_id):
    all_video = Video.objects.all()
    # object_list = Video.objects.filter(userfeedback__video=video_id)
    object_list = Video.objects.get(pk=video_id)
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'video/details.html', {
        'video': video,
        'all_video': all_video,
        'object_list': object_list,
    })


class DetailView(generic.DetailView):
    # model = Video
    model = User
    template_name = 'video/details.html'

    def get_queryset(self):

        return Video.objects.get()


def UserProfileView(request, user_id):
    template_name = 'video/profile.html'
    user = get_object_or_404(User, pk=user_id)
    return render(request, template_name, {'user': user})


class VideoCreate(CreateView):
    # template_name = 'video/video_form.html'
    form_class = AddVideoForm

    def get(self, request, video_id):
        if not request.user.is_authenticated():
            return render(request, 'video/login_form.html')
        else:
            user = get_object_or_404(User, pk=video_id)
            form = self.form_class(None, None)
            return render(request,  'video/video_form.html', {'form': form})

    def post(self, request, video_id):
        if not request.user.is_authenticated():
            return render(request, 'video/login_form.html')
        else:
            user = get_object_or_404(User, pk=video_id)
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():
                video = form.save(commit=False)
                video.user = user
                video.thumbnail = request.FILES['thumbnail']
                video.video_path = request.FILES['video_path']
                video.save()
                return render(request, 'video/profile.html', {'form': form})

            return render(request,  'video/video_form.html', {'form': form})


class VideoUpdate(UpdateView):
    model = Video
    fields = ['title', 'description', 'thumbnail', 'video_path']


class VideoDelete(DeleteView):
    model = Video
    success_url = reverse_lazy('video:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'video/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('video:index')

        return render(request, self.template_name, {'form': form})


class UserLoginView(FormView):
    template_name = 'video/login_form.html'
    form_class = UserLogin

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('video:index')

        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('video:login')


def discover(request):
    query = request.GET.get("q")
    if query:
        object_list = Video.objects.filter(title__icontains=query)
        return render(request, 'video/discover.html', {'object_list': object_list})
    else:
        object_list = Video.objects.all()
        return render(request, 'video/index.html', {'object_list': object_list})


# class CommentView(CreateView):
#     template_name = 'video/details.html'
#     form_class = UserFeedback
#
#     def get(self, request, pk):
#         if not request.user.is_authenticated():
#             return render(request, 'video/login_form.html')
#         else:
#             video = Video.objects.get(pk=pk)
#             form = self.form_class(None, None)
#             return render(request,  'video/details.html', {'form': form})
#
#     def post(self, request, pk):
#         com = request.GET.get("comment")
#         if not request.user.is_authenticated():
#             return render(request, 'video/login_form.html')
#         else:
#             video = Video.objects.get(pk=pk)
#             form = self.form_class(request.POST)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.video = video
#                 comment.comment = com
#                 comment.save()
#                 user_comment = UserFeedback.objects.all()
#                 return render(request, 'video/details.html', {
#                     'form': form,
#                     'user_comment': user_comment, })
#             return render(request,  'video/details.html', {'form': form})


def CommentView(request, video_id):
    if request.method == 'POST':
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            comment = request.POST.get('comment')
            video = Video.objects.get(pk=video_id)
            feedback = UserFeedback(video=video, comment=comment)
            feedback.save()
            # return redirect('video:comment')
            # return render(request, 'video/details.html', {'form': form})
            return redirect('video:details', video_id)
            # return redirect("{% url 'video:details' video_id %}")

        else:
            form = UserFeedbackForm()
        return render(request, 'video/details.html', {'form': form})
