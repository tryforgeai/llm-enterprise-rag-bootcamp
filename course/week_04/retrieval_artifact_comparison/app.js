const quickQueries = [
  "What is a proposition in Dense-X?",
  "Why does proposition-level retrieval help RAG?",
  "What does PRML Chapter 2 teach?",
  "How does Bayesian linear regression use model evidence?",
  "Why can linear regression use nonlinear basis functions?",
];

let backendStatus = null;
let latestRanked = [];

async function apiGet(path) {
  const response = await fetch(path, { cache: "no-store" });
  const payload = await response.json();
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.error || `HTTP ${response.status}`);
  }
  return payload;
}

async function apiPost(path, body = {}) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const payload = await response.json();
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.error || `HTTP ${response.status}`);
  }
  return payload;
}

async function checkBackend() {
  try {
    backendStatus = await apiGet("/api/status");
    updateModeBadges();
  } catch (error) {
    backendStatus = null;
    document.querySelector("#modeBadge").textContent = "Server required";
    document.querySelector("#indexBadge").textContent = "Run python3 server.py";
    document.querySelector("#answerMode").textContent = "server offline";
    writeStatus(`This demo no longer has a TF-IDF fallback.\nStart server.py to use SV cluster.\n\n${error.message}`);
  }
}

function updateModeBadges() {
  document.querySelector("#modeBadge").textContent = "SV cluster only";
  document.querySelector("#answerMode").textContent = "SV LLM + SV embeddings";

  if (!backendStatus.index_exists) {
    document.querySelector("#indexBadge").textContent = "Build SV index";
    writeStatus(
      `Connected to SV cluster config.\nEmbedding: ${backendStatus.default_model}\nChat: ${backendStatus.default_chat_model}\n\nClick "Generate QA pairs" or "Build SV index".`,
    );
    return;
  }

  const qaNote = backendStatus.generated_qa_exists ? "SV QA pairs ready" : "manual QA only";
  document.querySelector("#indexBadge").textContent = `${backendStatus.record_count} records · ${backendStatus.vector_dimensions}d`;
  writeStatus(
    `Ready.\nEmbedding: ${backendStatus.default_model}\nChat: ${backendStatus.default_chat_model}\n${qaNote}\nIndex: ${backendStatus.index_path}`,
  );
}

function writeStatus(message) {
  document.querySelector("#statusLog").textContent = message;
}

async function generateQaPairs() {
  const button = document.querySelector("#generateQaButton");
  button.disabled = true;
  writeStatus("Calling SV chat model to generate QA pairs from raw chunks...");

  try {
    const payload = await apiPost("/api/generate-qa", { questions_per_chunk: 3 });
    writeStatus(
      `Generated ${payload.qa_count} QA pairs with ${payload.model}.\nSaved: ${payload.path}\n\nNow click "Build SV index" to embed them.`,
    );
    document.querySelector("#ragAnswer").textContent = payload.qa_pairs
      .slice(0, 6)
      .map((item) => `Q: ${item.question}\nA: ${item.answer}`)
      .join("\n\n");
    await checkBackend();
  } catch (error) {
    writeStatus(`QA generation failed:\n${error.message}`);
  } finally {
    button.disabled = false;
  }
}

async function buildSvIndex() {
  const button = document.querySelector("#buildButton");
  button.disabled = true;
  writeStatus("Calling SV embedding model to embed all artifact records...");

  try {
    const payload = await apiPost("/api/build-index", {});
    writeStatus(
      `Built SV index: ${payload.record_count} records · ${payload.vector_dimensions}d\nModel: ${payload.model}\nEndpoint: ${payload.endpoint}`,
    );
    await checkBackend();
    await runSearch();
  } catch (error) {
    writeStatus(`SV index build failed:\n${error.message}`);
  } finally {
    button.disabled = false;
  }
}

async function runSearch() {
  const query = document.querySelector("#queryInput").value.trim();
  if (!query) return;

  if (!backendStatus?.index_exists) {
    writeStatus("No SV vector index yet. Click Build SV index first.");
    return;
  }

  writeStatus("Embedding query with SV cluster and searching dense vectors...");
  try {
    const payload = await apiPost("/api/search", { query, top_k: 12 });
    latestRanked = payload.results.map(normalizeRecord);
    renderRankedResults(latestRanked);
    document.querySelector("#ragAnswer").textContent = payload.extractive_answer;
    writeStatus(`SV search complete.\nEmbedding model: ${payload.model}`);
  } catch (error) {
    writeStatus(`SV search failed:\n${error.message}`);
  }
}

async function synthesizeAnswer() {
  const query = document.querySelector("#queryInput").value.trim();
  if (!query) return;

  if (!backendStatus?.index_exists) {
    writeStatus("No SV vector index yet. Click Build SV index first.");
    return;
  }

  const button = document.querySelector("#answerButton");
  button.disabled = true;
  writeStatus("Retrieving evidence, then calling SV chat model to synthesize an answer...");

  try {
    const payload = await apiPost("/api/answer", { query, top_k: 5 });
    latestRanked = payload.results.map(normalizeRecord);
    renderRankedResults(latestRanked);
    document.querySelector("#ragAnswer").textContent = payload.answer;
    writeStatus(`RAG answer complete.\nEmbedding: ${payload.model}\nChat: ${payload.chat_model}`);
  } catch (error) {
    writeStatus(`SV RAG answer failed:\n${error.message}`);
  } finally {
    button.disabled = false;
  }
}

function normalizeRecord(record) {
  return {
    id: record.record_id,
    type: record.artifact_type,
    source: record.source_id,
    title: record.title,
    text: record.display_text,
    score: record.score,
    pointer: record.source_pointer,
  };
}

function renderRankedResults(ranked) {
  const best = ranked[0];
  document.querySelector("#bestScore").textContent = best ? best.score.toFixed(3) : "0.000";
  document.querySelector("#bestTitle").textContent = best ? best.title : "No result";
  document.querySelector("#bestText").textContent = best ? best.text : "";
  document.querySelector("#bestType").textContent = best ? labelType(best.type) : "-";
  document.querySelector("#bestSource").textContent = best ? best.source : "-";

  for (const type of ["raw_chunk", "abstractive_summary", "proposition", "qa_pair"]) {
    const results = ranked.filter((record) => record.type === type).slice(0, 4);
    document.querySelector(`#${type}`).innerHTML = results.map(renderCard).join("");
  }
}

function labelType(type) {
  return type.replace(/_/g, " ");
}

function renderCard(record) {
  const width = Math.max(0, Math.min(100, record.score * 100));
  return `
    <article class="result-card">
      <div class="result-head">
        <strong>${escapeHtml(record.title)}</strong>
        <span class="score">${record.score.toFixed(3)}</span>
      </div>
      <div class="bar"><span style="width:${width}%"></span></div>
      <p>${escapeHtml(record.text)}</p>
      <div class="source">${escapeHtml(record.source)} · ${escapeHtml(record.id)} · ${escapeHtml(record.pointer || "")}</div>
    </article>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderQuickQueries() {
  document.querySelector("#quickQueries").innerHTML = quickQueries
    .map((query) => `<button type="button" data-query="${escapeHtml(query)}">${escapeHtml(query)}</button>`)
    .join("");

  document.querySelector("#quickQueries").addEventListener("click", (event) => {
    const button = event.target.closest("button[data-query]");
    if (!button) return;
    document.querySelector("#queryInput").value = button.dataset.query;
    runSearch();
  });
}

function renderSnippet() {
  document.querySelector("#svSnippet").textContent = `SV cluster endpoints used by this demo:

Chat / LLM:
POST http://10.0.10.51:8000/v1/chat/completions
model: openai/gpt-oss-20b

Text embedding:
POST http://10.0.10.51:8000/embed-text/v1/embeddings
model: Qwen/Qwen3-Embedding-0.6B

Pipeline:
1. raw chunks -> SV chat -> generated QA pairs
2. raw/summary/proposition/QA index_text -> SV embedding -> 1024d vectors
3. user query -> SV embedding -> cosine top-k
4. top-k evidence -> SV chat -> final grounded answer`;
}

document.querySelector("#runButton").addEventListener("click", runSearch);
document.querySelector("#answerButton").addEventListener("click", synthesizeAnswer);
document.querySelector("#buildButton").addEventListener("click", buildSvIndex);
document.querySelector("#generateQaButton").addEventListener("click", generateQaPairs);
renderQuickQueries();
renderSnippet();
document.querySelector("#queryInput").value = quickQueries[0];
checkBackend().then(runSearch);
