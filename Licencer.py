import json
import os
import re

class Ticket:
    def __init__(self, name, address, licence, speed, compound = False):
        self.name = name

        self.address = address

        self.licence = licence

        self.speed = speed

        self.compound = compound

class Reader:
    def __init__(self, directory):
        self.directory = directory

        self.read()

    def read(self):
        with open(self.directory, "r") as file:
            self.list = json.load(file)

class Database:
    def __init__(self, directory):
        self.directory = directory

        if not os.path.isfile(self.directory):
            open(self.directory, "x")

        self.tickets = []

    def add(self, ticket):
        self.tickets.append(ticket.__dict__)

    def save(self):
        with open(self.directory, "w") as file:
            json.dump(self.tickets, file)

licences = Reader("licences.json")
speeding = Reader("speeding.json")

db = Database("tickets.json")

def is_stanard_licence(licence):
    listed = list(licence)

    pattern = "[A-Z]{2}\d{2} [A-Z]{3}$"
    if re.search(pattern, licence):
        return True

def find_person(licence):
    for human in licences.list:
        if human.get("licence") == licence:
            return human

def fine():
    for car in speeding.list:
        licence = car.get("licence")
        person = find_person(licence)
        
        ticket = Ticket(
            person.get("name"),
            person.get("address"),
            licence,
            car.get("speed"),
            not is_stanard_licence(licence)
        )

        db.add(ticket)

fine()
print("Speeding tickets have been decided in", db.directory)
db.save()

# [A-Z]{2}\d{2} [A-Z]{3}$
        
