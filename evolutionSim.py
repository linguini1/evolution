# Evolution simulator

import random
import csv
from matplotlib import pyplot as plt

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
data = [[], [], [], [], [], []]
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


# Getting valid input
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

# Asking for export to CSV
while True:
    csv_exp = input("Do you want to export data to a CSV? (y/n): ")
    if csv_exp.lower() == 'yes' or csv_exp.lower() == 'y':
        csv_exp = True
        file = open("evolution.csv", 'w')
        headers = ["Time Step", "Population", "Deaths", "Average Reproduction", "Average Death", "Average Mutation"]
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        break
    elif csv_exp.lower() == 'no' or csv_exp.lower() == 'n':
        csv_exp = False
        break
    else:
        print("Invalid input.")

# Asking for console printing
while True:
    cons_out = input("Do you want to print data to console? (y/n): ")
    if cons_out.lower() == 'yes' or cons_out.lower() == 'y':
        cons_out = True
        break
    elif cons_out.lower() == 'no' or cons_out.lower() == 'n':
        cons_out = False
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

    # Writing to list
    data[0].append(time_step)
    data[1].append(Creature.population)
    data[2].append(Creature.deaths)
    data[3].append(average_rep)
    data[4].append(average_death)
    data[5].append(average_mut)

    # Writing info to CSV
    if csv_exp:
        writer.writerow({"Time Step": time_step,
                         "Population": Creature.population,
                         "Deaths": Creature.deaths,
                         "Average Reproduction": average_rep,
                         "Average Death": average_death,
                         "Average Mutation": average_mut})

    # Printing to console
    if counter % 2 == 0 and not cons_out:
        print(f"{str(time_step / time_steps * 100)[0:2]}% complete.")

    if cons_out:
        print(f"Time Step: {time_step}")
        print(f"Population: {Creature.population}")
        print(f"Deaths: {Creature.deaths}")
        print(f"Average reproduction stat: {average_rep}")
        print(f"Average death stat: {average_death}")
        print(f"Average mutation stat: {average_mut}")
        print(f"Creatures in list: {len(creatures)}")
        print("---------------------------------------------")

    # Resetting values
    average_rep = 0
    average_death = 0
    average_mut = 0
    Creature.deaths = 0
    counter = 0

# Closing CSV
if csv_exp:
    file.close()

# Plotting data
fig, axs = plt.subplots(2)
plt.tight_layout()

# Populations vs Deaths
axs[0].set_title("Population vs Deaths")
axs[0].plot(data[0], data[1], label='Population')
axs[0].plot(data[0], data[2], label='Deaths')
axs[0].set_xlabel("Time Step")
axs[0].set_ylabel('# of Creatures')
axs[0].legend()

# Stat Change
axs[1].set_title("Stat Changes")
axs[1].plot(data[0], data[3], label='Reproduction')
axs[1].plot(data[0], data[4], label='Death')
axs[1].plot(data[0], data[5], label='Mutation')
axs[1].set_xlabel("Time Step")
axs[1].set_ylabel('Stat %')
axs[1].legend()

plt.show()
