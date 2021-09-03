import time
import math
import random
import threading

class Fragment_Item:
    def __init__(self, name = "Default Item"):
        self.name = name

    def tick(self):
        pass

class Fragment_Skill:
    def __init__(self, name = "Default Skill", level = 1):
        self.name = name
        self.exp = 0

        self.output = []

    # Decided to use OSRS' leveling system
    # https://oldschool.runescape.wiki/w/Experience
    # [TODO] Rewrite this function as a sum() equation instead
    def expForLevel(level):
        total = 0
        for i in range(1, level):
            total += math.floor(i + 300 * math.pow(2, i / 7.0))
        return math.floor(total / 4)

    def level(self):
        retVal = 1
        while self.exp > Fragment_Skill.expForLevel(retVal + 1):
            retVal += 1
        return retVal

    def tick(self):
        raise ValueError("Ensure skill tick() is overwritten")

    def render(self, prefix = ""):
        print(f"{prefix}Skill: Lvl {self.level()} {self.name} [{self.exp}/{Fragment_Skill.expForLevel(self.level() + 1)}]")

class Fragment_Skill_Foraging(Fragment_Skill):
    def __init__(self):
        super().__init__()

        self.name = "Foraging"

    def tick(self):
        chance = 50
        val = random.randint(1, chance)
        if val == chance:
            item = Fragment_Item()
            self.output.append(item)

class Fragment_Unit:
    def __init__(self, name = "Default Unit", ID = 0):
        self.ID = ID
        self.name = name

        # Base stats
        #self.stats = []
        #self.agility = 1
        #self.construction = 1
        #self.intelligence = 1
        #self.strength = 1

        # Skills
        self.skills = []
        self.activeSkill = None

        self.skills.append(Fragment_Skill_Foraging())
        self.setActiveSkill("Foraging")

    def setActiveSkill(self, name):
        if name == "None" or name == "Inactive":
            self.activeSkill = None
            return

        skill = None
        for s in self.skills:
            if s.name == name: skill = s
        if skill is not None:
            self.activeSkill = skill
        else: print("Unit does not know that skill")

    def tick(self):
        if self.activeSkill != None:
            self.activeSkill.tick()

            for item in self.activeSkill.output:
                print(f"{self.name} found {item.name} while {self.activeSkill.name}")

    def render(self):
        activity = "Inactive"
        if self.activeSkill is not None: activity = self.activeSkill.name
        print(f"Unit ID {self.ID}: {self.name} -> {activity}")
        for skill in self.skills:
            skill.render(prefix = "\t")

class Fragments:
    def __init__(self):
        self.TPS = 20
        self.units = []
        self.warehouse = []

        # [TESTING]
        unit = Fragment_Unit()
        self.addUnit(unit)

        # [TODO/BUG] This thread is never properly killed and hangs innapropriately
        threading.Thread(target = self.gameLoop).start()
        self.userInterface()

    def genUnitID(self):
        retVal = random.randint(1000, 9999)    # [BUG] This range is hardcoded, this fails if we have too many available units
        available = True
        for unit in self.units:
            if unit.ID == retVal: return self.genUnitID()
        return retVal

    def unitByID(self, ID):
        for unit in self.units:
            if unit.ID == ID: return unit
        return None

    def userInterface(self):
        while True:
            command = input("Enter Input> ")

            commands = ["units", "unit add", "unit skill", "help"]

            if command == "units":
                if len(self.units) == 0: print("No Units")
                for unit in self.units: unit.render()
            elif command == "unit add":
                unit = Fragment_Unit(ID = self.genUnitID())
                self.addUnit(unit)
            elif command == "unit skill":
                ID = int(input("Unit ID: "))
                unit = self.unitByID(ID)
                if unit is not None:
                    activity = input("Activity: ")
                    unit.setActiveSkill(activity)
                else: print("Unit does not exist")
            elif command == "help":
                for command in commands: print(command)

    def addUnit(self, unit):
        print(f"Adding a unit")
        unit.ID = self.genUnitID()    # Ensure we have a unique identifier for every unit available
        self.units.append(unit)

    def tick(self):
        for unit in self.units:
            unit.tick()

            items = []
            # If any of our units have produced anything we take care of that now
            for skill in unit.skills:
                items = skill.output
                skill.output = []

            for item in items:
                self.warehouse.append(item)

    def gameLoop(self):
        while True:
            self.tick()
            time.sleep(1.0 / self.TPS)

fragments = Fragments()
