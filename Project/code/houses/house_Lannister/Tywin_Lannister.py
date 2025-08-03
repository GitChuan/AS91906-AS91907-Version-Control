from ..character import Character

class Tywin(Character):
    def __init__(self):
        super().__init__(
            name="Tywin Lannister",
            image_path="../pictures/tywin_lannister.png",
            hp=120,
            attack=60,
            intelligence=50,
            charisma=50
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
