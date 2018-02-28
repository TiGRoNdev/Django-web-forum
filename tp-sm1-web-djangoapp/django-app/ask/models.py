from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse


class TagManager(models.Manager):
    def popular(self):
        return self.order_by('-rating')

    def create_tag(self, name):
        tag = self.create(name=name)
        return tag


class Tag(models.Model):
    name = models.CharField(blank=False, max_length=15, unique=True)
    rating = models.IntegerField(default=0)
    objects = TagManager()

    def __unicode__(self):
        return self.name

    def __int__(self):
        return self.id


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by("-id")

    def popular(self):
        return self.order_by("-rating")

    def create_question(self, d):
        tags = []
        for tag in d['tags']:
            tags.append(Tag.objects.get_or_create(name=tag))
        question = self.create(title=d["title"],
                               text=d["text"],
                               added_at=datetime.now().date())
        return question, tags


class AnswerManager(models.Manager):
    def main(self, since, question, limit=10):
        qs = self.order_by("-id")
        qs = qs.filter(question=question)
        res = []
        if since is not None and since != "None":
            qs = qs.filter(id__lt=since)
        for p in qs[:100]:
            res.append(p)
            if len(res) >= limit:
                break
        if len(res) > 1:
            since = res[-1].id
        elif len(res) == 1:
            since = res[0].id
        return res, since

    def create_answer(self, d):
        answer = self.create(text=d["text"],
                             added_at=datetime.now().date())
        return answer


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateField(blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(User, models.DO_NOTHING, null=True)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(User, related_name="question_like_user")
    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('question', args=[str(self.id)])

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField(blank=True, auto_now_add=True)

    question = models.ForeignKey(Question, models.DO_NOTHING, null=True)
    author = models.ForeignKey(User, models.DO_NOTHING, null=True)
    objects = AnswerManager()

    def get_absolute_url(self):
        return reverse('question', args=[str(self.question.id)])
