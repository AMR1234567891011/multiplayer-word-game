#views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import wordform
from .models import wordG, Letter, uAttributes
from .validWordle import initSet, getRandWord, isValid

def homepage(request):
    return render(request,  'home.html')

def about(request):
    return render(request,  'about.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uName = form.cleaned_data.get('username')
            pWord = form.cleaned_data.get('password1')
            user = authenticate(username=uName, password=pWord)
            login(request, user)
            obj = uAttributes.objects.create(user= user, score=0, guesses=0)
            return redirect('login')
        else:
            form = UserCreationForm()
            return render(request, 'registration/signup.html', {'form':form})
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form':form})
        
#game stuff below
def word_game(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        formIN = wordform(request.POST)
        dt = str(formIN.data)
        if "argument" in dt:
            print(f"input:   {dt}")
            idx = dt.find("argument") + len("argument")+5
            s = str(dt[idx:len(dt) - 4])
            goal = str(wordG.objects.filter(user=request.user, goal = True).first().argument)

        if formIN.is_valid():
            formNEXT = wordform()
            UserAttributes = uAttributes.objects.get(user = request.user)

            if not isValid(s):#if not a valid guess dont return anything
                print(f"{s} is not a valid guess")
                user_wordG = wordG.objects.filter(user=request.user, goal = False).distinct()
                context = {
                'formIN':formNEXT,
                'guesses': user_wordG,
                'score': UserAttributes.score,
                'tries': UserAttributes.guesses,
                'feedback': 'Must enter a valid word'
                }
                return render(request, 'word_guess.html', context)
            
            wG = wordG.objects.create(argument = s,user=request.user)# add the word guess to users guesses in db
            if s == goal.split()[0]:# if the word is correct, go to the win screen
                print("DONE")
                wordG.objects.filter(user=request.user).delete()
                UserAttributes.score += 1
                UserAttributes.guesses += 1
                UserAttributes.save()
                return render(request, 'win_screen.html', {'word': goal})
            

            else:# go through the word and check if the letters are in position
                goal_used = [False for _ in range(5)]
                letter = ['x' for _ in range(5)]
                for i,char in enumerate(s):
                    if s[i]==goal[i]:
                        print(f"green at: {i + 1}")
                        letter[i] = 'g'
                        goal_used[i] = True
                for i,char in enumerate(s):
                    if s[i]!=goal[i]:#no greens
                        if char in goal:
                            for j,gchar in enumerate(goal):
                                if gchar == char and not goal_used[j]:
                                    print(f"yellow at: {i + 1}")
                                    letter[i] = 'y'
                                    goal_used[j] = True
                                    break
                        else:
                            letter[i] = 'x'

            for i, CHcolor in enumerate(letter):#add the correct character color combos to db becuase order is important
                print(f"{s[i]} color: {CHcolor}")
                Letter.objects.create(word = wG, character = s[i], position = i, color = CHcolor)
            user_wordG = wordG.objects.filter(user=request.user, goal = False).distinct()
            #guesses = wordG.objects.prefetch_related('letters').filter(letters__isnull=False).distinct()
            if len(user_wordG) >= 6:
                print("DONE")
                wordG.objects.filter(user=request.user).delete()
                UserAttributes.guesses += 1
                UserAttributes.save()
                return render(request, 'loss_screen.html', {'word': goal})
            UserAttributes.guesses += 1
            UserAttributes.save()
            context = {
                'formIN':formNEXT,
                'guesses': user_wordG,
                'score': UserAttributes.score,
                'tries': UserAttributes.guesses,
            }
            return render(request, 'word_guess.html', context)

    else:
        #first time opening game, need to select a new word
        user_wordG = wordG.objects.filter(user=request.user, goal = False).distinct()
        guessLen = len(user_wordG)
        if guessLen <= 0:
            if initSet():
                goal = str(getRandWord())
                wordG.objects.create(user=request.user, argument = goal, goal = True)
                print(f"NEW GOAL WORD: {goal}")
        else:
            goal = wordG.objects.filter(user=request.user, goal = True).distinct().first()
        if len(user_wordG) >= 6:
                print("DONE")
                wordG.objects.filter(user=request.user).delete()
                return render(request, 'loss_screen.html', {'word': goal})
        UserAttributes = uAttributes.objects.get(user = request.user)
        formIN = wordform()
        context = {
            'formIN': formIN,
            'guesses': user_wordG,
            'score': UserAttributes.score,
            'tries': UserAttributes.guesses
        }
        return render(request, 'word_guess.html', context)
