class User:
    def __init__(self, name):
        print(f"Creating a user named {name}")

        self.data = {}
        self.data["name"] = name
