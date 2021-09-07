SET datestyle TO 'DMY';
INSERT INTO users VALUES ('commitee','commitee','commitee');


SELECT new_voter(1,'Marcin','Lit');
SELECT new_voter(2,'Barbara','Beryl');
SELECT new_voter(3,'Dawid','Sod');
SELECT new_voter(4,'Bartlomiej','Magnez');
SELECT new_voter(5,'Danuta','Potas');
SELECT new_voter(6,'Weronika','Wapn');
SELECT new_voter(7,	'Andrzej', 'Tytan');
SELECT new_voter(8, 'Helena', 'Chrom');
SELECT new_voter(9, 'Gabriela', 'Mangan');
SELECT new_voter(10, 'Sebastian', 'Zelazo');
SELECT new_voter(11, 'Beata', 'Kobalt');
SELECT new_voter(12, 'Cezary', 'Nikiel');
SELECT new_voter(13, 'Katarzyna', 'Miedz');
SELECT new_voter(14, 'Michal', 'Cynk');
SELECT new_voter(15, 'Wlodznamerz', 'Pallad');
SELECT new_voter(16, 'Jacek', 'Kadm');
SELECT new_voter(17, 'Justyna', 'Cyna');
SELECT new_voter(18, 'Krzysztof', 'Cez');
SELECT new_voter(19, 'Mikolaj', 'Bar');
SELECT new_voter(20, 'Jan', 'Wolfram');
SELECT new_voter(21, 'Tomasz', 'Iryd');
SELECT new_voter(22, 'Anna', 'Platyna');
SELECT new_voter(23, 'Aleksandra', 'Zloto');
SELECT new_voter(24, 'Marta', 'Rtec');
SELECT new_voter(25, 'Marcel', 'Tal');
SELECT new_voter(26, 'Grzegorz', 'Olow');
SELECT new_voter(27,	'Maria', 'Rad');
SELECT new_voter(28, 'Piotr', 'Uran');
SELECT new_voter(29, 'Laura', 'Srebro');


SELECT new_election('finished',3,'02-04-2021','05-04-2021','07-04-2021');

INSERT INTO candidate VALUES ('finished',2);
INSERT INTO candidate VALUES ('finished',3);
INSERT INTO candidate VALUES ('finished',4);
INSERT INTO candidate VALUES ('finished',1);
INSERT INTO candidate VALUES ('finished',11);
INSERT INTO candidate VALUES ('finished',13);


INSERT INTO vote VALUES ('finished',1,2);
INSERT INTO vote VALUES ('finished',2,3);
INSERT INTO vote VALUES ('finished',3,4);
INSERT INTO vote VALUES ('finished',4,2);
INSERT INTO vote VALUES ('finished',5,3);
INSERT INTO vote VALUES ('finished',6,4);
INSERT INTO vote VALUES ('finished',7,4);
INSERT INTO vote VALUES ('finished',8,4);
INSERT INTO vote VALUES ('finished',9,3);
INSERT INTO vote VALUES ('finished',10,1);
INSERT INTO vote VALUES ('finished',11,11);
INSERT INTO vote VALUES ('finished',12,13);


SELECT new_election('current',4,'04-09-2021','06-09-2021','01-10-2021');

INSERT INTO candidate VALUES ('current',5);
INSERT INTO candidate VALUES ('current',7);
INSERT INTO candidate VALUES ('current',8);
INSERT INTO candidate VALUES ('current',9);
INSERT INTO candidate VALUES ('current',23);
INSERT INTO candidate VALUES ('current',24);
INSERT INTO candidate VALUES ('current',27);
INSERT INTO candidate VALUES ('current',26);

SELECT new_election('future',3,'06-10-2021','07-10-2021','08-10-2021');