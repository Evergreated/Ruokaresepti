# Ruokaresepti

Aiheena on ruokaresepti esimerkkiaiheista. 

Ominaisuudet:

Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.
Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
Käyttäjä näkee sovellukseen lisätyt reseptit.
Käyttäjä pystyy etsimään reseptejä hakusanalla.
Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
Käyttäjä pystyy valitsemaan esimerkiksi seuraavia luokitteluja:
Ruoan tyyppi: alkuruoka, pääruoka tai jälkiruoka
Ruokavalio: laktoositon, gluteeniton tai vegaaninen
Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.
Tässä pääasiallinen tietokohde on ruokaresepti ja toissijainen tietokohde on kommentti reseptiin.


Ominaisuudet kopioitu esimerkkiaiheen ruokaresepti kohdasta. 



Välipalautus 2 Update

Tämän hetkisen vaiheen sovelluksessa on toimintoja: 
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään. 
- Käyttäjä pystyy kirjautumaan ulos.
- Kirjautunut käyttäjä pystyy lisäämään reseptejä.
- Käyttäjä pystyy muokkaamaan ja poistamaan omia reseptejään.
- Käyttäjä pystyy selaamaan kaikkien käyttäjien lisäämiä reseptejä.
- Käyttäjä pystyy etsimään reseptejä niiden nimellä. 
- Resepti sisältää nimen, ainekset ja valmistusohjeen. *


Asennus ja käynnistäminen

1. Kloonaa repositorion 
2. Luo virtuaaliympäristö
3. Asenna Flask 
4. Luo tietokanta 
5. Määritä Flask salainen avaimen
6. Käynnistä sovellus


Sovelluksen testaaminen 

1. Luo uusi käyttäjätunnus Rekisteröidy-sivulla.
2. Kirjaudu sisään luomallasi tunnuksella.
3. Lisää uusi ruokaresepti.
4. Tarkista, että resepti näkyy etusivulla.
5. Muokkaa reseptiä ja tallenna muutokset.
6. Kokeile reseptien hakemista hakukentällä.
7. Poista lisäämäsi testiresepti.
8. Luo toinen käyttäjätunnus ja varmista, ettei sillä voi muokata tai poistaa ensimmäisen käyttäjän reseptejä.