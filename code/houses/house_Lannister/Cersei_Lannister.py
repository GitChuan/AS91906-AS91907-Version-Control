from Project.code.houses.character import Character

class Cersei(Character):
    def __init__(self):
        super().__init__(
            name="Cersei Lannister",
            image_path="../pictures/cersei_lannister.png",
            hp=60,
            attack=30,
            intelligence=60,
            charisma=85,
            ability="Queen’s Deception: Instantly kills all existing enemies, can be used up to 2 times.",
        )

    def get_display_data(self):
        return {
            "image_path": self.image_path,
            "name": self.name,
            "hp": self.hp,
            "attack": self.attack,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "ability": self.ability
        }