import json
from channels.generic.websocket import WebsocketConsumer
from myproject.models import groupLetter, group, groupMessage, groupGoal
from .groupManager import groupManager
from myproject.validWordle import isValid, getRandWord

groups = groupManager()
class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.lobby_name = self.scope['url_route']['kwargs']['lobby_name']
        self.room_group_name = f'lobby_{self.lobby_name}'
        self.U = self.scope["user"]
        self.accept()

        if groups.add(self.room_group_name, self):#if the group is new assign a goal word
            print("")
            groups.assignGoal(self.room_group_name, getRandWord().strip())
    
        groups.send_to_group(self, self.room_group_name, {
            'type': 'server-message',
            'message': groups.getGoal(self.room_group_name)
        })
        groups.send_to_group(self,self.room_group_name, {
            'type': 'lobby-management',
            'event': 'new-connection',
            'message': f'{self.scope["user"]}'
        })
        self.send(text_data=json.dumps({
            'type': 'connection',
            'message':'connected'
        }))

    def receive(self, text_data):
        print(f"INPUT FROM SOCKET --- {json.loads(text_data)["message"]} user: {self.scope["user"]}")
        input = json.loads(text_data)
        message = input["message"]
        if input["type"] == "guess-validation":
            
            if isValid(input["message"]):
                #code below grades a users guess
                goal = groups.getGoal(self.room_group_name)
                s = input["message"]
                goal_used = [False for _ in range(5)]
                letter = ['x' for _ in range(5)]
                for i,char in enumerate(s):
                    if s[i]==goal[i]:
                        print(f"green at: {i + 1}")
                        letter[i] = 'green'
                        goal_used[i] = True
                for i,char in enumerate(s):
                    if s[i]!=goal[i]:#no greens
                        if char in goal:
                            for j,gchar in enumerate(goal):
                                if gchar == char and not goal_used[j]:
                                    print(f"yellow at: {i + 1}")
                                    letter[i] = 'yellow'
                                    goal_used[j] = True
                                    break
                        else:
                            letter[i] = 'gray'
                
                groups.send_to_group(self, self.room_group_name, {
                    'type': 'lobby-guess',
                    'user': self.scope["user"].username,
                    'c1': letter[0],
                    'c2': letter[1],
                    'c3': letter[2],
                    'c4': letter[3],
                    'c5': letter[4],
                    'win': 'False',
                    'message': input["message"]
                })
            else:
                if message == "delete":
                    groups.kill(self.room_group_name)
                else:
                    self.send(text_data=json.dumps({
                        'type':'guess-validation',
                        'message': 'invalid guess, must be five letters and a real word',
                    }))


    