-- INSERT INTO Movies(title, year, description)
--                 VALUES("Interstellar", 2014, "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage."),
--                         ("Fight Club", 1999, "A ticking time bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. Their concept catches on, with underground fight clubs forming in every town, until an eccentric gets in the way and ignites an out of control spiral toward oblivion."),
--                         ("The Dark Knight", 2008, "When a menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman, James Gordon and Harvey Dent must work together to put an end to the madness.");

-- INSERT INTO Users(username, password)
--                 VALUES("Derek", "password1"),
--                         ("Erika", "password2");

INSERT INTO Reviews(Date, Review, Rating, MovieID, UserID)
                VALUES(CURRENT_DATE, "Greatest movie ever made, incredible in every aspect.", 5, 1, 1),
                        (CURRENT_DATE, "Flawless film.", 5, 1, 2),
                        (CURRENT_DATE, "Emotionally powerful media from start to finish, amazing plot twist.", 5, 2, 1),
                        (CURRENT_DATE, "Near perfect film with amazing direction/storytelling, tied together with amazing cast.", 5, 3, 2);