#!/usr/bin/env python3
"""Print books linked to selected authors in MongoDB Atlas."""

import logging
import os

import pymongo
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

# Read credentials from the shell environment.
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")


def main():
    """Connect to Atlas, print the author report, and close the client."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    client = None

    try:
        # Validate credentials before connecting.
        if not all([
            MONGODB_ATLAS_URL,
            MONGODB_ATLAS_USER,
            MONGODB_ATLAS_PWD,
        ]):
            raise ValueError("One or more Atlas environment variables are missing.")

        # Open the client using credentials from environment variables.
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            authSource="admin",
            server_api=ServerApi("1"),
            serverSelectionTimeoutMS=10000,
        )

        # Verify the connection before reporting success.
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas.")

        # Select the existing database and collections.
        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        # Include two loaded authors and Charlotte Bronte.
        author_ids = ["author_002", "author_003", "author_bronte"]
        author_filter = {"_id": {"$in": author_ids}}
        author_count = authors.count_documents(author_filter)
        print(f"Authors: {author_count}\n")

        # Find each author's books through the author_ids field.
        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning("Author not found: %s", author_id)
                continue

            print(author["name"])
            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")
            print()

    except (PyMongoError, ValueError) as error:
        logging.error("Could not generate the report: %s", error)
        raise SystemExit(1)

    finally:
        # Close the client even when an operation fails.
        if client is not None:
            client.close()
            logging.info("MongoDB client closed.")


if __name__ == "__main__":
    main()
