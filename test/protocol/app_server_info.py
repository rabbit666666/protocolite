from typing import List

class Seed:
    size: int

class Apple:
    weight: float
    seed: Seed

class Fruit:
    total_weight: float
    kinds: [str]
    basket_1: [Apple]
