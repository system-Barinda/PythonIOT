import os
from src.core.config import DATABASE_URL


def main():
    print("ENV DATABASE_URL:", os.getenv("DATABASE_URL"))

    print("CONFIG DATABASE_URL:", DATABASE_URL)

if __name__ == "__main__":
    main()
