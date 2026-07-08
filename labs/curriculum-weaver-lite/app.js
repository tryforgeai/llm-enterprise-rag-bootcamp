const concepts = {
  vectors: {
    name: "Vectors",
    summary: "Represent tokens, words, and hidden states as directions in a space.",
    prerequisites: [],
    why: "Attention starts with vector representations before it can compare anything.",
    depth: "intro",
    masteryBoost: 0.05,
  },
  dot_product: {
    name: "Dot Product",
    summary: "Measures alignment between two vectors and becomes the score behind attention.",
    prerequisites: ["vectors"],
    why: "QK^T is built from many dot products.",
    depth: "intro",
    masteryBoost: 0.08,
  },
  matrix_multiplication: {
    name: "Matrix Multiplication",
    summary: "Batches many vector comparisons into one efficient operation.",
    prerequisites: ["vectors", "dot_product"],
    why: "Attention compares every query with every key using matrix multiplication.",
    depth: "intro",
    masteryBoost: 0.06,
  },
  softmax: {
    name: "Softmax",
    summary: "Turns raw scores into a probability-like distribution of weights.",
    prerequisites: ["dot_product"],
    why: "Attention needs scores to become weights before values can be mixed.",
    depth: "intermediate",
    masteryBoost: 0.12,
  },
  qkv: {
    name: "Query, Key, Value",
    summary: "Three learned projections: what is looking, what can be matched, and what is retrieved.",
    prerequisites: ["matrix_multiplication"],
    why: "Q/K/V is the vocabulary of self-attention.",
    depth: "intermediate",
    masteryBoost: 0.12,
  },
  scaled_dot_product_attention: {
    name: "Scaled Dot-Product Attention",
    summary: "Computes softmax(QK^T / sqrt(d_k))V.",
    prerequisites: ["qkv", "softmax", "matrix_multiplication"],
    why: "This is the core mathematical operation inside self-attention.",
    depth: "advanced",
    masteryBoost: 0.16,
  },
  self_attention: {
    name: "Self-Attention",
    summary: "Lets every token retrieve contextual information from every other token in the same sequence.",
    prerequisites: ["scaled_dot_product_attention"],
    why: "This is the target concept for the demo.",
    depth: "advanced",
    masteryBoost: 0.18,
  },
  multi_head_attention: {
    name: "Multi-Head Attention",
    summary: "Runs multiple attention operations in parallel so the model can attend to different relationships.",
    prerequisites: ["self_attention"],
    why: "This is the next step after single-head self-attention is understood.",
    depth: "advanced",
    masteryBoost: 0.12,
  },
};

const sourceCards = {
  vectors: [
    {
      source: "Week 2 lecture notes",
      citation: "Tokenization and continuous machine language",
      summary: "Discrete tokens become continuous vectors so gradients and similarity can operate on them.",
    },
  ],
  dot_product: [
    {
      source: "Week 2 lecture notes",
      citation: "Dot product similarity",
      summary: "Vector similarity can be computed through dot products or cosine similarity.",
    },
  ],
  matrix_multiplication: [
    {
      source: "Linear algebra review",
      citation: "Matrix multiplication as batched dot products",
      summary: "Matrix multiplication compresses many pairwise vector comparisons into one operation.",
    },
  ],
  softmax: [
    {
      source: "Week 2 lecture notes",
      citation: "Softmax and temperature",
      summary: "Softmax converts arbitrary scores into a normalized distribution over choices.",
    },
  ],
  qkv: [
    {
      source: "Transformer tutorial",
      citation: "Query, key, value projections",
      summary: "Queries ask what to find, keys describe what can match, and values carry the content to mix.",
    },
  ],
  scaled_dot_product_attention: [
    {
      source: "Vaswani et al. 2017",
      citation: "Attention Is All You Need, Section 3.2.1",
      summary: "Scaled dot-product attention computes softmax(QK^T / sqrt(d_k))V.",
    },
    {
      source: "Week 2 lecture notes",
      citation: "Why divide by sqrt(d_k)",
      summary: "Scaling keeps high-dimensional dot products from making softmax too sharp.",
    },
  ],
  self_attention: [
    {
      source: "Transformer tutorial",
      citation: "Self-attention over a sequence",
      summary: "Each token uses the same sequence as its source of keys and values.",
    },
  ],
  multi_head_attention: [
    {
      source: "Vaswani et al. 2017",
      citation: "Attention Is All You Need, Section 3.2.2",
      summary: "Multi-head attention lets the model jointly attend to information from different representation subspaces.",
    },
  ],
};

const profiles = {
  beginner: {
    label: "Mira, new to transformers",
    known: ["vectors"],
    weak: ["dot_product", "softmax"],
    preference: "Intuition first, then math.",
    mastery: {
      vectors: 0.72,
      dot_product: 0.38,
      matrix_multiplication: 0.34,
      softmax: 0.24,
      qkv: 0.08,
      scaled_dot_product_attention: 0.02,
      self_attention: 0,
    },
  },
  intermediate: {
    label: "Rosso, math + code learner",
    known: ["vectors", "dot_product", "matrix_multiplication"],
    weak: ["softmax", "qkv"],
    preference: "Mathematical explanation with a code sketch.",
    mastery: {
      vectors: 0.92,
      dot_product: 0.82,
      matrix_multiplication: 0.76,
      softmax: 0.46,
      qkv: 0.32,
      scaled_dot_product_attention: 0.12,
      self_attention: 0.08,
    },
  },
  advanced: {
    label: "Kai, needs the scaling detail",
    known: ["vectors", "dot_product", "matrix_multiplication", "softmax", "qkv"],
    weak: ["scaled_dot_product_attention"],
    preference: "Skip basics. Explain the equation and failure mode.",
    mastery: {
      vectors: 0.96,
      dot_product: 0.92,
      matrix_multiplication: 0.88,
      softmax: 0.84,
      qkv: 0.78,
      scaled_dot_product_attention: 0.44,
      self_attention: 0.36,
    },
  },
};

const quizBank = {
  scaled_dot_product_attention: {
    question: "Why does scaled dot-product attention divide QK^T by sqrt(d_k)?",
    options: [
      "To keep dot-product scores from making softmax too sharp in high dimensions.",
      "To make the value matrix smaller before multiplication.",
      "To remove the need for learned projections.",
    ],
    answer: 0,
  },
  softmax: {
    question: "What does softmax do to attention scores?",
    options: [
      "Turns scores into normalized weights.",
      "Deletes negative scores from the sequence.",
      "Converts tokens into word pieces.",
    ],
    answer: 0,
  },
  qkv: {
    question: "In Q/K/V attention, what do values carry?",
    options: [
      "The content that gets mixed after attention weights are computed.",
      "Only the source citations.",
      "The model's final classification labels.",
    ],
    answer: 0,
  },
  self_attention: {
    question: "What makes self-attention 'self' attention?",
    options: [
      "The sequence attends to positions within the same sequence.",
      "The model trains without labels.",
      "The attention weights are fixed by hand.",
    ],
    answer: 0,
  },
};

const targetConcept = "self_attention";
const masteryThreshold = 0.7;
let activeProfileKey = "intermediate";
let currentPath = [];
let activeConceptId = null;

const profileCard = document.querySelector("#profileCard");
const diagnosticList = document.querySelector("#diagnosticList");
const pathList = document.querySelector("#pathList");
const traceLog = document.querySelector("#traceLog");
const lessonTitle = document.querySelector("#lessonTitle");
const lessonBody = document.querySelector("#lessonBody");
const goalInput = document.querySelector("#goal");

function collectPrerequisites(conceptId, seen = new Set()) {
  const concept = concepts[conceptId];
  if (!concept) return [];
  for (const prerequisite of concept.prerequisites) {
    if (!seen.has(prerequisite)) {
      seen.add(prerequisite);
      collectPrerequisites(prerequisite, seen);
    }
  }
  return Array.from(seen);
}

function orderConcepts(conceptIds) {
  const ordered = [];
  const visited = new Set();
  function visit(id) {
    if (visited.has(id)) return;
    visited.add(id);
    for (const prerequisite of concepts[id]?.prerequisites || []) {
      if (conceptIds.includes(prerequisite)) visit(prerequisite);
    }
    ordered.push(id);
  }
  conceptIds.forEach(visit);
  return ordered;
}

function buildPath(profile) {
  const prerequisites = collectPrerequisites(targetConcept);
  const candidates = [...prerequisites, targetConcept, "multi_head_attention"];
  const missing = candidates.filter((id) => (profile.mastery[id] || 0) < masteryThreshold);
  return orderConcepts(missing);
}

function masteryClass(score) {
  if (score >= 0.7) return "strong";
  if (score >= 0.4) return "medium";
  return "weak";
}

function masteryLabel(score) {
  if (score >= 0.7) return "strong";
  if (score >= 0.4) return "developing";
  return "needs support";
}

function renderProfile() {
  const profile = profiles[activeProfileKey];
  profileCard.innerHTML = `
    <strong>${profile.label}</strong>
    <p>${profile.preference}</p>
    <div class="tag-row">
      ${profile.known.map((item) => `<span class="tag">knows ${concepts[item].name}</span>`).join("")}
      ${profile.weak.map((item) => `<span class="tag">weak ${concepts[item].name}</span>`).join("")}
    </div>
  `;
}

function renderDiagnostics() {
  const profile = profiles[activeProfileKey];
  const ids = ["dot_product", "matrix_multiplication", "softmax", "qkv", "scaled_dot_product_attention"];
  diagnosticList.innerHTML = ids
    .map((id) => {
      const score = profile.mastery[id] || 0;
      const level = masteryClass(score);
      return `
        <div class="diagnostic-item ${level}">
          <strong>${concepts[id].name}</strong>
          <span>${masteryLabel(score)} · estimated mastery ${Math.round(score * 100)}%</span>
          <div class="meter"><div class="meter-fill" style="width: ${Math.round(score * 100)}%"></div></div>
        </div>
      `;
    })
    .join("");
}

function renderPath() {
  const profile = profiles[activeProfileKey];
  currentPath = buildPath(profile);
  pathList.innerHTML = currentPath
    .map((id, index) => {
      const concept = concepts[id];
      const knownPrereqs = concept.prerequisites.filter((pre) => (profile.mastery[pre] || 0) >= masteryThreshold);
      const missingPrereqs = concept.prerequisites.filter((pre) => (profile.mastery[pre] || 0) < masteryThreshold);
      return `
        <article class="path-card ${id === activeConceptId ? "active" : ""}" data-concept="${id}">
          <span class="number">${String(index + 1).padStart(2, "0")}</span>
          <h3>${concept.name}</h3>
          <p>${concept.summary}</p>
          <span class="meta">
            ${knownPrereqs.length ? `ready from ${knownPrereqs.map((pre) => concepts[pre].name).join(", ")}` : "foundation step"}
            ${missingPrereqs.length ? ` · repairs ${missingPrereqs.map((pre) => concepts[pre].name).join(", ")}` : ""}
          </span>
        </article>
      `;
    })
    .join("");

  document.querySelectorAll(".path-card").forEach((card) => {
    card.addEventListener("click", () => {
      activeConceptId = card.dataset.concept;
      renderPath();
      renderLesson(activeConceptId);
      renderTrace();
    });
  });

  if (!activeConceptId && currentPath.length) {
    activeConceptId = currentPath[Math.min(2, currentPath.length - 1)];
    renderPath();
    renderLesson(activeConceptId);
  }
}

function renderTrace() {
  const profile = profiles[activeProfileKey];
  const skipped = Object.keys(concepts).filter((id) => (profile.mastery[id] || 0) >= masteryThreshold);
  const goal = goalInput.value.trim();
  traceLog.innerHTML = `
    <div class="trace-card">
      <strong>Goal parsed</strong>
      ${goal || "Learn self-attention"}
      <span>Mapped to target concept: ${concepts[targetConcept].name}</span>
    </div>
    <div class="trace-card">
      <strong>Mastery threshold</strong>
      Include concepts below ${Math.round(masteryThreshold * 100)}% estimated mastery.
      <span>${skipped.length ? `Skipped: ${skipped.map((id) => concepts[id].name).join(", ")}` : "No concepts skipped."}</span>
    </div>
    <div class="trace-card">
      <strong>Path rule</strong>
      Traverse prerequisite graph, remove mastered concepts, topologically order the remaining concepts.
      <span>${currentPath.length} teachable steps selected.</span>
    </div>
    <div class="trace-card">
      <strong>Retrieval mode</strong>
      Step 1 uses curated source cards. Step 2 will replace this with hybrid RAG and metadata filters.
      <span>Pedagogy first, retrieval second.</span>
    </div>
  `;
}

function renderLesson(conceptId) {
  const concept = concepts[conceptId];
  const cards = sourceCards[conceptId] || [];
  const quiz = quizBank[conceptId] || quizBank.scaled_dot_product_attention;
  lessonTitle.textContent = concept.name;
  lessonBody.classList.remove("empty-state");
  lessonBody.innerHTML = `
    <section class="lesson-section">
      <h3>Why this comes now</h3>
      <p>${concept.why}</p>
    </section>
    <section class="lesson-section">
      <h3>Teaching explanation</h3>
      <p>${concept.summary}</p>
      <p>For this learner, the system selected this concept because it is either below the mastery threshold or directly unlocks ${concepts[targetConcept].name}.</p>
    </section>
    <section class="lesson-section">
      <h3>Source cards</h3>
      <div class="source-grid">
        ${cards
          .map(
            (card) => `
              <div class="source-card">
                <strong>${card.source}</strong>
                <p>${card.summary}</p>
                <span class="tag">${card.citation}</span>
              </div>
            `,
          )
          .join("")}
      </div>
    </section>
    <section class="lesson-section">
      <h3>Code sketch</h3>
      <pre class="code-block"><code>scores = Q @ K.T / sqrt(d_k)
weights = softmax(scores)
context = weights @ V</code></pre>
    </section>
    <section class="quiz-box">
      <h3>Quiz check</h3>
      <p>${quiz.question}</p>
      <div class="quiz-options">
        ${quiz.options.map((option, index) => `<button class="quiz-button" data-answer="${index}">${option}</button>`).join("")}
      </div>
    </section>
  `;

  document.querySelectorAll(".quiz-button").forEach((button) => {
    button.addEventListener("click", () => {
      const selected = Number(button.dataset.answer);
      const correct = selected === quiz.answer;
      button.classList.add(correct ? "correct" : "incorrect");
      if (correct) {
        const profile = profiles[activeProfileKey];
        profile.mastery[conceptId] = Math.min(1, (profile.mastery[conceptId] || 0) + concept.masteryBoost);
        renderDiagnostics();
        renderTrace();
      }
    });
  });
}

document.querySelectorAll(".segment").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".segment").forEach((segment) => segment.classList.remove("active"));
    button.classList.add("active");
    activeProfileKey = button.dataset.profile;
    activeConceptId = null;
    renderProfile();
    renderDiagnostics();
    renderPath();
    renderTrace();
  });
});

document.querySelector("#generatePath").addEventListener("click", () => {
  activeConceptId = null;
  renderPath();
  renderTrace();
});

renderProfile();
renderDiagnostics();
renderPath();
renderTrace();
