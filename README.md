Run BeingsCreator.py - each "y" input will generate a being and tell you its unique beingid, if it is human, and its sex/age/weight
Your first being will initialize the beings.db database, and all beings will be committed to this database
BeingsReader.py will query the entire beings.db database except for the ishuman values. It will try to guess whether each being is human or not based on the other attributes.
A new column "guessed_ishuman" will be added to the db with the guess values.
Once the whole database has been evaluated, it will tell you what percentage of beings it guessed correctly on.
