# Mining software repository

Analisi dei commit della repository 'https://github.com/godotengine/godot' con l'obiettivo di rispondere alla seguente domanda: Quali sono i 10 file più coinvolti in commit mirati a correggere bug?

## Requisiti
- Librerie python elencate nel dile `requirements.txt`

## Configurazione del progetto

1. **Clona la repository** nella directory: `./python-scripts/resources/`
```bash
cd ./python-scripts/resources
git clone https://github.com/godotengine/godot
```
2. **Crea un ambiente virtuale** (consigliato)
3. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```
## Esecuzione del progetto
```bash
cd ./python-scripts/src
python analyzer.py
```
## Note sull'utilizzo
- Nella cartella `./js-scripts/` è presente il codice per ottenere dalle issue il bug tracker del progetto quindi può non essere eseguito ppoichè i risultati sono memorizzati nel issue.db
- issue.db è un database SQLite ottenuto convertendo le issue bug in formato JSON
- Non bisogna, quindi, rieseguire il codice `./python-scripts/src/convert_to_sqlite.py`
- Quando si vuole ottenere il JSON dei file più buggati non si consiglia di decommentare il codice che fa partire il metodo `find_top_10_bugged_file(filtered_commits_list)` in `analyzer.py` poiché attualmente è commentato data la quantità di tempo che ci vuole per analizzare tutti i file che sono stati modificati dai commit in esame. Si consiglia quindi di caricare solamente  il file `top_10_bugged_file.json` che è stato ottenuto dall'esecuzione del metodo menzionato precedentemente.

## Contenuti
- `/python-scripts/src/`: script di analisi e script di utility
- `/js-scripts/`: script che fa uso delle API di GitHub per ottenere le issue con label `bug`
- `/python-scripts/src/top_10_bugged_file.json`: lista dei file più buggati in ordine decrescenti ottenuti dal metodo: `find_top_10_bugged_file(filtered_commits_list)`
- `/python-scripts/src/resources`: locazione in cui si consiglia di clonare la repository presa in esame
- `/python-scripts/src/resources/issues.db`: db SQLite contenente le issue con la label `bug` della repository presa in esame