class UserDetails:
    def __init__(self):
        self.users = {}

    def add_user(self):
        member_id = input("Enter Member ID: ")
        name = input("Enter Name: ")
        lucky_number = int(input("Enter Lucky Number Preference: "))
        hobbies = input("Enter Hobbies (comma-separated): ").split(",")

        books = []
        num_books = int(input("How many books has the user read? "))
        for i in range(num_books):
            book_title = input("Enter book title: ")
            book_author = input("Enter book author: ")
            books.append({book_title: book_author})

        self.users[member_id] = {
            "name": name,
            "luckyNumberPreference": lucky_number,
            "hobbies": hobbies,
            "books": books
        }
        print("User added successfully!")

    def search_user(self):
        member_id = input("Enter Member ID to search: ")
        user = self.users.get(member_id)
        if user:
            print("User found successfully!")
            print(user)
        else:
            print("User not found.")

    def delete_user(self):
        member_id = input("Enter Member ID to delete: ")
        if member_id in self.users:
            del self.users[member_id]
            print("User deleted successfully!")
        else:
            print("User not found.")

    def list_of_users(self):
        if not self.users:
            print("No users available.")
            return
        for member_id, details in self.users.items():
            print(f"Member ID: {member_id}, Details: {details}")



userdetails = UserDetails()

while True:
    print("\n1. Add User\n2. Search User\n3. Delete User\n4. List Users\n5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        userdetails.add_user()
    elif choice == "2":
        userdetails.search_user()
    elif choice == "3":
        userdetails.delete_user()
    elif choice == "4":
        userdetails.list_of_users()
    elif choice == "5":
        print("Exiting the program...")
        break
    else:
        print("Invalid choice! Please try again.")