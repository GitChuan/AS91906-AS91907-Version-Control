from ..character import Character

class Bran(Character):
    def __init__(self):
        super().__init__(
            name="Bran Stark",
            image_path="../pictures/bran_stark.png",
            hp=120,
            attack=40,
            intelligence=100,
            charisma=70
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
