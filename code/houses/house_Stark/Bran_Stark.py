from Project.code.houses.character import Character

class Bran(Character):
    def __init__(self):
        super().__init__(
            name="Bran Stark",
            image_path="../pictures/bran_stark.png",
            hp=50,
            attack=0,
            intelligence=60,
            charisma=50,
            ability="Penetrating eyes: Find the optimal way to win in a battle, can be used up to 5 times.",
        )

    def get_display_data(self):
        return {
            "image_path": self.image_path,
            "name": self.name,
            "hp": self.hp,
            "attack": self.attack,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "ability": self.ability,
        }
