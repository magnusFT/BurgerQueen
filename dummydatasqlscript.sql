-- Sett inn brukere
INSERT INTO Brukere (Navn, Passord, Ansatt) VALUES
('Geralt', 'hesterbest', 'Nei'),
('Yennefer', 'qwerty', 'Nei'),
('Roach', 'pizza', 'Nei'),
('Jaskier', 'nyttpassord', 'Ja');

-- Sett inn burgere
INSERT INTO Burgere (Navn, Ingredienser) VALUES
('Whopper Queen', 'Burgerbrød, burgerkjøtt, salat, tomat'),
('Triple Cheesy Princess', 'Burgerbrød, burgerkjøtt, ost, salat, tomat'),
('Kingdom Fries', 'Potet');

-- Sett inn ordre
INSERT INTO Ordre (Hvem, Hva, Produsert) VALUES
('Geralt', 'Whopper Queen', 'Ja'),
('Geralt', 'Whopper Queen', 'Nei'),
('Jaskier', 'Triple Cheesy Princess', 'Nei'),
('Roach', 'Whopper Queen', 'Nei');

-- Sett inn ingredienser
INSERT INTO Ingredienser (Ingrediens, "Hvor mye") VALUES
('Burgerbrød topp og bunn', 9001),
('Burgerkjøtt', 10),
('Salat', 8008),
('Tomat', 1337),
('Ost', 42),
('Agurk', 666),
('Potet', 420);
