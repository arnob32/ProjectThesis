
class AuthService:
    def __init__(self):
        self.users = []

    def signup(self, data: dict):
        self.users.append(data)
        print("✅ New user signed up!")
        print("📋 Current Users List:")
        for u in self.users:
            print(u)   # 👈 each user printed in terminal
        return {"status": "success", "user": data}


    def signup(self, data: dict):
        # simple mock signup
        self.users.append(data)
        return {"status": "success", "user": data}

    def login(self, email: str, password: str):
        for user in self.users:
            if user["email"] == email and user["password"] == password:
                return {"status": "success", "role": user["role"]}
        return {"status": "failed", "message": "Invalid credentials"}
