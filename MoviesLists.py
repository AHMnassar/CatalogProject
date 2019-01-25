from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DB_setup import Year, Base, CatalogItem, User

engine = create_engine('sqlite:///Movies.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create a user
User1 = User(name="Ahmed Nassar", email="ananassar13@gmail.com")
session.add(User1)
session.commit()

# catalog for year 2000
year1 = Year(user_id=1, name="2000")

session.add(year1)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="American Psycho", description="A wealthy New York City investment banking executive, hides his alternate psychopathic ego",
                     theme="crime", year=year1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="The Beach", description="Vicenarian Richard travels to Thailand and finds himself in possession of a strange map",
                     theme="adventure", year=year1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Cast Away ", description="A FedEx executive must transform himself physically and emotionally to survive a crash landing on a deserted island.",
                     theme="adventure", year=year1)

session.add(catalogItem3)
session.commit()


# catalog for year 2001
year2 = Year(name="2001")

session.add(year2)
session.commit()


catalogItem1 = CatalogItem(name="The Lord of the Rings: The Fellowship of the Ring", description="A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
                     theme="fantasy", year=year2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Spirited Away", description=" a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
                     theme="animation", year=year2)

session.add(catalogItem2)
session.commit()


# catalog for year 2002
year3 = Year(name="2002")

session.add(year3)
session.commit()


catalogItem1 = CatalogItem(name="Harry Potter and the Chamber of Secrets", description="An ancient prophecy seems to be coming true when a mysterious presence begins stalking the corridors of a school of magic and leaving its victims paralyzed.",
                     theme="fantasy", year=year3)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="The Lord of the Rings: The Two Towers", description="While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron's new ally, Saruman, and his hordes of Isengard.",
                     theme="fantasy", year=year3)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="The Pianist", description="A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto of World War II.",
                     theme="drama", year=year3)

session.add(catalogItem3)
session.commit()

# catalog for year 2003
year4 = Year(name="2003")

session.add(year4)
session.commit()


catalogItem1 = CatalogItem(name="The Lord of the Rings: The Return of the King", description="Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
                     theme="fantasy", year=year4)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Mystic River", description="The lives of three men who were childhood friends are shattered when one of them has a family tragedy.",
                     theme="crime", year=year4)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Pirates of the Caribbean: The Curse of the Black Pearl", description="Jack Sparrow to save his love, the governor's daughter, from Jack's former pirate allies, who are now undead.",
                     theme="adventure", year=year4)

session.add(catalogItem3)
session.commit()

# catalog for year 2004
year5 = Year(name="2004")

session.add(year5)
session.commit()


catalogItem1 = CatalogItem(name="Harry Potter and the Prisoner of Azkaban", description="It's Harry's third year at Hogwarts; not only does he have a new teacher, but there is also trouble brewing.",
                     theme="fantasy", year=year5)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="The Incredibles", description="A family of undercover superheroes, while trying to live the quiet suburban life, are forced into action to save the world.",
                     theme="animation", year=year5)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Troy", description="An adaptation of Homer's great epic, the film follows the assault on Troy by the united Greek forces and chronicles the fates of the men involved.",
                     theme="history", year=year5)

session.add(catalogItem3)
session.commit()

# catalog for year 2005
year6 = Year(name="2005")

session.add(year6)
session.commit()


catalogItem1 = CatalogItem(name="King Kong", description="Kong, a giant ape who is immediately smitten with leading lady Ann Darrow.",
                     theme="drama", year=year6)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Kingdom of Heaven", description="Balian of Ibelin travels to Jerusalem during the Crusades of the 12th century, and there he finds himself as the defender of the city and its people.",
                     theme="action", year=year6)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Fantastic Four", description="A group of astronauts gain superpowers after a cosmic radiation exposure and must use them to oppose the plans of their enemy",
                     theme="action", year=year6)

session.add(catalogItem3)
session.commit()

print "added catalog items!"