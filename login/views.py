from django.shortcuts import render, HttpResponse, redirect
from .models import User, UserForm


def login(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form['user'].data
        password = form['password'].data

        result = User.objects.filter(user=user, password=password)
        if result and len(result) == 1:
            request.session['user'] = user
            return redirect('recommendations')
        else:
            return redirect('login/create.html', context={'form': form})
    else:
        return render(request, "login/login.html", context={'form': form})


def register(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = User()
        user.user = form['user'].data
        user.password = form['password']

        User.save(user)
        request.session['user'] = user.user
        return redirect('recommendations')
    else:
        return redirect('login/create.html', context={'form': form})


def recommendations(request):
    return render(request, 'login/recommendations.html')
    # user = request.session['user']
    # print(user)
    # recommendations_result = Recommendations.objects.filter(user=user).order_by('-rating')
    #
    # jaccard_u = recommendations_result.filter(recommendationType='jaccard').filter(model='u')
    # cosine_u = recommendations_result.filter(recommendationType='cosine').filter(model='u')
    # pearson_u = recommendations_result.filter(recommendationType='pearson').filter(model='u')
    #
    # jaccard_t = recommendations_result.filter(recommendationType='jaccard').filter(model='t')
    # cosine_t = recommendations_result.filter(recommendationType='cosine').filter(model='t')
    # pearson_t = recommendations_result.filter(recommendationType='pearson').filter(model='t')
    #
    # return render(request, "login/recommendations.html", context=
    #     {
    #         'user': user,
    #         'jaccard_u': jaccard_u,
    #         'cosine_u': cosine_u,
    #         'pearson_u': pearson_u,
    #         'jaccard_t': jaccard_t,
    #         'cosine_t': cosine_t,
    #         'pearson_t': pearson_t,
    #      }
    #               )
