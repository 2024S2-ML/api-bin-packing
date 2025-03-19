from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Shirt, ShirtRects, Base

engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(bind=engine)

def populate_data():
    with Session(bind=engine) as db:

        # Define the data for each shirt
        shirts_data = [
            {
                "type": "P",
                "size": "P",
                "rects": [
                    {"width": 67, "height": 48},
                    {"width": 67, "height": 48},
                    {"width": 70, "height": 58},
                    {"width": 50, "height": 20},
                    {"width": 50, "height": 20},
                    {"width": 21, "height": 15},
                    {"width": 21, "height": 15},
                    {"width": 20, "height": 9},
                    {"width": 20, "height": 9},
                    {"width": 20, "height": 9},
                    {"width": 20, "height": 9},
                ]
            },
            {
                "type": "M",
                "size": "M",
                "rects": [
                    {"width": 67, "height": 49},
                    {"width": 67, "height": 49},
                    {"width": 71, "height": 60},
                    {"width": 52, "height": 20},
                    {"width": 52, "height": 20},
                    {"width": 21, "height": 15},
                    {"width": 21, "height": 15},
                    {"width": 20, "height": 10},
                    {"width": 20, "height": 10},
                    {"width": 20, "height": 10},
                    {"width": 20, "height": 10},
                ]
            },
            {
                "type": "G",
                "size": "G",
                "rects": [
                    {"width": 68, "height": 50},
                    {"width": 68, "height": 50},
                    {"width": 73, "height": 62},
                    {"width": 54, "height": 20},
                    {"width": 54, "height": 20},
                    {"width": 21, "height": 15},
                    {"width": 21, "height": 15},
                    {"width": 21, "height": 11},
                    {"width": 21, "height": 11},
                    {"width": 21, "height": 11},
                    {"width": 21, "height": 11},
                ]
            }
        ]


        for shirt_data in shirts_data:

            shirt = Shirt(type=shirt_data["type"], size=shirt_data["size"])
            db.add(shirt)
            db.commit()
            db.refresh(shirt)


            for rect_data in shirt_data["rects"]:
                rect = ShirtRects(width=rect_data["width"], height=rect_data["height"], shirt_id=shirt.id)
                db.add(rect)
            db.commit()

        # Close the database session
        db.close()


if __name__ == "__main__":
    populate_data()