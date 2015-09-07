from django import forms
from django.contrib.auth.forms import UserCreationForm
from main import models
from main.models import Author, Question, Answer, Review, Subject


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Author
        fields = ('username', 'email', 'password1', 'password2')


class ReviewForm(forms.ModelForm):
    curr_subject = Subject.objects.get(current=True)
    label = u"How would you rate {} overall?".format(curr_subject.name)
    RATINGS = (
        (1, ""),
        (2, ""),
        (3, ""),
        (4, ""),
        (5, ""),
    )
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATINGS, label=label)
    class Meta:
        model = Review
        fields = ('rating', )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question', )


class AnswerForm(forms.Form):
    answer = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'autofocus': 'true'} #actually all you need is autofocus attr. true not needed.
    ))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.question = None
        self.setup()
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].label = self.question.question

    def setup(self):
        if "question" in self.request.session:
            self.question = Question.objects.get(id=self.request.session["question"])
        else:
            self.question = Question.objects.get(subject__current=True)
            self.request.session["question"] = self.question.id

    # with the wizard, this does not seem to be used. saving happens in the wizard's done()
    def save(self):
        del self.request.session["question"]
        print "SAVED BRAH"
        Answer.objects.create(
            question=self.question,
            author=self.request.user,
            answer=self.cleaned_data['answer']
        )
        # super(AnswerForm, self).save()


class AnswerForm1(AnswerForm):

    def setup(self):
        if "question1" in self.request.session:
            self.question = Question.objects.get(id=self.request.session["question1"])
        else:
            self.question = Question.objects.random_subject_curr()
            self.request.session["question1"] = self.question.id


class AnswerForm2(AnswerForm):

    def setup(self):
        if "question2" in self.request.session:
            self.question = Question.objects.get(id=self.request.session["question2"])
        else:
            self.question = Question.objects.random_subject_curr()
            while int(self.request.session["question1"]) == self.question.id:
                self.question = Question.objects.random_subject_curr()
            self.request.session["question2"] = self.question.id


class AnswerForm3(AnswerForm):

    def setup(self):
        if "question3" in self.request.session:
            self.question = Question.objects.get(id=self.request.session["question3"])
        else:
            not_unique = True
            while not_unique:
                self.question = Question.objects.random_subject_curr()
                if self.question.id not in (int(self.request.session["question1"]), int(self.request.session["question2"])):
                    not_unique = False
            self.request.session["question3"] = self.question.id