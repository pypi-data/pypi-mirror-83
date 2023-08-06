## Componenti del gruppo

Danilo Fumagalli, mat 830683

Marta Pelusi, mat 800444

## Introduzione

Si vuole implementare una pipeline con GitLab per una applicazione scritta in lunguaggio Python che utilizza le seguenti librerie:

\- matplotlib

\- numpy

\- MySQLdb

L'applicazione vuole creare effetti di colore da immagini estratte da un database mySQL.

## Come funziona

Questo è un progetto strutturato in più script:

\- media.py

\- scambia.py

\- main.py

[media.py](https://gitlab.com/Bakedsloth/2020_assignment1_a1/-/blob/develop/media.py) è composto da una funzione *get_media* che prende in input un'immagine e restituisce un array 1x3 delle medie del colore nei tre canali colore RGB dell'immagine in input.

[scambia.py](https://gitlab.com/Bakedsloth/2020_assignment1_a1/-/blob/develop/scambia.py) è composto da una funzione *scambia* che prende in input un'immagine e un intero *pos* e, in base al valore di pos, scambia tra loro due canali colore restituendo l'immagine modificata.

l'intero *pos* corrisponde alla posizione (nell'array restituito dallo script media.py) della media colore che ha il valore più alto.

media.py e scambia.py sono due script che possono essere eseguiti indipendentemente tra loro.

[main.py](https://gitlab.com/Bakedsloth/2020_assignment1_a1/-/blob/develop/main.py) è lo script che unisce l'operato degli altri due script.

L'altro componente dell'applicazione è un database mySQL composto da 5 righe e 4 colonne.

Le quattro colonne sono rappresentative dell'id, del nome, dell'estensione e del percorso di 5 immagini.

Le immagini sono contenute in una cartella chiamata *immagini* all'interno del repository GitLab.

Il database è popolato attraverso un file csv chiamato metadata.csv, anch'esso all'interno del repository GitLab.

## Assunzioni realizzazione della pipeline

Il file [.gitlab-ci.yml](https://gitlab.com/Bakedsloth/2020_assignment1_a1/-/blob/develop/.gitlab-ci.yml) contiene la nostra pipeline.

Abbiamo scelto di non imporre una versione precisa di Python, ma usare l'ultima versione installata.

Come servizi abbiamo scelto di utilizzare l'ultima versione di mySQL per connetterci al nostro database.

Salviamo i moduli nella cache per risparmiare tempo nelle esecuzioni successive.

Prima di eseguire lo script installiamo virtualenv e creiamo un ambiente virtuale in cui inseriamo tutte le librerie necessarie all'esecuzione della nostra applicazione. Queste in particolare sono:

​	\- matplotlib

​	\- numpy

​	\- mysqlclient

​	\- mysql-connector-python

​	\- pymysql

Gli stages che andiamo ad eseguire sono:

​	\- build

​	\- verify

​	\- unit-test

Nello stage **build** creiamo il file di testo requirements.txt all'interno del quale andiamo ad inserire tutte le librerie che vogliamo installare ed utilizzare con le loro rispettive versioni.

Nello stage **verify** utilizziamo prospector e bandit per individuare eventuali errori nello script main, in quanto esso è quello che mette insieme i vari script richiamandoli, come spiegato sopra.

Nello stage **unit-test** installiamo ed utilizziamo la libreria pytest per eseguire i test all'interno dello script [test_unit.py](https://gitlab.com/Bakedsloth/2020_assignment1_a1/-/blob/develop/test_unit.py). Questo script testa il corretto funzionamento degli script media.py e scambia.py facendo delle prove: nel caso di media.py viene testata una proprietà specifica del calcolo della media aritmetica, mentre nel caso di scambia.py viene verificato se scambiando canali colore due volte l'immagine resta la stessa in quanto lo scambio è commutativo.
