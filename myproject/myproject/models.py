#models.py
from django.db import models
from django.conf import settings

class uAttributes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    score = models.PositiveIntegerField()
    guesses = models.PositiveBigIntegerField()

class wordG(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=-1)
    goal = models.BooleanField(default = False)
    argument = models.CharField(max_length = 5, help_text='')

class Letter(models.Model):
    COLORS = [
        ('g', 'Green'),
        ('y', 'Yellow'),
        ('x', 'Gray'),  # Use 'x' for gray to distinguish from letters
    ]

    word = models.ForeignKey(wordG, on_delete=models.CASCADE, related_name="letters")
    character = models.CharField(max_length=1, help_text='A single letter')
    position = models.PositiveIntegerField(help_text='Position in the word (0-4)')
    color = models.CharField(max_length=1, choices=COLORS, help_text='Feedback color')

class validWord(models.Model):
    argument = models.CharField(max_length = 5, help_text='')
class validGuess(models.Model):
    argument = models.CharField(max_length= 5, help_text= '')

#multiplayer stuff is below
class group(models.Model):
    name = models.CharField(max_length = 100)#just the ws url for now, maybe it will be different in the future


class groupMessage(models.Model):
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    message = models.JSONField()

class groupGoal(models.Model):
    group = models.ForeignKey(group, on_delete=models.CASCADE)
    goal = models.CharField(max_length=5, default='tests')
    
class groupLetter(models.Model):
    COLORS = [
        ('g', 'Green'),
        ('y', 'Yellow'),
        ('x', 'Gray'),  # Use 'x' for gray to distinguish from letters
    ]
    
    groupId = models.ForeignKey(group, on_delete=models.CASCADE)
    character = models.CharField(max_length=1, help_text='A single letter')
    position = models.PositiveIntegerField(help_text='Position in the word (0-4)')
    color = models.CharField(max_length=1, choices=COLORS, help_text='Feedback color')
