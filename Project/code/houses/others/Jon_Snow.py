from ..character import Character

class JonSnow(Character):
    def __init__(self):
        super().__init__(
            name="Jon Snow",
            image_path="../pictures/jon_snow.png",
            hp=120,
            attack=65,
            intelligence=50,
            charisma=75
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
