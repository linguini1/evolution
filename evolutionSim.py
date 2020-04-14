# Evolution simulator

import random
import csv

# Starting information
repChance = 30
deathChance = 10
mutChance = 10
mutAmount = 5 / 100
initial_pop = 20
time_steps = 31
# -----------------------------
creatures_buffer = []
creatures = []
average_rep = 0
average_death = 0
average_mut = 0

# Asking if defaults should be changed
print("Default starting data is as follows: ")
print("Replication chance: 30%")
print("Death chance: 10%")
print("Mutation chance: 10%")
print("Mutation amount: 3%")
print("Initial population: 20")
print("Number of time steps: 30")
print()


# Getting valid input function
def get_data(message):
    while True:
        try:
            variable = int(input(message))
            return variable
        except ValueError:
            print("Invalid input.")


while True:
    set_info = input("Do you want to set new starting data? (y/n): ")
    if set_info.lower() == "yes" or set_info.lower() == "y":
        repChance = get_data("Replication chance: ")
        deathChance = get_data("Death chance: ")
        mutChance = get_data("Mutation chance: ")
        mutAmount = get_data("Mutation amount: ") / 100
        initial_pop = get_data("Initial population: ")
        time_steps = get_data("Number of time steps: ") + 1
        break
    elif set_info.lower() == "no" or set_info.lower() == "n":
        break
    else:
        print("Invalid input.")


# Creature class
class Creature:
    # Population tracker
    population = 0
    deaths = 0

    def __init__(self, rep_chance, death_chance, mut_chance, mut_amount):
        self.repChance = rep_chance
        self.deathChance = death_chance
        self.mutChance = mut_chance
        self.mutAmount = mut_amount
        self.status = 'alive'

        # Tracking population with every instance
        Creature.population += 1

    def mutate(self, chance):
        if chance < self.mutChance:
            trait = random.randint(1, 3)
            plus = random.randint(1, 2)
            if trait == 1:
                if plus == 1:
                    self.mutChance *= (1 + self.mutAmount)
                else:
                    self.mutChance -= self.mutChance * self.mutAmount
            elif trait == 2:
                if plus == 1:
                    self.repChance *= (1 + self.mutAmount)
                else:
                    self.repChance -= self.repChance * self.mutAmount
            else:
                if plus == 1:
                    self.deathChance *= (1 + self.mutAmount)
                else:
                    self.deathChance -= self.deathChance * self.mutAmount
        else:
            pass

    # Reproduction function
    def reproduce(self, chance):
        if chance <= self.repChance:
            creatures_buffer.append(Creature(self.repChance, self.deathChance, self.mutChance, self.mutAmount))
        else:
            pass

    # Death function
    def die(self, chance):
        if chance <= self.deathChance:
            self.status = 'dead'
            Creature.population -= 1
            Creature.deaths += 1
        else:
            pass

    # Live function to run reproduction and death simultaneously
    def live(self):
        chance = random.uniform(0, 100)
        self.reproduce(chance)
        chance = random.uniform(0, 100)
        self.die(chance)
        chance = random.uniform(0, 100)
        self.mutate(chance)


# Setting up CSV information
file = open("evolution.csv", 'w')
headers = ["Time Step", "Population", "Deaths", "Average Reproduction", "Average Death", "Average Mutation"]
writer = csv.DictWriter(file, fieldnames=headers)
writer.writeheader()

# Populating with initial creature population
for _ in range(initial_pop):
    creatures.append(Creature(repChance, deathChance, mutChance, mutAmount))

# Starting sim
counter = 0
for time_step in range(1, time_steps):
    for creature in creatures:
        if creature.status == 'alive':
            # Getting stat data for this specific time step
            average_rep += creature.repChance
            average_death += creature.deathChance
            average_mut += creature.mutChance
            counter += 1
            # Letting creature live if it is not dead
            creature.live()
        else:
            pass

    average_rep /= counter
    average_death /= counter
    average_mut /= counter

    # Appending the buffer and resetting it
    for creature in creatures_buffer:
        creatures.append(creature)

    creatures_buffer = []

    # Writing info to CSV
    writer.writerow({"Time Step": time_step,
                     "Population": Creature.population,
                     "Deaths": Creature.deaths,
                     "Average Reproduction": average_rep,
                     "Average Death": average_death,
                     "Average Mutation": average_mut})

    # Printing important info
    print(f"Time Step: {time_step}")
    print(f"Population: {Creature.population}")
    print(f"Deaths: {Creature.deaths}")
    print(f"Average reproduction stat: {average_rep}")
    print(f"Average death stat: {average_death}")
    print(f"Average mutation stat: {average_mut}")
    print(f"Creatures in list: {len(creatures)}")
    print("---------------------------------------------")
    average_rep = 0
    average_death = 0
    average_mut = 0
    Creature.deaths = 0
    counter = 0
