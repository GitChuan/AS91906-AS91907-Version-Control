from ..character import Character

class Cersei(Character):
    def __init__(self):
        super().__init__(
            name="Cersei Lannister",
            image_path="../pictures/cersei_lannister.png",
            hp=100,
            attack=50,
            intelligence=60,
            charisma=85
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