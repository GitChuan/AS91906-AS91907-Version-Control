from ..character import Character

class Tyrion(Character):
    def __init__(self):
        super().__init__(
            name="Tyrion Lannister",
            image_path="../pictures/tyrion_lannister.png",
            hp=80,
            attack=60,
            intelligence=95,
            charisma=60
        )

    def get_display_data(self):
        return {
            "image_path": self.image_path,
            "name": self.name,
            "hp": self.hp,
            "attack": self.attack,
            "intelligence": self.intelligence,
            "charisma": self.charisma
        }
