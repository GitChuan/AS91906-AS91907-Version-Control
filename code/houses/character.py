# 通用角色模板类
class Character:
    def __init__(self, name, image_path, hp, attack, intelligence, charisma, ability):
        self.name = name
        self.image_path = image_path
        self.hp = hp
        self.attack = attack
        self.intelligence = intelligence
        self.charisma = charisma
        self.ability = ability

    # def is_alive(self):
    #     return self.hp > 0

