"""Hack the planet!
"""

import meshbbs.bbs
import random

letter = 'P'
name = "hack the Planet"

quotes = [
"Mess with the best, die like the rest.",
"There is no right and wrong. There's only fun and boring.",
"Spandex: it's a privilege, not a right.",
"The pool on the roof must have a leak.",
"YO THIS IS ZERO COOL!",
"Whoa! This isn't woodshop class?",
"Of all the things I've lost, I miss my mind the most.",
"Orwell is here now. He's livin' large. We have no names, man. No names. We are nameless!",
"When I was a child, I spoke as a child, I understood as a child, I thought as a child, but when I became a man, I put away childish things. What? It's Corinthians one, chapter thirteen verse eleven.",
"God gave men brains larger than dogs so they wouldn't hump women's legs at cocktail parties.' - Ruth Libby.",
"It's in that place where I put that thing that time.",
"Angelheaded hipsters burning for the ancient heavenly connection to the starry dynamo in the machinery of night.",
"I hope you don't screw like you type.",
"So, would your holiness care to change her password?",
"Remember, hacking is more than just a crime. It's a survival trait.",
"HACK THE PLANET",
"This *is* a payphone.",
"Hack the planet! Hack the planet!",
"I don't play well with others.",
"If you want to be elite, you've got to do a righteous hack!"
]

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user

    def run(self) -> str:
        self.user.print(random.choice(quotes))
