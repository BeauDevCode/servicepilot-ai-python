from app.database import init_db
from app.seed_data import seed_demo_data

if __name__ == "__main__":
    init_db()
    seed_demo_data()
    print("Seeded ServicePilot AI demo data.")

