from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Years, Base, Games, User

engine = create_engine('sqlite:///Wildcat.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

User1 = User(name='John Calipari', email='JCalipari@myemail.com', picture=
'https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Year 2005-06
year1 = Years(user_id=1, yearmonth="2005-06")

session.add(year1)
session.commit()

games2 = Games(user_id=1, opponent="South Dakota State", description="arena - Rupp Arena final - Win  71-54",
            year=year1)

session.add(games2)
session.commit()


games1 = Games(user_id=1, opponent="Lipscomb", description="arena - Rupp Arena final - Win  71-54", year=year1)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="Lipscomb", description="arena - Rupp Arena final - Win  71-54", year=year1)

session.add(games2)
session.commit()

games3 = Games(user_id=1, opponent="Iowa", description="arena - Municipal Auditorium final - Loss  63-67", year=year1)

session.add(games3)
session.commit()

games4 = Games(user_id=1, opponent="West Virginia", description="arena - Municipal Auditorium final - Win  80-66", year=year1)

session.add(games4)
session.commit()

games5 = Games(user_id=1, opponent="Liberty", description="arena - Rupp Arena final - Win  81-51", year=year1)

session.add(games5)
session.commit()

games6 = Games(user_id=1, opponent="High Point", description="arena - Rupp Arena final - Win  75-55", year=year1)

session.add(games6)
session.commit()

games7 = Games(user_id=1, opponent="North Carolina", description="arena - Rupp Arena final - Loss  79-83", year=year1)

session.add(games7)
session.commit()

games8 = Games(user_id=1, opponent="Georgia State", description="arena - Philips Arena final - Win  73-46", year=year1)

session.add(games8)
session.commit()


# 2006-07
year2 = Years(user_id=1, yearmonth="2006-07")

session.add(year2)
session.commit()


games1 = Games(user_id=1, opponent="Miami (OH)", description="arena - Rupp Arena final - Win  57-46", year=year2)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="Mississippi Valley State", description="arena - Rupp Arena final - Win  79-56", year=year2)

session.add(games2)
session.commit()

games3 = Games(user_id=1, opponent="DePaul", description="arena - Lahaina Civic Center final - Win  87-81", year=year2)

session.add(games3)
session.commit()

games4 = Games(user_id=1, opponent="UCLA", description="arena - Lahaina Civic Center final - Loss  68-73", year=year2)

session.add(games4)
session.commit()

games5 = Games(user_id=1, opponent="Memphis", description="arena - Lahaina Civic Center final - Loss  63-80", year=year2)

session.add(games5)
session.commit()

games6 = Games(user_id=1, opponent="Coll. of Charleston", description="arena - Rupp Arena final - Win  77-61", year=year2)

session.add(games6)
session.commit()

games7 = Games(user_id=1, opponent="North Carolina", description="arena - Dean Smith Center final - Loss  63-75", year=year2)

session.add(games7)
session.commit()

games8 = Games(user_id=1, opponent="Tenn-Chattanooga", description="arena - Freedom Hall final - Win  77-61", year=year2)

session.add(games8)
session.commit()


# 2007-08
year1 = Years(user_id=1, yearmonth="2007-08")

session.add(year1)
session.commit()


games1 = Games(user_id=1, opponent="Central Arkansas", description="arena - Rupp Arena final - Win  67-40", year=year1)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="Gardner-Webb", description="arena - Rupp Arena final - Loss  68-84", year=year1)

session.add(games2)
session.commit()

games3 = Games(user_id=1, opponent="Liberty", description="arena - Rupp Arena final - Win  80-54", year=year1)

session.add(games3)
session.commit()

games4 = Games(user_id=1, opponent="Texas Southern", description="arena - Rupp Arena final - Win  83-35", year=year1)

session.add(games4)
session.commit()

games5 = Games(user_id=1, opponent="Stony Brook", description="arena - Rupp Arena final - Win  62-52", year=year1)

session.add(games5)
session.commit()

games6 = Games(user_id=1, opponent="North Carolina", description="arena - Rupp Arena final - Loss  77-86", year=year1)

session.add(games6)
session.commit()

games7 = Games(user_id=1, opponent="Indiana", description="arena - Assembly Hall (IU) final - Loss  51-70", year=year1)

session.add(games7)
session.commit()

games8 = Games(user_id=1, opponent="Alabama-Birmingham", description="arena - Freedom Hall final - Loss  76-79", year=year1)

session.add(games8)
session.commit()


# 2008-09
year1 = Years(user_id=1, yearmonth="2008-09")

session.add(year1)
session.commit()


games1 = Games(user_id=1, opponent="Virginia Military", description="arena - Rupp Arena final - Loss  103-111", year=year1)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="North Carolina", description="arena - Dean Smith Center final - Loss  58-77", year=year1)

session.add(games2)
session.commit()

games3 = Games(user_id=1, opponent="Delaware State", description="arena - Rupp Arena final - Win  71-42", year=year1)

session.add(games3)
session.commit()

games4 = Games(user_id=1, opponent="Longwood", description="arena - Rupp Arena final - Win  91-57", year=year1)

session.add(games4)
session.commit()

games5 = Games(user_id=1, opponent="Kansas State", description="arena - Orleans Arena final - Win  74-72", year=year1)

session.add(games5)
session.commit()

games6 = Games(user_id=1, opponent="West Virginia", description="arena - Orleans Arena final - Win  54-43", year=year1)

session.add(games6)
session.commit()

games7 = Games(user_id=1, opponent="Lamar", description="arena - Rupp Arena final - Win  103-61", year=year1)

session.add(games7)
session.commit()

games8 = Games(user_id=1, opponent="Miami", description="arena - Rupp Arena final - Loss  67-73", year=year1)

session.add(games8)
session.commit()

games9 = Games(user_id=1, opponent="Mississippi Valley State", description="arena - Rupp Arena final - Win  88-65", year=year1)

session.add(games9)
session.commit()

games10 = Games(user_id=1, opponent="Indiana", description="arena - Rupp Arena final - Win  72-54", year=year1)

session.add(games10)
session.commit()


# 2009-10
year1 = Years(user_id=1, yearmonth="2009-10")

session.add(year1)
session.commit()


games1 = Games(user_id=1, opponent="Morehead", description="arena - Rupp Arena final - Win  75-59", year=year1)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="Miami (OH)", description="arena - Rupp Arena final - Win  72-70", year=year1)

session.add(games2)
session.commit()

games3 = Games(user_id=1, opponent="Sam Houston State", description="arena - Rupp Arena final - Win  102-92", year=year1)

session.add(games3)
session.commit()

games4 = Games(user_id=1, opponent="Rider", description="arena - Rupp Arena final - Win  92-63", year=year1)

session.add(games4)
session.commit()

games5 = Games(user_id=1, opponent="Cleveland State", description="arena - Moon Palace Ballroom final - Win  73-49", year=year1)

session.add(games5)
session.commit()

games6 = Games(user_id=1, opponent="Stanford", description="arena - Moon Palace Ballroom final - Win  73-65", year=year1)
session.add(games6)
session.commit()

games7 = Games(user_id=1, opponent="UNC Asheville", description="arena - Freedom Hall final - Win  94-57", year=year1)

session.add(games7)
session.commit()

games8 = Games(user_id=1, opponent="North Carolina", description="arena - Rupp Arena final - Win  68-66", year=year1)

session.add(games8)
session.commit()


# 2010-11
year1 = Years(user_id=1, yearmonth="2010-11")

session.add(year1)
session.commit()


games1 = Games(user_id=1, opponent="East Tennessee State", description="arena - Rupp Arena final - Win  88-65", year=year1)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="Portland", description="arena - Rose Garden final - Win  79-48", year=year1)

session.add(games2)
session.commit()

games3 = Games(user_id=1, opponent="Oklahoma", description="arena - Lahaina Civic Center final - Win  76-64", year=year1)

session.add(games3)
session.commit()

games4 = Games(user_id=1, opponent="Washington", description="arena - Lahaina Civic Center final - Win  74-67", year=year1)

session.add(games4)
session.commit()

games5 = Games(user_id=1, opponent="Connecticut", description="arena - Lahaina Civic Center final - Loss  67-84", year=year1)

session.add(games5)
session.commit()


# 2011-12
year1 = Years(user_id=1, yearmonth="2011-12")

session.add(year1)
session.commit()

games1 = Games(user_id=1, opponent="Marist", description="arena - Rupp Arena final - Win  108-58", year=year1)

session.add(games1)
session.commit()

games1 = Games(user_id=1, opponent="Kansas", description="arena - Madison Square Garden final - Win  75-65", year=year1)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="Penn State", description="arena - Mohegan Sun Arena final - Win  85-47", year=year1)

session.add(games2)
session.commit()

games3 = Games(user_id=1, opponent="Old Dominion", description="arena - Mohegan Sun Arena final - Win  62-52", year=year1)

session.add(games3)
session.commit()

games4 = Games(user_id=1, opponent="Radford", description="arena - Rupp Arena final - Win  88-40", year=year1)

session.add(games4)
session.commit()

games2 = Games(user_id=1, opponent="Portland", description="arena - Rupp Arena final - Win  87-63", year=year1)

session.add(games2)
session.commit()

games10 = Games(user_id=1, opponent="St. Johns", description="arena - Rupp Arena final - Win  81-59", year=year1)

session.add(games10)
session.commit()


# 2012-13
year1 = Years(user_id=1, yearmonth="2012-13")

session.add(year1)
session.commit()


games1 = Games(user_id=1, opponent="Maryland", description="arena - Barclays Center final - Win  72-69", year=year1)

session.add(games1)
session.commit()

games2 = Games(user_id=1, opponent="Duke", description="arena - Georgia Dome final - Loss  68-75", year=year1)

session.add(games2)
session.commit()

games1 = Games(user_id=1, opponent="Lafayette", description="arena - Rupp Arena final - Win  101-49", year=year1)

session.add(games1)
session.commit()

games1 = Games(user_id=1, opponent="Morehead", description="arena - Rupp Arena final - Win  81-70", year=year1)

session.add(games1)
session.commit()


games1 = Games(user_id=1, opponent="Long Island", description="arena - Rupp Arena final - Win  104-75", year=year1)

session.add(games1)
session.commit()


print "added games!"
