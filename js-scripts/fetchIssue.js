import { Octokit } from "@octokit/core";
import fs from "fs";

const octokit = new Octokit({
    auth: process.env.GITHUB_TOKEN
});

async function fetchAllIssues() {
    let issuesData = []; // Array per accumulare tutte le issue
    let page = 1;        // Partenza dalla pagina 1
    let fetchedData;

    try {
        do {
            // Effettua la richiesta alla pagina corrente
            fetchedData = await octokit.request('GET /repos/{owner}/{repo}/issues', {
                owner: 'godotengine',
                repo: 'godot',
                headers: {
                    'X-GitHub-Api-Version': '2022-11-28' // presi dalla doc delle issue API
                },
                state: "all",
                labels: "bug",
                per_page: 100,  // Numero massimo di issue per pagina
                page: page      // Numero di pagina corrente
            });

            // Mappa i dati della pagina corrente e aggiungili a issuesData
            const currentIssues = fetchedData.data.map(issue => ({
                number: issue.number,
                state: issue.state,
                title: issue.title,
                body: issue.body,
                user: issue.user ? {
                    login: issue.user.login,
                    id: issue.user.id,
                } : null,
                assignee: issue.assignee ? {
                    login: issue.assignee.login,
                    id: issue.assignee.id
                } : null,
                pull_request: issue.pull_request ? {
                    url: issue.pull_request.url,
                    html_url: issue.pull_request.html_url,
                    diff_url: issue.pull_request.diff_url,
                    patch_url: issue.pull_request.patch_url
                } : null,
                closed_by: issue.closed_by ? {
                    login: issue.closed_by.login,
                    id: issue.closed_by.id,
                } : null,
            }));

            issuesData.push(...currentIssues); // Aggiungi i dati della pagina corrente
            page++;                            // Passa alla pagina successiva

        } while (fetchedData.data.length > 0); // Continua finché ci sono issue nella risposta

        // Salva tutti i dati raccolti in JSON
        fs.writeFileSync("issues_data.json", JSON.stringify(issuesData, null, 2));
        console.log("Dati delle issue salvati in issues_data.json");

    } catch (error) {
        console.error("Errore nella richiesta:", error);
    }
}

fetchAllIssues();