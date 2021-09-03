
class GameLoop:
    def __init__(self):
        print("Creating a Fragments Game Loop")

        self.t = 0
        self.TPS = 20

    def tick(self):
        print("ticking")

    # [TODO] Utilize epoch checks for time deltas instead of utilizing tick count (which could be incorrect due to many reasons)
    def tick(self):
        # Pretend to give exp to users
        for user in LocalData.records:
            LocalData.records[user]["exp"] += 10

        t += 1
        if t % (TPS * 60) == 0: LocalData.save()

        time.sleep(1.0 / TPS)    # Find a way to sleep yet only for the required duration, presuming all tick calculations have been met