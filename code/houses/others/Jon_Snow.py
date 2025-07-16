from Project.code.houses.character import Character

class JonSnow(Character):
    def __init__(self):
        super().__init__(
            name="Jon Snow",
            image_path="../pictures/jon_snow.png",
            hp=12000,
            attack=850,
            intelligence=70,
            charisma=70,
            ability="Swordsmanship: Temporarily double the attack amount for 20 seconds.",
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
