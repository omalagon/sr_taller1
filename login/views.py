from django.shortcuts import render, HttpResponse, redirect
from .models import User, Recommendations, UserForm, LoginForm


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        userid = form['userid'].data
        result = User.objects.filter(userid=userid)
        if result and len(result) == 1:
            request.session['userid'] = userid
            return redirect('recommendations')
        else:
            return redirect('register')
    else:
        return render(request, "login/login.html", context={'form': form})


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = User()
        user.userid = form['userid'].data
        user.gender = form['gender'].data
        user.age = form['age'].data
        user.country = form['country'].data

        User.save(user)
        request.session['userid'] = user.userid
        return redirect('recommendations')
    else:
        return render(request, "login/create.html", context={'form': form})

def recommendations(request):
    userid = request.session['userid']
    print(userid)
    recommendations_result = Recommendations.objects.filter(userid=userid).order_by('-rating')

    jaccard_u = recommendations_result.filter(recommendationType='jaccard').filter(model='u')
    cosine_u = recommendations_result.filter(recommendationType='cosine').filter(model='u')
    pearson_u = recommendations_result.filter(recommendationType='pearson').filter(model='u')

    jaccard_t = recommendations_result.filter(recommendationType='jaccard').filter(model='t')
    cosine_t = recommendations_result.filter(recommendationType='cosine').filter(model='t')
    pearson_t = recommendations_result.filter(recommendationType='pearson').filter(model='t')

    return render(request, "login/recommendations.html", context=
        {
            'userid': userid,
            'jaccard_u': jaccard_u,
            'cosine_u': cosine_u,
            'pearson_u': pearson_u,
            'jaccard_t': jaccard_t,
            'cosine_t': cosine_t,
            'pearson_t': pearson_t,
         }
                  )
