import random
from typing import List

class Pet:
    MAX_STAT = 10
    MIN_STAT = 0
    
    def __init__(self, name: str, pet_type: str = "generic"):
        self.name = name
        self.pet_type = pet_type
        self.hunger = 6
        self.energy = 3
        self.happiness = 5
        self.tricks = []
        self._mood = "neutral"
        self._emoji = self._get_emoji()
        
    def _update_mood(self) -> None:
        if self.happiness >= 8:
            self._mood = "happy"
        elif self.happiness <= 3:
            self._mood = "sad"
        else:
            self._mood = "neutral"
        self._emoji = self._get_emoji()
    
    def _get_emoji(self) -> str:
        emojis = {
            "happy": "😊",
            "sad": "😢",
            "neutral": "😐",
            "tired": "😴",
            "hungry": "😋"
        }
        if self.energy <= 2:
            return emojis["tired"]
        if self.hunger >= 8:
            return emojis["hungry"]
        return emojis.get(self._mood, "🐾")
    
    def _clamp_stat(self, value: int) -> int:
        return max(self.MIN_STAT, min(self.MAX_STAT, value))
    
    def eat(self, food_amount: int = 3) -> str:
        self.hunger = self._clamp_stat(self.hunger - food_amount)
        self.happiness = self._clamp_stat(self.happiness + 1)
        self._update_mood()
        return f"{self._emoji} {self.name} ate. Hunger: {self.hunger}, Happiness: {self.happiness}"
    
    def sleep(self, hours: int = 1) -> str:
        energy_gain = hours * 2
        self.energy = self._clamp_stat(self.energy + energy_gain)
        self._update_mood()
        return f"{self._emoji} {self.name} slept for {hours} hour(s). Energy: {self.energy}"
    
    def play(self) -> str:
        if self.energy < 2:
            return f"{self._emoji} {self.name} is too tired to play."
        
        self.energy = self._clamp_stat(self.energy - 2)
        self.happiness = self._clamp_stat(self.happiness + 2)
        self.hunger = self._clamp_stat(self.hunger + 1)
        self._update_mood()
        
        play_actions = [
            f"{self.name} chases its tail!",
            f"{self.name} plays with a toy!",
            f"{self.name} runs around excitedly!"
        ]
        return f"{self._emoji} {random.choice(play_actions)} Energy: {self.energy}, Happiness: {self.happiness}, Hunger: {self.hunger}"
    
    def train(self, *tricks: str) -> str:
        learned = []
        for trick in tricks:
            if trick not in self.tricks:
                self.tricks.append(trick)
                learned.append(trick)
        
        if not learned:
            return f"{self._emoji} {self.name} already knows those tricks."
        
        self.happiness = self._clamp_stat(self.happiness + 1)
        self._update_mood()
        
        if len(learned) == 1:
            return f"{self._emoji} {self.name} learned a new trick: {learned[0]}!"
        return f"{self._emoji} {self.name} learned new tricks: {', '.join(learned)}!"
    
    def show_tricks(self) -> str:
        if not self.tricks:
            return f"{self._emoji} {self.name} doesn't know any tricks yet."
        return f"{self._emoji} {self.name} knows: {', '.join(self.tricks)}"
    
    def get_status(self) -> str:
        status = [
            f"{self._emoji} {self.name}'s status:",
            f"Type: {self.pet_type}",
            f"Mood: {self._mood}",
            f"Hunger: {self.hunger}/10",
            f"Energy: {self.energy}/10",
            f"Happiness: {self.happiness}/10",
            f"Tricks known: {len(self.tricks)}"
        ]
        return "\n".join(status)
    
    def random_action(self) -> str:
        actions = [
            (self.eat, ()),
            (self.sleep, (1,)),
            (self.play, ()),
            (lambda: f"{self._emoji} {self.name} is just hanging out.", ())
        ]
        if self.tricks:
            actions.append((lambda: f"{self._emoji} {self.name} performs {random.choice(self.tricks)}!", ()))
        
        action, args = random.choice(actions)
        return action(*args)


if __name__ == "__main__":
    pet = Pet("Max", "dog")
    print(pet.get_status())
    print(pet.eat())
    print(pet.play())
    print(pet.sleep(2))
    print(pet.train("roll over", "play dead"))
    print(pet.show_tricks())
    print(pet.get_status())
    
    print("\nRandom actions:")
    for _ in range(5):
        print(pet.random_action())