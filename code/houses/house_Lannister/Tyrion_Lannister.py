from Project.code.houses.character import Character

class Tyrion(Character):
    def __init__(self):
        super().__init__(
            name="Tyrion Lannister",
            image_path="../pictures/tyrion_lannister.png",
            hp=50,
            attack=10,
            intelligence=95,
            charisma=50,
            ability="Silver Tongue: Convert enemies to your allies in battle(Instantly add their hp and attack to yourself), can only be used once.",
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
