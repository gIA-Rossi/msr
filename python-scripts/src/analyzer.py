import sqlite3
from collections import defaultdict

from git import Repo
import re
import json

# connetto al db
conn = sqlite3.connect('./resources/issues.db')
c = conn.cursor()

query = """
SELECT id, state, title, body, user_login as open_by, assignee, closed_by
FROM issues
WHERE id = ?
"""


# Path alla repository locale
repo_path = "./resources/godot"
repo = Repo(repo_path)

commits_list = []


def do_query_test(id):

    c.execute(query, (id,))
    results = c.fetchall()
    return results


def load_commits_from_json(file_path):
    with open(file_path, 'r') as file:
        commits = json.load(file)
    return commits


def syn_sem_criteria_calc(commit):

    syn_confidence = 0
    sem_confidence = 0
    message = commit.message.lower()

    # logica per il primo criterio:
    # se esiste nel messaggio di commit la parola 'bug' o 'fix', si assegna un punto di confidenza

    if "fix" in message or "bug" in message:
        syn_confidence += 1;

    # logica per il secondo criterio
    # Si analizzano i numeri presenti nei messaggi di commit e si cerca una corrispondenza nel BT
    # trovo i numeri all'interno dei messaggi di commit
    numeri = re.findall(r'\d+', message)
    numeri = [int(num) for num in numeri]

    print(numeri)

    # cerco tutte le corrispondenze nel BT
    for numero in numeri:
        id = numero
        c.execute(query, (id,))
        results = c.fetchall()
        if results:
            syn_confidence += 1
            for row in results:
                print(
                    f"ID: {row[0]}, State: {row[1]}, Title: {row[2]}, Body: {row[3]}, Open By: {row[4]}, "
                    f"Assignee: {row[5]}, Closed By: {row[6]}")

                # Calcolo dei punti di confidenza semantica
                # Criteri:
                # 1. Lo stato di b è passato almeno una volta allo stato FIXED
                # 2. La descrizione riassuntiva di b è contenuta nel messaggio di commit c
                # 3. L'autore di c è registrato come assegnatario di b
                # 4. Uno o più dei file modificati sono allegati a b

                # Sostanzialmente devo verificare se l'id del Bug è presente nel BT e poi dare i punti di confidenza

                if row[1].lower() == 'closed':
                    sem_confidence += 1

                if row[2].lower() in message:
                    sem_confidence += 1

                if commit.author.name.lower() == row[5].lower() if row[5] is not None else False:
                    sem_confidence += 1

            break
        else:
            print("Nessun risultato trovato per l'ID specificato.")

    if syn_confidence >= 1 or sem_confidence >= 1:
        commits_list.append({
            'id': commit.hexsha,
            'syn_confidence': syn_confidence,
            'sem_confidence': sem_confidence
        })


def get_one_fix_bug_commit():
    if not repo.bare:
        print("Analisi dei commit con parole chiave 'commit' e 'fix'...")
        n = 0

        for commit in repo.iter_commits():
            message = commit.message.lower()
            if "bug" in message or "fix" in message:
                n += 1

            if n == 1:
                print(commit.message)
                print(commit.hexsha)
                return commit
    else:
        print("La directory specificata non contiene una repository Git valida.")


def apply_filter_to_commits(commits_list):

    filtered_commits = []

    for item in commits_list:
        if item['sem_confidence'] > 1 or (item['sem_confidence'] == 1 and item['syn_confidence'] > 0):
            filtered_commits.append(item)

    ordered_by_max_confidence = sorted(filtered_commits,
                                       key=lambda x: (x["sem_confidence"], x["syn_confidence"]),
                                       reverse=True)

    return ordered_by_max_confidence


def start_analyze():

    if not repo.bare:
        # filtro
        for commit in repo.iter_commits():
            syn_sem_criteria_calc(commit)

        filtered_commits_list = apply_filter_to_commits(commits_list)

        # salvo localmente i commit per evitare l'esecuzione di nuovo
        with open('ordered_filtered_commits_list.json', 'w') as file:
            json.dump(filtered_commits_list, file, indent=4)
    else:
        print("La directory specificata non contiene una repository Git valida.")

    return commits_list


def find_top_10_bugged_file(list_of_commits):

    bug_file_count = defaultdict(int)

    for commit in list_of_commits:

        try:
            commit_obj = repo.commit(commit['id'])
        except Exception as e:
            print(f"Errore nel recuperare il commit {commit['id']}: {e}")
            continue

        changed_files = commit_obj.stats.files

        for file in changed_files.keys():

            bug_file_count[file] += 1

    most_bugged_file = sorted(bug_file_count.items(), key=lambda x: x[1], reverse=True)
    return most_bugged_file


def get_the_10(list_of_bugged_file):

    # dovrei escludere i file inutili che sono presenti in github
    exlcuded_files = ["LICENSE"]
    excluded_extension = [".md", ".txt", ".yml", ".yaml"]

    # uso una list comprehension per fare prima
    filtered_files = [
        file for file in list_of_bugged_file
        if file[0] not in exlcuded_files and not any(file[0].endswith(ext) for ext in excluded_extension)
    ]

    return filtered_files[:10]


if __name__ == '__main__':

    #commit = get_one_fix_bug_commit()
    #syn_sem_criteria_calc(commit)
    #res = do_query_test(171)

    #for row in res:
    #    print(row[1].lower())

    # TO-DO:
    # verifico se funziona
    # filtro la lista dei commit tenendo quelli che soddisfano la formula
    # analizzo i commit per scoprire i 10 file più buggati

    # Carica il file JSON

    # start_analyze()

    # print(commits_list[0])

    # with open('ordered_filtered_commits_list.json', 'r') as file:
      #  commits_list = json.load(file)

    # list = find_top_10_bugged_file(commits_list)

    # salvo localmente i commit per evitare l'esecuzione di nuovo
    # with open('top_10_bugged_file.json', 'w') as file:
      #  json.dump(list, file, indent=4)

    with open('top_10_bugged_file.json', 'r') as file:
        top_10 = json.load(file)

    # salvo i primi 10
    list_to_be_saved = get_the_10(top_10)

    with open('the_10.json', 'w') as file:
        json.dump(list_to_be_saved, file, indent=4)
