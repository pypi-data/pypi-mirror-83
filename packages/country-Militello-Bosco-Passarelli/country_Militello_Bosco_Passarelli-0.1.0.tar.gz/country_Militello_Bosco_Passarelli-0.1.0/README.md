# DATI UTILI
<!-- blank line -->
----
<!-- blank line -->

Indirizzo repository gitlab: https://gitlab.com/theunusual/2020_assignment1_countries

Studenti:
- 807019 Patrick Militello
- 816099 Alessandro Bosco
- 862037 Raffaello Passarelli 

# INTRODUZIONE
<!-- blank line -->
----
<!-- blank line -->

Il progetto in esame è basato sul rendere il processo di sviluppo software più efficace ed efficiente tramite l'utilizzo di una pipeline CI/CD su Gitlab. La pipeline utilizzata, che consente di automatizzare l'intero processo di sviluppo, è costituita da 7 fasi (implementata come job):
- Build: risoluzione di dipendenze e compilazione del codice.
- Verify: esegue analisi dinamiche o statiche di vario genere del codice.
- Unit-test: esegue gli unit-test, ovvero i test sui singoli moduli.
- Integration-test: esegue gli integration-test, ovvero i test sull'interazione tra i differenti moduli.
- Package: ***in sviluppo***
- Release: ***in sviluppo***
- Deploy: ***in sviluppo***

Il codice della pipeline è contenuto nel file .gitlab-ci.yml e prevede come primo comando il caricamento dell'immagine docker di default per i container dei job (python:3.8.6). La variabile globale settata è  PIP_CACHE_DIR ("$CI_PROJECT_DIR/.cache/pip") che contiene la cartella
utilizzata per scopi di cache.


# APPLICATIVO UTILIZZATO
<!-- blank line -->
----
<!-- blank line -->

L'applicativo utilizzato è diviso in tre differenti moduli:
- Uno script python principale, che costituisce il corpo fondamentale del programma (countries.py);
- Uno script python contenente le funzioni accessorie (funzioni_country.py);
- Un database locale (TestDB).

Il semplice funzionamento dello script principale riguarda il popolamento del database locale, con eventuale creazione in caso non esista, sulla base dei dati presenti nel file country.csv: essi riguardano 10 paesi del mondo e la relativa popolazione espressa in milioni. Il database viene dunque interrogato e vengono mostrati a video i dati inseriti nella tabella. Infine, vengono svolte alcune semplici operazioni sui dati estratti sulla base delle funzioni accessorie sviluppate, come il calcolo della somma totale della popolazione dei 10 paesi e del paese con popolazione massima. 


# CACHE
<!-- blank line -->
----
<!-- blank line -->

GitLab CI / CD fornisce un meccanismo di memorizzazione nella cache che ci permette di risparmiare tempo durante l'esecuzione dei jobs riutilizzando lo stesso contenuto di un job precedente. E' stato particolarmente utile in quanto il nostro applicativo python dipende da diverse librerie.
E' stata pertanto definita la cache a livello globale che viene ereditata da ogni job. Le librerie Python sono state installate in un ambiente virtuale sotto venv /, la cache di pip sotto .cache / pip / ed entrambi sono stati memorizzati nella cache per-branch.


# FASE DI BUILD
<!-- blank line -->
----
<!-- blank line -->

DIRE CHE ESSENDO L'APPLICATIVO IN PYTHON SI E' UTILIZZATA L'IMMAGINE DI PYTHON E COS'E' UN'IMMAGINE
Per la fase di build è stato redatto il file requirements.txt, contente il nome e la versione delle librerie Python necessarie per l'esecuzione dell'applicativo. 
Dalla pipeline sono dunque state installate tutte le librerie e relative dipendenze contenute nel file tramite il comando *- pip install -r requirements.txt*.


# FASE DI VERIFY
<!-- blank line -->
----
<!-- blank line -->

La fase di Verify è stata suddivisa in due differenti analisi del codice:
- Analisi sintattica, tramite la libreria Python Prospector.
- Analisi della sicurezza, tramite la libreria Python Bandit.

Prospector è un tool per l'analisi del codice Python che permette di evidenziare errori, potenziali problemi e violazioni di standard convenzionali. Il comando utilizzato è *- prospector --no-autodetect countries.py*: il comando no-autodetect permette di evitare che Prospector ricerchi automaticamente l'installazione di librerie strettamente correlate a quelle presenti, ma difatto non utilizzate. Nel nostro caso, era stata rilevata la mancata installazione della libreria Django, non utilizzata ma strettamente legata alla libreria sqlite3, impiegata per la gestione del database.

Bandit è un tool per la rilevazione di problemi di sicurezza comuni nel codice Python: esso scansiona il file e genera un rapporto contenente i risultati dell'analisi di sicurezza. Il comando utilizzato è *-bandit -r countries.py*.

# FASE DI UNIT-TEST
<!-- blank line -->
----
<!-- blank line -->

Per la fase di unit-test è stato creato uno script Python (test_countries.py) per testare le funzioni accessorie contenute nel file relativo. A tal fine, è stata utilizzata la libreria unittest che supporta l'automazione dei test tramite fixtures (impianti di test), test suites e test runner. E' stata creata una classe che implementa i test delle tre funzioni: il semplice funzionamento dei test consiste nell'utilizzo di assert al fine di verificare che l'output restituito dalle funzioni implementate sia uguale al risultato atteso. Per l'esecuzione dei test è stato utilizzato il framework pytest, che semplifica la scrittura di piccoli test e supporta anche test funzionali complessi per applicazioni e librerie.
Il comando utilizzato è *- pytest -k 'test_unit' --junitxml=report_unit_test.xml*, dove l'utilizzo del comando -k 'string' permette di eseguire solamente i test il cui nome inizia per *string*.
junitxml è invece un modulo di Python che permette di generare automaticamente report in formato XML a partire dai risultati di test suit sritte in Python. Successivamente, questo file è stato caricato come artefatto di Gitlab, ovvero una lista di file e cartelle create da un job una volta concluso e resi disponibili per il download locale.


# FASE DI INTEGRATION-TEST
<!-- blank line -->
----
<!-- blank line -->

La fase di integration-test estende quella di unit-test: sono infatti stati aggiunti al medesimo script (test_countries.py) tre test sull'interazione tra lo script principale e il database: dato uno stato noto del database, è stato effettuato un cambiamento (insert o delete) e una lettura (select) per verificare che il risultato atteso sia a esso conforme. Le librerie e i moduli utilizzati sono i medesimi della unit-test.
Il comando utilizzato è *- pytest -k 'test_integration' --junitxml=report_integration_test.xml*, per eseguire unicamente i test il cui nome inizia per "test_integration" e per salvare il risultato in un file XML, successivamente caricato come artefatto.


# FASE DI PACKAGE
<!-- blank line -->
----
<!-- blank line -->

***IN SVILUPPO***

# FASE DI RELEASE
<!-- blank line -->
----
<!-- blank line -->

***IN SVILUPPO***

# FASE DI DEPLOY
<!-- blank line -->
----
<!-- blank line -->

***IN SVILUPPO***