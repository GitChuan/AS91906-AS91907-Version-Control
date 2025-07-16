from Project.code.houses.character import Character

class Eddard(Character):
    def __init__(self):
        super().__init__(
            name="Eddard Stark",
            image_path="../pictures/eddard_stark.png",
            hp=150,
            attack=90,
            intelligence=30,
            charisma=60,
            ability="Shield of the North: Decreases all damage taken by 50%.",
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
