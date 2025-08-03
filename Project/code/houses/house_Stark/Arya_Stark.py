from ..character import Character

class Arya(Character):
    def __init__(self):
        super().__init__(
            name="Arya Stark",
            image_path="../pictures/arya_stark.png",
            hp=70,
            attack=70,
            intelligence=80,
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
