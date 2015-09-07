from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response
from formtools.wizard.views import SessionWizardView
from main.forms import EmailUserCreationForm, AnswerForm
from main.models import Question, Answer, Subject, Review, Author


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.email_user("Welcome! Thank you for joining our sexy online community, Oyster.fm!")
            return redirect("home")
    else:
        form = EmailUserCreationForm()
    return render(request, "registration/register.html", {
        "form": form,
    })


def build_reviews(reviews):
    for rev in reviews:
        answers = Answer.objects.filter(review=rev['review'])
        rev['qa'] = []
        for answer in answers:
            question = Question.objects.get(answers=answer)
            rev['qa'].append({'question': question, 'answer': answer})
    return reviews


@login_required
def profile(request, author_id):
    author = Author.objects.get(id=author_id)
    author_reviews = [{'review': x} for x in Review.objects.filter(author=author).order_by('-created')]
    reviews = build_reviews(author_reviews)
    data = {
        "author": author,
        "reviews": reviews,
    }
    return render(request, "profile.html", data)


def home(request):
    s = Subject.objects.get(current=True)
    print subject
    recent_reviews = [{'review': x} for x in Review.objects.filter(subject__current=True).order_by('id')[:5]]
    reviews = build_reviews(recent_reviews)

    data = {
        'subject': s,
        'reviews': reviews,
    }
    return render(request, "home.html", data)


# def review(request):
#     if "question" in request.session:
#         print "question in session"
#         print request.session['question']
#         question = Question.objects.get(id=int(request.session['question']))
#     else:
#         question = Question.objects.get(subject__current=True)
#         print "new question"
#
#     if request.method == "POST":
#         form = AnswerForm(request.POST, question=question.question)
#         if form.is_valid():
#             answer = form.cleaned_data['answer']
#             print question.question
#             print answer
#             del request.session['question']
#             Answer.objects.create(question=question, author=request.user, answer=answer)
#             return redirect("review")
#
#     else:
#         form = AnswerForm(question=question.question)
#         request.session['question'] = question.id
#     return render(request, "review.html", {
#         "form": form,
#     })


def process_form_data(form_list, request):
    form_data = [form.cleaned_data for form in form_list]
    form_a1 = form_data[0]['answer']
    form_a2 = form_data[1]['answer']
    form_a3 = form_data[2]['answer']
    form_q = form_data[3]['question']
    form_r1 = int(form_data[4]['rating'])
    q1 = Question.objects.get(id=request.session["question1"])
    q2 = Question.objects.get(id=request.session["question2"])
    q3 = Question.objects.get(id=request.session["question3"])
    subject = Subject.objects.get(current=True)

    r1 = Review.objects.create(rating=form_r1, author=request.user, subject=subject)
    Question.objects.create(author=request.user, subject=subject, question=form_q)
    Answer.objects.create(question=q1, review=r1, author=request.user, answer=form_a1)
    Answer.objects.create(question=q2, review=r1, author=request.user, answer=form_a2)
    Answer.objects.create(question=q3, review=r1, author=request.user, answer=form_a3)

    del request.session['question1']
    del request.session['question2']
    del request.session['question3']
    return form_data


class ReviewWizard(SessionWizardView):
    template_name = "review_form.html"

    def done(self, form_list, **kwargs):
        form_data = process_form_data(form_list, self.request)

        return render_to_response("done.html", {"form_data": form_data})

    def get_form_kwargs(self, step=None):
        kwargs = super(ReviewWizard, self).get_form_kwargs(step)
        if int(step) in (0, 1, 2):
            kwargs['request'] = self.request
        return kwargs


def review(request):
    if request.method == "POST":
        form = AnswerForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            print "saved"
            return redirect("review")
    else:
        form = AnswerForm(request=request)
    return render(request, "review.html", {
        "form": form,
    })


def archives(request):
    subjects = Subject.objects.all().order_by('id')
    data = {
        "subjects": subjects,
    }
    return render(request, "archives.html", data)


def subject(request, subject_id):
    s = Subject.objects.get(id=subject_id)
    subject_reviews = [{'review': x} for x in Review.objects.filter(subject=s).order_by('-created')]
    reviews = build_reviews(subject_reviews)
    data = {
        "subject": s,
        "reviews": reviews,
    }

    return render(request, "subject.html", data)