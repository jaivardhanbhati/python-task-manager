import hashlib
import os
import uuid

# users list # 
USERS_FILE = "users.txt"

# encrypted password #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# registeration flow #
def register():
    username = input("Enter a new username: ").strip()
    password = input("Enter a new password: ").strip()

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                stored_user = line.strip().split(",")[0]
                if username == stored_user:
                    print("Username already exists. Try a different one.")
                    return None

    hashed = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{hashed}\n")
    print("Registration successful!")
    return username

# login #
def login():
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    encryptedPwd = hash_password(password)

    if not os.path.exists(USERS_FILE):
        print("No users registered yet.")
        return None

    with open(USERS_FILE, "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split(",")
            if username == stored_user and encryptedPwd == stored_hash:
                print("Login successful!")
                return username

    print("Invalid username or password.")
    return None


def get_task_file(username):
    return "tasks_{username}.txt"


def add_task(username):
    desc = input("Enter task description: ").strip()
    task_id = str(uuid.uuid4())[:8]
    with open(get_task_file(username), "a") as f:
        f.write(f"{task_id}|{desc}|Pending\n")
    print(f"Task '{desc}' added with ID {task_id}.")


def view_tasks(username):
    print("\nYour Tasks:")
    print("ID        | Description                 | Status")
    # print("-" * 50)
    try:
        with open(get_task_file(username), "r") as f:
            for line in f:
                task_id, desc, status = line.strip().split("|")
                print(f"{task_id:<10}| {desc:<25}| {status}")
    except FileNotFoundError:
        print("No tasks found.")


def mark_task_completed(username):
    task_id = input("Enter the Task ID to mark as completed: ").strip()
    tasks = []
    found = False

    try:
        with open(get_task_file(username), "r") as f:
            for line in f:
                tid, desc, status = line.strip().split("|")
                if tid == task_id:
                    tasks.append(f"{tid}|{desc}|Completed\n")
                    found = True
                else:
                    tasks.append(line)
        if found:
            with open(get_task_file(username), "w") as f:
                f.writelines(tasks)
            print("Task marked as completed.")
        else:
            print("Task ID not found.")
    except FileNotFoundError:
        print("No tasks to update.")


def delete_task(username):
    task_id = input("Enter the Task ID to delete: ").strip()
    tasks = []
    deleted = False

    try:
        with open(get_task_file(username), "r") as f:
            for line in f:
                tid, desc, status = line.strip().split("|")
                if tid == task_id:
                    deleted = True
                else:
                    tasks.append(line)
        if deleted:
            with open(get_task_file(username), "w") as f:
                f.writelines(tasks)
            print("Task deleted.")
        else:
            print("Task ID not found.")
    except FileNotFoundError:
        print("No tasks to delete.")


def task_menu(username):
    while True:
        print("\n--- Task Manager ---")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete a Task")
        print("5. Logout")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_task_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.")


def main():
    print("=== Welcome to Task Manager ===")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            user = register()
            if user:
                task_menu(user)
        elif choice == "2":
            user = login()
            if user:
                task_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Try again.")


if __name__ == "__main__":
    main()