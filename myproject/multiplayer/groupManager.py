import json
from myproject.models import group, groupMessage, groupGoal

class groupManager:
    def __init__(self):
        self.groups = {}
    def kill(self, name):#clear all data about a group
        print(f"killed {name}")
        if name in self.groups:
            self.groups[name][0].delete()
            del self.groups[name]

    def flush(self, name, socket):#flush old messages to new websocket
        print(f"flushing {name} to {socket.U}")
        if name in self.groups:
            g, _ = self.groups[name]
            messages = groupMessage.objects.filter(group=g).distinct()
            for obj in messages:
                print(f"flushed message: {obj.message}")
                socket.send(json.dumps(obj.message))
        
    def add(self, name, socket):
        new = False
        if name not in self.groups:
            self.groups[name] = (group.objects.create(name=name),set())
            new = True
            print(f"made new group {name}")
        g, sockets = self.groups[name]
        sockets.add(socket)
        self.flush(name, socket)
        print(f"{socket.U} joined group {name}")
        return new
    def remove(self, name, socket):
        if name in self.groups and socket in self.groups[name]:
            self.groups[name].remove(socket)
            if not self.groups[name]:
                self.groups[name][0].delete()
                del self.groups[name]

    def send_to_group(self, sock, name, message):
        if name in self.groups:
            g, sockets = self.groups[name]
            print(f"message sent: {groupMessage.objects.create(group=g, message=message)}")
            for s in sockets:
                s.send(json.dumps(message))

    #extra functions for the wordle game
    def assignGoal(self, name, goal):
        if name in self.groups:
            g, _ = self.groups[name]
            groupGoal.objects.filter(group=g).delete()
            groupGoal.objects.create(group=g, goal=goal)
    def getGoal(self, name):
        if name in self.groups:
            g, _ =self.groups[name]
            return groupGoal.objects.filter(group=g)[0].goal
    
    