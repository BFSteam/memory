# memory #

### run memory
*Memory* runs under `python 3.6.3`

I personally use pyenv and virtualenv to run this project. 

Install pyenv

```
cd
git clone git://github.com/yyuu/pyenv.git .pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

Install virtualenv under pyenv

```
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
source ~/.bashrc
```

Install python version `3.6.3` (check the ![requirements](https://github.com/pyenv/pyenv/wiki))

```
pyenv install 3.6.3
```

Check with `pyenv versions`

Now create a project `mkdir myproject; cd myproject`

Install `virtualenv inside`

```
pyenv virtualenv 3.6.3 venv
pyenv activate venv
git clone https://github.com/BFSteam/memory.git
git clone https://github.com/terna/SLAPP3
pip install -r memory/requirements.txt
cp memory/run.py .
echo "../../memory/src" > SLAPP3/project.txt
```

Now run with `python run.py`





university abm project
<img src="https://github.com/BFSteam/memory/blob/master/tex/img/png/cover.png" />
[[https://github.com/BFSteam/memory/blob/master/tex/img/png/cover.png]]
![img](tex/img/png/cover.png)
####italian description
# Progetto di econofisica: Effetti della memoria nel *news spreading* #
## Roberto Bertilone, Francesco Fanchin, Nicola Sella ##
In una rete reale ci chiediamo se la memoria di notizie lette possa influenzare la dinamica ed
eventualmente creare effetti di segregazione. Per modellizzare questo fenomeno di diffusione
implementiamo una rete assegnando comportamenti microscopici per cercare fenomeni
macroscopici emergenti.
I nodi della rete sono costituiti da due tipi di agenti: le fonti e gli utenti.
Le fonti sono il bacino da cui gli utenti possono attingere notizie ed eventualmente diffonderle.
Gli utenti possono diffondere notizie in base a una loro intenzione: sanno crearsi una opinione delle
notizie che leggono e degli utenti primi vicini; inoltre “hanno una memoria” cioè possono ricordare
un certo numero di notizie che hanno visualizzato in precedenza.
I link rappresentano la sola possibilità di instaurare una comunicazione tra due agenti.
In questo progetto intendiamo studiare la lunghezza della memoria degli agenti tramite l’analisi di
misure statistiche della rete.

Inizialmente implementeremo una rete scale free con link indiretti e pesati. La struttura scale free
rappresenta la miglior approssimazione di rete reale essendo la sua distribuzione di grado descritta
da una legge di potenza: dunque costituisce una valida ipotesi iniziale. La tipologia di link scelta
evidenzia la bilateralità e l’intensità della comunicazione tra gli agenti. Prendendo come esempio
uno scambio di informazione tra due persone oppure tra una persona e un giornale, il peso
rappresenta il feeling, l’affiatamento pregresso; un segno posto davanti ad esso ne potrebbe
specificare l’entità (buono, indifferente, cattivo).
Nel corso della dinamica i link possono essere creati o distrutti dagli agenti e il loro peso può
cambiare a seguito di interazioni.
Come detto in precedenza, le fonti sono agenti che per loro natura non ricevono notizie: per
economia di programmazione il link che le collega ad un agente resta comunque indiretto anche se
le notizie sono solo in uscita.
Le notizie sono descritte da vari parametri tra cui un vettore di “topics”: ogni componente di esso è
un valore numerico che rappresenta la percentuale di pertinenza a quel topic all’interno della
notizia.
Ogni fonte è focalizzata, in misura variabile, sugli stessi argomenti. La notizia contiene inoltre
l’identificativo della fonte che l’ha diffusa ed un fattore che ne rappresenta l’importanza. Si terrà
traccia di altri metadati come ad esempio la data di pubblicazione.
Il tempo è scandito dall’observer. Ogni fonte genererà nuove notizie tenendo conto lei stessa del
tempo che passa.
Le notizie al primo ciclo sono diffuse dalle fonti, successivamente lo spread è fra fonti e utenti e fra
utenti e utenti.
L’utente avrà inoltre un tempo di attivazione che sarà regolato attraverso un suo orologio interno
tenendo conto del tempo che scorre nel mondo: solo mentre è attivo sarà possibile per lui interagire
con il sistema. 
Gli utenti hanno uno stato mentale che viene inizializzato al primo ciclo temporale. Questo stato
rappresenta la personalità dell’utente, i suoi interessi e veicola le sue scelte.
Una apposita funzione “distanza” permette di confrontare una notizia con lo stato mentale del
singolo utente; in esso è contenuto un vettore avente come dimensione il numero di topics. Lo stato
contiene inoltre altri parametri che caratterizzano con maggiore specificità il singolo utente, ad
esempio la sua propensione a leggere e diffondere notizie.

La dinamica del sistema sarà determinata dalle azioni degli utenti; i parametri sopra descritti
influenzeranno le loro decisioni.
Intendiamo indagare come la variazione nella lunghezza della memoria possa influenzare le
decisioni degli agenti procedendo con analisi sistematiche, ad esempio, sui tempi di diffusione.
Effettueremo diverse simulazioni a varie lunghezze, fissando le condizioni iniziali (seed) ottenendo
una statistica sufficiente. Eventuali altre variazioni saranno apportate in corso d’opera.

Ci aspettiamo di osservare correlazioni tra la lunghezza della memoria e variazioni macroscopiche
del sistema. Inoltre potrebbero emergere fenomeni di polarizzazione (segregazione, echo
chambers) ampiamente studiati in letteratura, ma non completamente compresi.

## Ulteriori sviluppi ##
Ulteriori decisioni dell'agente potranno essere implementate in seguito con una rete neurale
interna allenata a prendere vari tipi di decisione in merito alle preferenze sulle notizie o alla
creazione/rimozione dei link.
Un altro punto da analizzare potrebbe essere la topologia iniziale della rete: al variare di essa, si
potrebbero indagare gli effetti macroscopici, in linea di principio molto diversi.

## Agent or MAS? ##
The agents can operate in their environment, making decisions and interacting each other. Initially
there is no comunication protocol between them. They want to maximize their own benefit which is
communicate and share news with "friends". There is no social or system behaviour, only individual.
We can conclude that the system is not MAS.

### agent feats ###
The required characteristics of each agents are *veracity* and *benevolence*. No mobility is required. 
The agents are rationals meaning that they try to reach their goal sympathyzind with their "neighbours"
Each agent can receive information from the world or from another agent; it can also interact with 
the world or with an agent.
Their ability to modify the environment is the rimotion of a link in the social network.
The only accessible variable for each agent is the clock number; they can also access something "near"
them.

### non deterministic environment ###
The environment is not deterministic. Every action can produce different effects in a probabilistic
way.
The sphere of action of each agent is limited to its neighbours. They can have an opinion and read 
near news. They have limited senses and sensors.
Also the actions between agents are non deterministic and do not have the complete control over another
agent.

### static environment **?** ###
### discrete or continous environment **?** ###

### (mostly) reactive agents ###
each agent makes local fair decisions: global behaviours may emerge.
When active each agent can control the environment and reacto to the changes. It is possible
that during his inactive state the environment has changed and the goal of the agent is unreachable.
For this reason the agent can act in an unpredictable way and somehow irrational.

### Do the agents have "Reactivity", "Proactiveness" and "Social Ability"? ###
  * Reactivity: The agents can control the clock and the news spreading around them during the
    evolution of the system
  * Proactiveness: Each agent knows what his goal is and how to reach it
  * Social Ability: They know how to send and recive news, to determine sympathy with neighbours


### Set of environment states

### Set of agent actions
