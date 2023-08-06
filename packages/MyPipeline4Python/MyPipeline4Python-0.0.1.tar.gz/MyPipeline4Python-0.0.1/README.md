I componenti del gruppo:

- Tiberio Falsiroli
- Giovanni Donato Gallo
- Lorenzo Di Tria 

Link repository:
https://gitlab.com/2020_assignment1_pipelinetest/2020_assignment1_pipeline_project.git

L'applicazione consiste in un semplice script python, il quale si collega ad un DB contenente una base di dati avente come attributi
"nome" , "cognome", e "numero di telefono". Lo script ci permette di eseguire una query, grazie alla quale inserendo nome e cognome, possiamo
vedere i numeri di telefono delle tuple corrispondenti. Qual'ora non risultasse alcuna tupla corrispondente, abbiamo la possibilità di inserire anche il numero di telefono, in modo tale da aggiungerla alla base di dati.

La Pipeline
La pipeline sfrutta l'immagine di un container python, versione 3.7. 
Abbiamo poi strutturato una cache iniziale, in modo da poterla sfruttare globalmente per ogni stage della pipeline,
ed ottimizzare i tempi di esecuzione della stessa. Abbiamo inserito in cache due path:

- .cache/pip --> dove andremo ad importare i vari moduli, in modo da poterli riutilizzare tra i vari stage
- venv/ --> dove andiamo a posizionare il nostro ambiente virtuale

Al momento la nostra pipeline è composta da due stage: build e verify.
Per entrambi andremo prima ad importare i moduli necessari, per poi andarli ad eseguire. Ogni stage ha anche un comando echo, in modo da tenere traccia dell'andamento della pipeline.

Stage: build
Per questo stage abbiamo semplicemente importato i moduli richiesti per l'esecuzione dello script, tramite un comando che installva tutti i moduli trascritti nel file "requirements.txt"

Stage: verify
Abbiamo suddiviso questo stage in due job che vengono eseguiti in parallelo, uno dedicato al modulo bandit e l'altro dedicato al modulo prospector;
in entrambi abbiamo installato i moduli necessari per i rispettivi job prima dell'esecuzione dello script (before_script:), per poi eseguire i comandi 
"bandit" e "prospector" su tutti i fili con estensione .py contenuti nella cartella src.

Progressi:
La pipeline comincia a prendere forma, e ad essere ottimizzata. Il prossimo step consisterà nel creare dei test, in modo da progredire con gli stage.


Problematiche attuali:
Abbiamo attualmente problemi a far eseguire un controllo statico del codice da parte di Prospector, in quanto sono richiesti degli input da linea di comando, ma che ancora dobbiamo ben capire come passare "indirettamente", in modo che Prospector possa sfruttarli. Stiamo inoltre cercando di ottimizzare il più possibile l'esecuzione della pipeline tramite la cache



