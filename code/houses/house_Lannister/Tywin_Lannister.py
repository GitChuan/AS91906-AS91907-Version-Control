from Project.code.houses.character import Character

class Tywin(Character):
    def __init__(self):
        super().__init__(
            name="Tywin Lannister",
            image_path="../pictures/tywin_lannister.png",
            hp=130,
            attack=75,
            intelligence=85,
            charisma=70,
            ability= "Legacy of Power: Earn 1.5 times the points during score calculation.",
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
