# NOMI — Master Roadmap
*Curriculum, Path to a Custom AI Model, and Team Levels*

This combines the handoff PDF and the README into one working plan. Future features from the README are the north star; the handoff doc's roadmap (v0.1–v0.5) is still the near-term build order.

---

## A. Concepts & Courses You Need

Grouped by domain, roughly in the order you'll touch them.

### A1. Math & CS Foundations (already underway)
- **Calculus** — you're already using Professor Leonard for this. Keep going through multivariable calc; you'll need gradients/partial derivatives once you touch ML training.
- **Linear Algebra** — matrices, eigenvalues, vector spaces. This is the actual language of neural nets (weights are matrices, embeddings are vectors). Your recent probability/linear algebra problem set is directly on-path.
- **Probability & Statistics** — Bayesian inference (which you've been drilling) is exactly what underlies how language models reason about uncertainty, and how you'll later design NOMI's memory-relevance scoring.
- **Data Structures & Algorithms** — needed for the memory/knowledge-graph system specifically (graphs, hashing, trees for retrieval).

### A2. Programming & Systems
- **Python** — primary language for the v0.1–v0.5 prototype (fastest path to a working device).
- **C++** — you're already building toward this for NVIDIA; it becomes essential once you optimize NOMI's inference for the Pi or move to a custom board.
- **Git & Linux** — already in your plan; non-negotiable for any team project.
- **Embedded systems basics** — GPIO, I2C/SPI, interrupts, real-time constraints. Raspberry Pi docs + "Raspberry Pi for Dummies" style resources are enough to start.

### A3. Computer Vision (Feature 1: Visual Understanding)
- OpenCV fundamentals (image capture, preprocessing)
- CNNs / object detection basics
- Courses: **Stanford CS231n** (free, YouTube + notes), **fast.ai Practical Deep Learning for Coders**

### A4. Audio / Speech (capture → text → speech)
- Basic digital signal processing concepts (sampling, noise reduction)
- Speech-to-text: Whisper (OpenAI, open-source) or Vosk (fully offline, lightweight — better for Pi)
- Text-to-speech: Piper or Coqui TTS (both run offline, important for your "quiet, privacy-first" philosophy)

### A5. NLP & LLM Integration
- How transformers work at a conceptual level (attention, tokens, context windows)
- Prompt engineering — designing NOMI's "personality" through system prompts initially
- API integration patterns (you'll use Claude/GPT APIs for v0.1–v0.3 before any custom model)
- RAG (Retrieval-Augmented Generation) and vector embeddings — this is literally how "long-term memory" gets implemented technically

### A6. Databases & Memory Systems (Features 4 & 5)
- SQLite — your v0.1–v0.2 memory store
- Vector databases — Chroma or FAISS (both free, run locally, no cloud dependency — fits your privacy-first principle)
- Knowledge graphs — Neo4j basics, for when memory evolves beyond simple recall into relationships between people/places/topics

### A7. Hardware / Electronics
- Basic circuits and power management (battery life is going to be your hardest v0.1 constraint)
- Microcontroller programming if you eventually move off Pi to something like an ESP32 for the "future hardware" redesign

### A8. Product / UX
- Human-robot interaction principles — how "personality" through a small display actually reads as alive vs. gimmicky
- This matters more than it sounds; it's the difference between NOMI feeling like a pet and feeling like a gadget

---

## B. Path Toward a Custom AI Model (Later Versions)

You said you want NOMI running on a model **you built**, eventually. Being direct about the reality here so the plan stays credible:

**Training a frontier-class LLM from scratch is not realistic for an independent team** — that takes many millions of dollars in compute and huge curated datasets. That's not the actual goal, though. Here's the realistic progression:

| Stage | What it means | Skills needed |
|---|---|---|
| **1. API-based** (v0.1–v0.5) | Claude/GPT API does the reasoning | Prompt engineering, API integration |
| **2. Fine-tuning** | Take an open model (Llama, Phi, Gemma small variants) and fine-tune it on NOMI-specific conversations/personality | PyTorch, LoRA/QLoRA fine-tuning, Hugging Face ecosystem |
| **3. Distillation for edge** | Compress a fine-tuned model down to run *on-device* on the Pi (or custom board) without cloud calls | Quantization, pruning, knowledge distillation |
| **4. Custom small architecture** | Design your own lightweight model architecture specialized for NOMI's narrow domain (companion conversation + vision captioning) rather than general intelligence | Deep learning theory, transformer internals, training infrastructure |

This is genuinely where your NVIDIA path matters — GPU programming, CUDA, and edge-AI optimization (their Jetson line is built almost exactly for this use case) are directly transferable skills. An NVIDIA internship, especially anything touching Jetson or TensorRT, would give you real infrastructure experience for Stage 3–4.

**Recommended learning order for this track:**
1. Andrej Karpathy's *"Neural Networks: Zero to Hero"* (YouTube) — best free intro to building models from scratch
2. Stanford CS231n (vision) and CS224n (NLP) — free lecture notes/videos
3. Hugging Face's free courses on fine-tuning and transformers
4. NVIDIA's own Jetson/TensorRT documentation once you're ready for edge deployment

---

## C. Team Structure & Levels

Since you want to recruit and gate progress by achievement, here's a level system — each level has a clear goal, the roles it needs, and an exit condition before you unlock the next one.

### Level 0 — Solo Prototype *(You, now)*
**Goal:** v0.1 — capture image/audio → send to AI API → speak response, on a breadboarded Pi.
**Roles needed:** Just you.
**Exit criteria:** A working end-to-end loop, even if ugly. This is your proof-of-concept and pitch demo.

### Level 1 — Core Loop Team *(2–3 people)*
**Goal:** v0.1 polish + v0.2 (session memory).
**Roles to recruit:** A second Python/embedded dev, and someone comfortable with audio pipelines (STT/TTS).
**Exit criteria:** NOMI holds a coherent conversation across multiple questions in one session, runs reasonably fast on the Pi.

### Level 2 — Memory & Personality Team *(4–6 people)*
**Goal:** v0.3 (long-term memory) + v0.5 (animated face/personality).
**Roles to recruit:** A backend/database person (vector DB + knowledge graph), a UX/embedded-display person for the animated eyes.
**Exit criteria:** NOMI remembers something from last week unprompted, and its face/expressions are recognizable and not distracting.

### Level 3 — Hardware & Product Team *(6–10 people)*
**Goal:** Move off breadboard Pi to a real enclosure, possibly custom PCB.
**Roles to recruit:** An electronics/PCB engineer, an industrial designer.
**Exit criteria:** A device that looks and feels like a product, survives a full day on battery.

### Level 4 — Custom AI Team *(add 2–3 ML specialists)*
**Goal:** Fine-tune and distill your own model for on-device inference (Stage 2–3 from Section B).
**Roles to recruit:** ML engineers with fine-tuning/quantization experience.
**Exit criteria:** NOMI can run core conversation + vision captioning without a cloud API call.

### Level 5 — Scale Team
**Goal:** Manufacturing, business operations, wider rollout.
**Roles to recruit:** Ops, business/legal, manufacturing partner.
**Exit criteria:** Beyond scope for now — revisit once Level 4 is real.

**Practical note on recruiting:** Don't recruit for Level 2+ roles until Level 0/1 is demoable. A working prototype, even rough, is 10x more convincing to potential teammates than a spec doc — people join momentum, not plans.

---

## Immediate Next Step

Level 0 is entirely yours to build right now with what you already know (Python) and what you're already learning (C++, Git/Linux). Want to start there — setting up the Pi capture → API → speech loop?
