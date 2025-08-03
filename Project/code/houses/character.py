# Common charactor class
class Character:
    def __init__(self, name, image_path, hp, attack, intelligence, charisma):
        self.name = name
        self.image_path = image_path
        self.hp = hp
        self.attack = attack
        self.intelligence = intelligence
        self.charisma = charisma