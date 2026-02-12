# BNL
BNL's newest Autonomous Slave Driver (ASD).


## GITHUB INFO
NB: IKKE KLON ORIGINAL REPOET. Lag en fork og klon den.

## For å bygg Docker image:

Root i dette prosjektet er fra rooten av BNL directorie. Skal dermed se slik ut:

```console
dinbruker:~/din_bane/BNL$ 
```

Om du ikke er i denne banen, så bruker du kommandoen:
```console
cd banen_din/BNL
```

`cd` står for `Change Directory`.

Antar dere allerede har installert Docker.

Docker i vårt tilfelle har 3 prosesser i seg
*Lag/modifiser et image.
*Bygg et image.
*Kjør det image'e.

### Modifiser image'e
Først, så må eventuelle endringa gjøres. For å få mest stabil og elementær funksjonalitet, la den vær default. Derimot, hvis du ska teste dine egne funksjone så må du kun endre på `Dockerfile` fila som ligg i `custom_docker`. **IKKE ENDRE PÅ** `Dockerfile` **I** `docker_image` **MAPPA**. For å faktisk få den til å hent fra dine egne endringa, så må du endre korr image hente filan fra. I Det her e i `linje 96` i `private_docker/Dockerfile`:

```python
RUN git clone --recursive "https://github.com/Havlia/BNL" /bnl_git
```

Bytt linken ut med linken til din fork, i.e.:

```python
RUN git clone --recursive "https://github.com/dinbruker/BNL" /bnl_git
```

Om du mangle visse libraries, og vil ikke last ned dem hver gang, så kan dem legges til i packages nedlastinga på `linje 11` i docker fila:

```python
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    bash-completion \
    dirmngr \
    .
    .
    .
```

`\` betyr bare "behandle som om dem e på samme linje", så:

```console
apt install pakke1 \
	pakke2 \
	pakke 3 \
```

er det samme som:

```console
apt install pakke1 pakke2 pakke 3
```

Det er bare ryddigere.

Så om du trenger flere pakker, så bare legger du den til i lista.

### Bygg Docker Image
Deretter så må Docker-imageé bygges. Kjør kommandoen:

```console
sudo docker build --tag bnl:ros-image "docker_image" 
```

* `docker build` er kommandoen for å bygge et image.
* `--tag` er terminal flagget som lar deg gi image'e et slags navn.
* `bnl:ros-image` er Docker sin egen navnekonvensjon. Helst opretthold denne til en viss grad. se [Docker sin dokumentasjon](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/#tagging-images).
* `docker_image` e mappe navnet. Hvis du ska bruk din skreddersydde versjon, så må du bytt ut herren med `private_docker`. Hermetegnene `" "` er bare for å unngå problemer med eventuell mellomrom i navn.

> Bygginga kommer til å ta en stund første gangen (~4-5 min), men dere kan fint gjøre andre ting i mens denne jobber.

Den vil gi noen varsla på slutten, men vil ikke vær problematisk hvis du ser herre:

```console
..
..
 => => unpacking to docker.io/library/bnl:ros2-gui
                                                                         31.3s

 4 warnings found (use docker --debug to expand):
 - LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format (line 51)
 - LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format (line 52)
 - LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format (line 89)
 - LegacyKeyValueFormat: "ENV key=value" should be used instead of legacy "ENV key value" format (line 98)

```

> Note: Docker image'e du har bygget er lokalisert på pcen din i en spesifik mappe. Du trenger ikke fiske den fram selv, ettersom docker vet hvor den lagrer disse.

### Kjør Docker fil

No ska du kjør Docker konteinern, og det kan gjøres på 2 måta, basert på ka du treng.

#### Uten GUI (Default)

Dersom du skal kun kjøre funksjoner og kommunikasjon uten noen former for gui elementer (i.e. ikke gazebo, rviz2, rqt, rqt-graph, plotjuggler o.l.) så kan du starte den på vanlig vis.

> Note: ingen andre apper som bruker grafiske elementer i Dockern vil heller funke, som f.eks. `gedit`. Alle ting som åpner et nytt vinduet er no-go i denne modusen.

Da starter du den med kommandoen:

```console
sudo docker run --rm -it bnl:ros-image
```

* `docker run` er kommandoen for å starte en container.
* `-it` er 2 flagg som trengs for å få en interaktiv terminal linje. (i = interaktiv, t = terminal). `-it = -i -t`
* `--rm` er 1 flagg for å passe på å fjerne endringene du gjorde etter du stopper prosessen. Dette er for å passe på at du ikke gjør noen uheldige endringer. 

> Om du opplever at du trenger å lagre endringer, så bør du endre image'e. Det finnes også `docker commit`, men denne er ikke foretrekt hvis du ofte gjør endringer.

Atter en gang, hvis du bruker skreddersydd docker, så må du bytte ut `bnl:ros-image` med hvilket enn navn du selv lagde.

Du vil nå få en ny terminallinje, som ser noe slikt ut:

```console
root@f38ad4e50fa7:/bnl_git# 
```

Gratulerer! Du har nå åpnet en Docker konteiner. Ros er lokalisert på samme sted som på linux, og du er nå i root av Git'en.

* Ros-lokasjon: `/opt/ros/jazzy/`
* Git-lokasjon: `/bnl_git/`
\
#### Kjør Docker fil med Rocker (GUI)

Rocker er en wrapper på Docker, som lar deg kjøre med gpu akselerasjon og mange andre ting, men viktigst er `x11`, som lar oss loade GUI.

Start med å laste ned Rocker:

```console
sudo apt install python3-rocker
```

Om den ikke finner denne, så pass på at du har oppdatert apt:

```console
sudo apt update
```

> Rocker ligger i repositorie til Docker, så hvis du har docker skal det være lett å laste ned Rocker.

Deretter, så er det lignende til default metoden, hvor du kjører kommandoen:

```console
sudo rocker --x11 bnl:ros-image
```
* `rocker` er kommandoen for å starte Rocker.
* `--x11` er flagget for å starte med x11 funksjonalitet.

For siste gang, bytt `bnl:ros-image` til hva enn du kalte image ditt dersom du kjører skreddersydd.

Dersom alt startet riktig skal du til slutt se:

```console
root@2f35155ec1cc:/bnl_git#
```

Gratulerer! Du har startet en GUI variant av Docker. Ros er lokalisert på samme sted som på linux, og du er nå i root av Git'en.

* Ros-lokasjon: `/opt/ros/jazzy/`
* Git-lokasjon: `/bnl_git/`


# For å avslutte Docker.

Ettersom `Ctrl+C` brukes for å avslutte terminal prosesser, så bruke docker `Ctrl+D`for å avslutte konteinern. Da går du tilbake til en vanlig terminal, og alt du jobbet med er slettet.

**HUSK: DET LAGRES IKKE AV SÆ SJØL!!!**
