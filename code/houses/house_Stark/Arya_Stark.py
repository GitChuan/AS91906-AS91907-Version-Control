from Project.code.houses.character import Character

class Arya(Character):
    def __init__(self):
        super().__init__(
            name="Arya Stark",
            image_path="../pictures/arya_stark.png",
            hp=100,
            attack=70,
            intelligence=80,
            charisma=70,
            ability="Needle Mastery: Innate 60% chance to land a critical hit.",
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
