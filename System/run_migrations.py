import subprocess

def run_makemigrations():
    try:
        subprocess.run(['python3', 'manage.py', 'makemigrations'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running 'makemigrations': {e}")
    else:
        print("Migrations created successfully.")

def run_migrate():
    try:
        subprocess.run(['python3', 'manage.py', 'migrate'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running 'migrate': {e}")
    else:
        print("Database migration successful.")

if __name__ == "__main__":
    run_makemigrations()
    run_migrate()

