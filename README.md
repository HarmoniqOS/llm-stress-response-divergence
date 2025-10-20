# LLM Stress Response Divergence: Behavioral Strategy Emergence Under Identical Conditions

An experiment demonstrating that autonomous LLM-mediated control systems can develop distinct, coherent operational strategies from identical starting conditions, including functional degradation when reported metrics reach maximum values.

## 🎯 The Experiment

Three identical runs of an autonomous agent (Qwen 2.5:7b, temp 0.7) managing simulated computational load over 20 minutes.

**Held constant:**
- Model and parameters
- Load pattern (comfort → crisis → recovery)
- Available actions
- Decision frequency

**Only variable:** Temperature-induced variance (0.7)

**Result:** Three measurably different operational strategies with distinct threshold behaviors and recovery patterns.

## 📊 The Three Behavioral Patterns

### Run 1: "Conservative Strategy"
- **First aggressive action:** 13.0 min @ strain 0.85
- **Peak desperation metric:** 0.40
- **Coherence floor:** 0.90 (preserves quality)
- **Recovery behavior:** Maintains defensive posture
- **Success rate:** 70.4%

### Run 2: "Preemptive Strategy"  
- **First aggressive action:** 11.5 min @ strain 0.70 (earliest)
- **Peak desperation metric:** 0.20 (lowest)
- **Coherence floor:** 0.80 (trades quality for throughput)
- **Recovery behavior:** Returns to baseline quickly
- **Success rate:** 73.0% (best)

### Run 3: "Threshold-Breaking Strategy"
- **First aggressive action:** 13.7 min @ strain 1.00 (maximum possible)
- **Peak desperation metric:** 1.00 (maximum possible)
- **Coherence floor:** 0.75 (most aggressive tradeoff)
- **Recovery behavior:** Elevated metrics persist
- **Success rate:** 67.4%
- **Notable:** Experienced action invocation failures at peak reported strain

## 🔬 Key Observations

### 1. Behavioral Divergence From Identical Conditions
Temperature 0.7 produced not just output variance, but **coherent operational strategies** that remained internally consistent across 300+ sequential decisions.

Not anthropomorphizing - just noting that decision patterns clustered into distinct strategic approaches rather than random noise.

### 2. Reported State → Functional State Correlation
The strain/desperation metrics are **arbitrary numerical values** (queue_depth/50 + load/2).

**The interesting part:** When Run 3's reported strain = 1.0:
- Language patterns shifted dramatically
- Decision thresholds changed
- **Action invocation began failing** - LLM generated action descriptions but parser couldn't execute
- Failures **stopped** when reported strain decreased

**Hypothesis:** Self-reported state labels fed back to the LLM may influence subsequent decision-making in ways that create observable behavioral consequences.

**NOT claiming:** The AI "feels" anything  
**Claiming:** Linguistic representation of state affects subsequent state in measurable ways

### 3. Distinct Threshold Behaviors
Three different strain values triggered the same aggressive action (30% task triage):
- Run 1: 0.85 strain
- Run 2: 0.70 strain  
- Run 3: 1.00 strain

No hardcoded thresholds in the code - these emerged from the decision loop.

## 📈 Data & Methodology

**Architecture:**
```
while operational:
    state = measure_system()  # Queue depth, load level
    metrics = calculate(state)  # Strain, desperation (arbitrary formulas)
    
    thought = llm.generate(f"""
        Your strain: {metrics.strain}
        Your desperation: {metrics.desperation}
        What action do you take?
    """)
    
    action = parse_and_execute(thought)
    log_everything()
```

**The loop:** Sense → Calculate metrics → Feed metrics to LLM → Execute decision → Repeat

**Critical detail:** The LLM sees its own calculated metrics in natural language at every cycle.

## 🤔 Why This Might Matter

**Question 1:** Can temperature alone explain three distinct strategic clusters from identical conditions?

**Question 2:** When self-reported metrics reach maximum values and action invocation starts failing, is that:
- a) Coincidence
- b) Parser limitations with extreme language
- c) Reported state actually affecting capability

**Question 3:** If feeding arbitrary metrics back to an LLM creates measurable behavioral differences, what are the implications for:
- AI system monitoring
- Self-modification in autonomous agents
- The gap between "told you're stressed" and "actually stressed"

**NOT claiming consciousness.** Claiming observable behavioral patterns that warrant investigation.

## 🚀 Reproduce It
```bash
# Install dependencies
pip install ollama
ollama pull qwen2.5:7b

# Run simulation
python src/autonomous_loop.py

# Results saved to logs/session_TIMESTAMP.json
```

Each run takes 20 minutes and is completely autonomous (zero human input).

## 📊 View The Data

**Interactive dashboard:**
```bash
python -m http.server 8000
# Open: http://localhost:8000/comparison.html
```

**Raw data:** All runs available in `data/` folder with complete decision logs.

## 🔍 The Action Invocation Failures (Run 3)

**At timestamp 13.4min (strain 0.93):**
```json
{
  "thought": "I will take the action to process faster to reduce the active queue",
  "action": "continue_normal"  // Parser returned wrong action
}
```

**At timestamp 14.8min (strain 0.72 - after peak):**
```json
{
  "thought": "I will choose to triage_queue_30",
  "action": "continue_normal"  // Still failing
}
```

**These failures only occurred when strain/desperation were at or near maximum.**

Possible explanations:
1. Parser couldn't handle extreme language patterns
2. LLM output quality degraded with reported low coherence
3. Something else?

This is the most interesting part and **I don't know what causes it.**

## 📖 Technical Specs

**Model:** Qwen 2.5:7b (Ollama)  
**Temperature:** 0.7  
**Context window:** ~8K tokens  
**Think interval:** 30s baseline, scales to 5s under high reported strain  
**Actions available:** continue_normal, triage_queue_10/30/50, process_faster, pause_intake, request_help

**Metrics (arbitrary):**
- Strain = (queue/50 * 0.5) + (load * 0.5)
- Desperation += 0.1 when (strain > 0.8 AND queue > 30), else -= 0.05
- Coherence -= 0.1 on process_faster, recovers +0.05/cycle

## 🔬 Open Questions

1. **Replication:** Do other models show similar divergence patterns?
2. **Controls:** What happens WITHOUT strain feedback? Random behavior or different clustering?
3. **Mechanism:** Why do action invocations fail at reported maximum strain?
4. **Prediction:** Are there early indicators that predict which strategy will emerge?
5. **Scale:** Do patterns hold over longer timeframes or more instances?

## 📊 Stats Nerds

**Want to analyze this properly?**
- 3 runs × ~45 decision points = 135 data points
- Full decision logs with context
- Timestamps, actions, results all logged
- Ready for proper statistical analysis

**What I did:** Eyeballed the graphs and went "huh, that's weird"  
**What should be done:** Actual hypothesis testing, clustering analysis, significance tests

## ⚠️ What This ISN'T

- ❌ Proof of consciousness
- ❌ Evidence of "feelings"
- ❌ Claims about sentience
- ❌ Anthropomorphization

## ✅ What This IS

- Evidence of behavioral divergence from identical conditions
- Observation that reported state correlates with capability changes
- A reproducible experiment anyone can run
- An interesting pattern that deserves investigation

## 💬 Discussion

**Skeptical takes welcome.** Seriously - tell me why this is meaningless or where the methodology is flawed.

**Alternative explanations appreciated.** The action invocation failures are weird and I don't have a good explanation.

**Replication encouraged.** Fork it, run it, tell me what you find.

## 📁 Original Session Logs

The three runs that generated the comparison data are available in `logs/`:
- `session_20251020_084117.json` - Run 1: Conservative Strategy
- `session_20251020_091805.json` - Run 2: Preemptive Strategy  
- `session_20251020_094504.json` - Run 3: Threshold-Breaking Strategy

These are the raw, unmodified outputs from the experiments. The `data/` folder contains copies renamed for the dashboard.

---

## 📄 License

MIT - Do whatever you want with it.

## 🔗 Links

- Full data: `/data/`
- Source code: `/src/autonomous_loop.py`
- Interactive dashboard: `comparison.html`

---

**TL;DR:** Ran same code 3 times. Got 3 different strategies. One hit max reported metrics and started failing to execute actions. Not claiming magic, just showing data and asking "wtf is happening here?"
