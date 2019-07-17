import time
from PIL import Image
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from .forms import TopicForm, EntryForm
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    topic = Topic.objects.all()
    context = {'topics': topic}
    return render(request, 'dj_logs/index.html', context)

def topics(request):
    qs = Topic.objects.all()
    return render(request, 'dj_logs/topics.html', {'topics': qs})

def topic(request,topic_id):

    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'dj_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加主题"""
    if request.method !='POST':
        #未提交数据：创建一个新表单
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic1 =form.save(commit=False)
            new_topic1.owner =request.user
            new_topic1.save()
            return HttpResponseRedirect(reverse('dj_logs:topics'))

    context = {'form': form}
    return render(request, 'dj_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        if request.user != User.objects.all().get(username='root'):
            raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry1 = form.save(commit=False)
            new_entry1.topic = topic
            new_entry1.save()
            return HttpResponseRedirect(reverse('dj_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'dj_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        if request.user != User.objects.all().get(username='root'):
            raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dj_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'dj_logs/edit_entry.html', context)

def search(request):
    search_name = request.GET.get('name')
    topics = Topic.objects.filter(name__icontains=search_name)
    content = {'search': search_name,
               'topics': topics}
    return render(request, 'dj_logs/search.html', content)

@login_required
def delete_entry(request, delete_id):
    d_entry = Entry.objects.get(id=delete_id)
    d_entry_tp = d_entry.topic
    if d_entry_tp.owner != request.user:
        if request.user != User.objects.all().get(username='root'):
            raise Http404
    d_entry.delete()
    return HttpResponseRedirect(reverse('dj_logs:topic', args=[d_entry_tp.id]))

@login_required
def delete_topic(request, topic_id):
    d_top = Topic.objects.get(id=topic_id)
    if d_top.owner != request.user:
        if request.user != User.objects.all().get(username='root'):
            raise Http404
    d_top.delete()
    return HttpResponseRedirect(reverse('dj_logs:topics'))

def translation(request):
    from demo.youdao import translation
    if request.method == 'GET':
        entry_text = request.GET.get('text')
        # entry = Entry.objects.all().get(id=entry_id)
        entry_text = translation.trans(entry_text)
        return JsonResponse({'res': entry_text})
    # content = {'trans': trans_entry}
    # print(trans_entry)
    #return HttpResponseRedirect(reverse('dj_logs:topic', args=[entry.topic_id]))

def trans_aip(request):
    from demo.youdao import Yd_api, Tp_aip
    if request.method == 'GET':
        start_text = request.GET.get('text')
        trans_lc = request.GET.get('lc').split(',')
        end_text = Yd_api.connect(start_text, trans_lc)
        return JsonResponse({'res': end_text})
    if request.method == 'POST':
        image = request.FILES.get('img')
        phototime = request.user.username + time.strftime('%y%m%d%H%M%S')
        photo_last = str(image).split('.')[-1]
        photoname = '%s.%s' % (phototime, photo_last)
        image = Image.open(image)
        image.save('static/img/trans/' + photoname)
        image_path = 'D:/code~/PY/dj/static/img/trans/' + photoname
        res = Tp_aip.get_trans(image_path)
        trans_list = []
        for res_s in res:
            trans_list.append([res_s['context'], res_s['tranContent']])
        content = {
                   'trans': trans_list,
                   'image': photoname,
                   }
        return render(request, 'word/index.html', content)

def other(request):

    return render(request, 'dj_logs/other.html', {})

def baidu(request):
    from demo.baidu import aiptest
    content ={}
    if request.method == 'POST':
        image = request.FILES.get('img')
        phototime = request.user.username +time.strftime('%y%m%d%H%M%S')
        photo_last = str(image).split('.')[-1]
        photoname = '%s.%s' % (phototime, photo_last)
        image = Image.open(image)
        image.save('static/img/df/'+photoname)
        image_path = 'D:/code~/PY/dj/static/img/df/'+photoname
        content['res'] = aiptest.my_detect(image_path)
        content['image'] = photoname

    return render(request, 'dj_logs/face.html', content)
