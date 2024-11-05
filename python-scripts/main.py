# This is a sample Python script.
import json
import sqlite3

from git import Repo


# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def load_issues(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    repo_path = "./resources/godot"
    repo = Repo(repo_path)

    #try:
     #   issues = load_issues('./resources/issues_data.json')
     #   print("Connessione avvenuta con successo")

    #except Exception as e:
     #   print("Errore di connessione")

    if not repo.bare:
        print("repo essite")
    else:
        print("repo non valida")


