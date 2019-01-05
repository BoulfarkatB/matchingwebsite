from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from mainapp.forms import SignUpForm, EditUserForm, EditProfileForm


appname = 'Shaaadi.com'


def index(request):
    context = { 'appname': appname }
    return render(request, 'mainapp/index.html', context)


"""
Uses Django User's Model, as it comes with built in validation
and is more robust and secure.
"""
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = SignUpForm()

    context = {
        'appname': appname,
        'form': form
    }
    return render(request, 'mainapp/signup.html', context)


## https://www.youtube.com/watch?v=2yoWf-kDXIk ##
# Used to view current logged in user's profile
# As well as others, with an optional parameter
@login_required
def profile(request, pk=None):
    if pk: user = User.objects.get(pk=pk)
    else: user = request.user
    context = {
        'appname': appname,
        'user': user
    }
    return render(request, 'mainapp/profile.html', context) 


@login_required
def edit_profile(request):
    if request.method == 'POST':
        userForm = EditUserForm(request.POST, instance=request.user)
        profileForm = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            return redirect('/profile')
    else:
        userForm = EditUserForm(instance=request.user)
        profileForm = EditProfileForm(instance=request.user.profile)
        context = {
            'appname': appname,
            'userForm': userForm,
            'profileForm': profileForm
        }
    return render(request, 'mainapp/edit_profile.html', context)


@login_required
def members(request):
    logged_in_user = request.user
    # Displays everyone apart from admin & current logged in user   
    other_users = User.objects.exclude(id__in=[1,logged_in_user.id])


    liu_name = []
    for hobby in logged_in_user.profile.hobbies.all():
       liu_name.append(hobby.name)

    liu = (logged_in_user, liu_name)

    result = []
    for user in other_users:
        hobbies = user.profile.hobbies.all()
        hobby_names = []
        for hobby in hobbies:
           hobby_names.append(hobby.name)
        result.append((user, hobby_names))

    ordered_list = order_by_hobbies(liu, result)
    
    context = {
        'appname': appname,
        'users': ordered_list
    }
    return render(request, 'mainapp/members.html', context)

# Helper method for sorting the list
def order_by_hobbies(user, other_users):
    (user_1, user_hobbies) = user
    result = []
    for (user, hobbies) in other_users:
        # Use set notation to find hobbies in common using intersect    
        result_s = set(hobbies)
        # Count the hobbies in intersection        
        count = len(result_s.intersection(user_hobbies))        
        result.append((user, count))

    # Sorts the list by users with the most common hobbies
    result = sorted(result, key=lambda us:us[1])
    # Displays in decending order    
    result.reverse() 

    result_t = []
    for r in result:
       result_t.append(r[0])

    return result_t
