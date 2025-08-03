from ..character import Character

class Eddard(Character):
    def __init__(self):
        super().__init__(
            name="Eddard Stark",
            image_path="../pictures/eddard_stark.png",
            hp=110,
            attack=70,
            intelligence=60,
            charisma=30
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
