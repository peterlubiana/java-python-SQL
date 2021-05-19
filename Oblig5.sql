-- Oblig 5


-- komme inn på databasen: psql -h dbpg-ifi-kurs -U brukernavn -d brukernavn

-- Oppgave 0
SELECT COUNT(*) FROM film;


/*Oppgave 1
Skriv ut en tabell med to kolonner, først rollefigurnavn, så antall ganger dette rollefigurnavnet forekommer i filmcharacter-tabellen. Ta bare med navn som forekommer mer enn 2000 ganger. Sorter etter fallende hyppighet. (90/91 rader)
*/

select filmcharacter, count(filmcharacter) as occurences 
FROM filmcharacter fc 
group by filmcharacter 
having count(filmcharacter) > 2000 ORDER BY occurences DESC;
 






/*
Oppgave 2
Skriv ut filmtittel og produksjonsår for filmer som Stanley Kubrick har regissert («director»). (16 rader) Løs oppgaven med:
• 2a: INNER JOIN
• 2b: NATURAL JOIN
• 2c: Implisitt join
Tips: Personer som har deltatt i en film finnes i tabellen filmparticipation. Navn finnes i person.
*/


-- a)
Select title, prodyear 
from film f inner join filmparticipation fp on f.filmid = fp.filmid inner join person p on fp.personid = p.personid 
where fp.parttype LIKE 'director' AND p.firstname like 'Stanley' and p.lastname like 'Kubrick';

-- b)

Select title, prodyear 
from film f natural join filmparticipation fp natural join person p 
where fp.parttype like 'director' and p.firstname like 'Stanley' and p.lastname like 'Kubrick';

-- c) 
Select title, prodyear 
from film f, filmparticipation fp, person p 
WHERE f.filmid = fp.filmid and p.personid = fp.personid and fp.parttype LIKE 'director' AND p.firstname like 'Stanley' and p.lastname like 'Kubrick';









/*
Oppgave 3
Skriv ut personid og fullt navn til personer med fornavnet Ingrid (i person) som har spilt rollen Ingrid (i filmcharacter).
Fullt navn skal returneres i én kolonne, ved å konkatenere fornavn med etternavn på formatet «FORNAVN ETTERNAVN». 
Ta også med filmtittelen det gjelder og hvilket land filmen er produsert i (fra filmcountry). (14 rader)
*/

select distinct p.personid, CONCAT(p.firstname,' ',p.lastname) as name, f.title, c.country 
from person p inner join filmcharacter fc on p.firstname = fc.filmcharacter inner join filmparticipation fp on fc.partid = fp.partid natural join film f natural join filmcountry c 
where p.firstname = 'Ingrid' and p.personid = fp.personid and fp.parttype = 'cast';









/*
Oppgave 4
Skriv ut filmid, tittel og antall sjangrer (fra filmgenre) for filmer som inneholder tekststrengen «Antoine » (legg merke til mellomrom etter «toine».)
Husk å også få med filmer uten sjanger.
(17 rader, hvorav 4 har flere enn 0 sjangre)
*/ 

select f.filmid, title, count(genre)  
from film f left join filmgenre fg on f.filmid = fg.filmid 
where title like '%Antoine %' group by f.filmid, title;









/*    
Oppgave 5
Finn antall deltagere i hver deltagelsestype (parttype) per film blant kinofilmer som har «Lord of the Rings»
 som del av tittelen (hint: kinofilmer har filmtype 'C' i tabellen filmitem). 
 Skriv ut filmtittel, deltagelsestype og antall deltagere. (27 rader)
*/

select f.title, parttype, count(parttype) 
from film f natural join filmitem fi natural join filmparticipation fc 
where title like '%Lord of the Rings%' and fi.filmtype = 'C' 
group by f.title, parttype;







/*
Oppgave 6
Tittel og produksjonsår for alle filmene som ble utgitt i det laveste produksjonsåret.
 Spørringen kan ikke anta at du vet antall filmer dette gjelder (ikke bruk LIMIT). (2 rader)
*/

select title, prodyear 
from film 
group by prodyear, title 
having prodyear = (select min(prodyear) from film);








/*
Oppgave 7
Finn tittel og produksjonsår på filmer som både er med i 
sjangeren Film-Noir og Comedy. (3 rader) 
*/

(select title, prodyear from film f join filmgenre fg on f.filmid = fg.filmid where genre = 'Film-Noir')
intersect all
(select title, prodyear from film f join filmgenre fg on f.filmid = fg.filmid where genre = 'Comedy');











/*
Oppgave 8
Lag en spørring som returnerer tittel og produksjonsår for alle filmer fra både oppgave 6 og 7. (5 rader)
*/

( select title, prodyear from film group by prodyear, title having prodyear = (select min(prodyear) from film) )

union all

( 
 ( select title, prodyear 
   from film f join filmgenre fg on f.filmid = fg.filmid 
   where genre = 'Film-Noir')

 intersect all

 (  select title, prodyear 
	from film f join filmgenre fg on f.filmid = fg.filmid 
	where genre = 'Comedy')
);










/*
Oppgave 9
Finn tittel og produksjonsår for alle filmer der Stanley Kubrick 
både hadde parttype director og cast (ref oppgave 2). (2 rader)
*/

( select title, prodyear 
  from film f left join filmparticipation fp on  f.filmid = fp.filmid join person p on fp.personid = p.personid 
  where p.firstname = 'Stanley' and p.lastname = 'Kubrick' and fp.parttype = 'cast' ) 

intersect all 

( select title, prodyear 
  from film f left join filmparticipation fp on  f.filmid = fp.filmid join person p on fp.personid = p.personid 
  where p.firstname = 'Stanley' and p.lastname = 'Kubrick' and fp.parttype = 'director' );









/*
Oppgave 10
Hvilke TV-serier med flere enn 1000 brukerstemmer (votes) 
har fått den høyeste scoren (rank)? (3 rader) 
Tips: TV-serier finnes i tabellen series, og informasjon om brukerstemmer og score i filmrating.
*/

select maintitle 
from series join filmrating on seriesid = filmid 
where votes > 1000 
and rank = ( select max(rank) from series, filmrating where filmid = seriesid and votes > 1000) ;






/*
Oppgave 11
Hvilke land forekommer bare én gang i tabellen filmcountry? (9 rader)
*/

select country
from filmcountry group by country having count(country) = 1;







/*
Oppgave 12
I tabellen filmcharacter kan vi si at unike rollenavn er rollenavn 
som bare forekommer én gang i tabellen. 
Hvilke skuespillere (navn og antall filmer) har spilt figurer 
med unikt rollenavn i mer enn 199 filmer? (3 eller 13 rader)
*/


-- NB: denne bruker litt tid !! :)   Gjerne feedback meg på hvorfor hvis du har anledning!!!! :) 
select CONCAT(p.firstname,' ',p.lastname) as name, count(fp.partid) as amount_of_films_participated_in from person p natural join filmparticipation fp natural join filmcharacter fc where parttype = 'cast' and fc.filmcharacter in 
( select filmcharacter
from filmcharacter group by filmcharacter having count(filmcharacter) = 1 ) group by name having count(fp.partid) > 199;










/*
Oppgave 13
Fornavn og etternavn på personer som har regissert filmer med over 60 000 stemmer,
 der ALLE disse filmene har fått en score (rank) på 8 eller høyere. (49 rader)
*/

(select distinct firstname, lastname
from person p natural join filmparticipation fp
where parttype = 'director' and fp.filmid in ( select filmid from filmrating where votes > 60000 ))
except all
(
select distinct firstname, lastname
from person p natural join filmparticipation fp
where parttype = 'director' and fp.filmid in ( select filmid from filmrating where votes > 60000 and rank < 8 )) order by lastname;



