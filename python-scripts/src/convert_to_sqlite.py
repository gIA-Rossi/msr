import json
import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
percorso_file_issue = os.path.join(base_dir, "..", "resources", "issues_data.json")


def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Crea la tabella se non esiste
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY,
            state TEXT,
            title TEXT,
            body TEXT,
            user_login TEXT,
            user_id INTEGER,
            assignee TEXT,
            closed_by TEXT,
            pull_request_url TEXT
        )
    ''')
    return conn


def insert_issue(c, issue):
    # Estrai l'URL della pull request se presente
    pull_request_url = issue['pull_request']['url'] if issue.get('pull_request') else None

    # Estrai il login dell'assegnatario se presente, altrimenti metti None
    assignee_login = issue['assignee']['login'] if issue.get('assignee') else None

    # Estrai chi ha chiuso l'issue se presente, altrimenti metti None
    closed_by_login = issue['closed_by']['login'] if issue.get('closed_by') else None

    c.execute('''
        INSERT INTO issues (id, state, title, body, user_login, user_id, assignee, closed_by, pull_request_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        issue['number'],
        issue['state'],
        issue['title'],
        issue['body'],
        issue['user']['login'],
        issue['user']['id'],
        assignee_login,  # Usa il login dell'assegnatario
        closed_by_login,  # Usa il login di chi ha chiuso
        pull_request_url
    ))


def load_issues(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == "__main__":
    db_name = 'issues.db'
    conn = create_database(db_name)
    c = conn.cursor()

    try:
        issues = load_issues(percorso_file_issue)
    except FileNotFoundError:
        print("file non trovato")

    # Se il JSON è una lista, iteriamo su ciascuna issue
    for issue in issues:
        insert_issue(c, issue)

    # Salva (commit) le modifiche e chiudi la connessione
    conn.commit()
    conn.close()
