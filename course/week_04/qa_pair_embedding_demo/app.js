const sourceChunk =
  "Berlin, situated on the banks of the River Spree, serves as the capital of Germany and is its most populous city, with a metropolitan population exceeding six million residents. The city has been a center of European politics since reunification in 1990.";

const factoids = [
  {
    id: "F1",
    text: "Berlin is situated on the banks of the River Spree.",
    question: "Where is Berlin situated?",
    answer: "Berlin is situated on the banks of the River Spree.",
  },
  {
    id: "F2",
    text: "Berlin is the capital of Germany.",
    question: "What is the capital of Germany?",
    answer: "Berlin is the capital of Germany.",
  },
  {
    id: "F3",
    text: "Berlin is Germany's most populous city.",
    question: "What is Germany's most populous city?",
    answer: "Berlin is Germany's most populous city.",
  },
  {
    id: "F4",
    text: "Berlin's metropolitan population exceeds six million residents.",
    question: "How many residents live in Berlin's metropolitan area?",
    answer: "Berlin's metropolitan population exceeds six million residents.",
  },
  {
    id: "F5",
    text: "Berlin has been a center of European politics since reunification in 1990.",
    question: "Since when has Berlin been a center of European politics?",
    answer: "Berlin has been a center of European politics since reunification in 1990.",
  },
];

const dimensions = [
  "berlin",
  "germany",
  "capital",
  "city",
  "river",
  "spree",
  "population",
  "residents",
  "politics",
  "reunification",
  "time",
  "location",
  "question",
];

const featureWeights = [
  { terms: ["berlin"], dim: "berlin", weight: 1.0 },
  { terms: ["germany", "german"], dim: "germany", weight: 1.0 },
  { terms: ["capital"], dim: "capital", weight: 1.5 },
  { terms: ["city", "populous"], dim: "city", weight: 0.9 },
  { terms: ["river"], dim: "river", weight: 1.2 },
  { terms: ["spree"], dim: "spree", weight: 1.4 },
  { terms: ["population", "populous", "metropolitan"], dim: "population", weight: 1.3 },
  { terms: ["resident", "residents", "million"], dim: "residents", weight: 1.2 },
  { terms: ["politics", "political", "european"], dim: "politics", weight: 1.3 },
  { terms: ["reunification", "1990"], dim: "reunification", weight: 1.5 },
  { terms: ["when", "since"], dim: "time", weight: 0.9 },
  { terms: ["where", "situated", "banks"], dim: "location", weight: 1.0 },
  { terms: ["what", "where", "when", "how", "which"], dim: "question", weight: 0.4 },
];

const quickQueries = [
  "What is the capital of Germany?",
  "What is Germany's most populous city?",
  "Where is Berlin situated?",
  "How many residents live in Berlin's metropolitan area?",
  "Since when has Berlin been a center of European politics?",
];

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s']/g, " ")
    .split(/\s+/)
    .filter(Boolean);
}

function embedText(text) {
  const tokens = tokenize(text);
  const vector = dimensions.map(() => 0);

  for (const { terms, dim, weight } of featureWeights) {
    const dimIndex = dimensions.indexOf(dim);
    const hits = terms.reduce((count, term) => {
      return count + tokens.filter((token) => token.includes(term)).length;
    }, 0);
    vector[dimIndex] += hits * weight;
  }

  // A tiny genre penalty/boost: questions should match generated questions better
  // than raw paragraphs, but the answer text still contributes useful entity facts.
  if (text.includes("?")) {
    vector[dimensions.indexOf("question")] += 1.2;
  }

  return vector;
}

function cosine(left, right) {
  const dot = left.reduce((sum, value, index) => sum + value * right[index], 0);
  const leftNorm = Math.sqrt(left.reduce((sum, value) => sum + value * value, 0));
  const rightNorm = Math.sqrt(right.reduce((sum, value) => sum + value * value, 0));
  if (!leftNorm || !rightNorm) {
    return 0;
  }
  return dot / (leftNorm * rightNorm);
}

const qaIndex = factoids.map((factoid) => ({
  id: `qa_${factoid.id.toLowerCase()}`,
  artifactType: "qa_pair",
  sourceChunkId: "chunk_berlin_001",
  question: factoid.question,
  answer: factoid.answer,
  indexText: `${factoid.question} ${factoid.answer}`,
  vector: embedText(`${factoid.question} ${factoid.answer}`),
}));

const paragraphIndex = {
  id: "paragraph_chunk_berlin_001",
  artifactType: "whole_paragraph",
  sourceChunkId: "chunk_berlin_001",
  indexText: sourceChunk,
  vector: embedText(sourceChunk),
};

function renderStaticContent() {
  document.querySelector("#sourceChunk").textContent = sourceChunk;

  document.querySelector("#factoids").innerHTML = factoids
    .map(
      (factoid) => `
        <div class="factoid">
          <strong>${factoid.id}</strong>
          <span>${factoid.text}</span>
        </div>
      `,
    )
    .join("");

  document.querySelector("#qaPairs").innerHTML = qaIndex
    .map(
      (record) => `
        <section class="qa-card">
          <h3>${record.id}</h3>
          <p><strong>Q:</strong> ${record.question}</p>
          <p><strong>A:</strong> ${record.answer}</p>
          <p>Pointer: ${record.sourceChunkId}</p>
        </section>
      `,
    )
    .join("");

  document.querySelector("#indexRows").innerHTML = qaIndex
    .map(
      (record) => `
        <tr>
          <td>${record.id}</td>
          <td>${record.indexText}</td>
          <td>${record.sourceChunkId}</td>
        </tr>
      `,
    )
    .join("");

  document.querySelector("#quickQueries").innerHTML = quickQueries
    .map((query) => `<button type="button" data-query="${query}">${query}</button>`)
    .join("");

  document.querySelector("#queryInput").value = quickQueries[0];
  document.querySelector("#apiSnippet").textContent = buildApiSnippet();
}

function buildApiSnippet() {
  const payload = {
    model: "Qwen/Qwen3-Embedding-0.6B",
    input: [
      "What is the capital of Germany?",
      ...qaIndex.map((record) => record.indexText),
    ],
  };

  return `POST http://10.0.10.51:8000/embed-text/v1/embeddings
Content-Type: application/json

${JSON.stringify(payload, null, 2)}

# Search:
# 1. embed user query
# 2. embed QA index_text records
# 3. cosine(query_vector, index_vector)
# 4. follow source_chunk_id back to original evidence`;
}

function renderResultList(container, results) {
  container.innerHTML = results
    .map((result) => {
      const width = Math.max(0, Math.min(100, result.score * 100));
      return `
        <div class="result">
          <div class="result-top">
            <span>${result.id}</span>
            <span>${result.score.toFixed(4)}</span>
          </div>
          <div class="bar"><span style="width: ${width}%"></span></div>
          <p>${result.indexText}</p>
        </div>
      `;
    })
    .join("");
}

function runSearch() {
  const query = document.querySelector("#queryInput").value.trim();
  const queryVector = embedText(query);

  const qaResults = qaIndex
    .map((record) => ({
      ...record,
      score: cosine(queryVector, record.vector),
    }))
    .sort((left, right) => right.score - left.score);

  const paragraphScore = cosine(queryVector, paragraphIndex.vector);
  const paragraphResults = [{ ...paragraphIndex, score: paragraphScore }];
  const winner = qaResults[0];

  renderResultList(document.querySelector("#qaResults"), qaResults);
  renderResultList(document.querySelector("#paragraphResult"), paragraphResults);

  document.querySelector("#evidence").innerHTML = `
    <div class="answer-box">
      <h3>Top synthetic hit</h3>
      <p><strong>${winner.question}</strong><br />${winner.answer}</p>
    </div>
    <div class="source-box">
      <h3>Evidence actually used for final answer</h3>
      <p>${sourceChunk}</p>
    </div>
  `;
}

function bindEvents() {
  document.querySelector("#searchButton").addEventListener("click", runSearch);
  document.querySelector("#quickQueries").addEventListener("click", (event) => {
    const button = event.target.closest("button[data-query]");
    if (!button) {
      return;
    }
    document.querySelector("#queryInput").value = button.dataset.query;
    runSearch();
  });
}

renderStaticContent();
bindEvents();
runSearch();
