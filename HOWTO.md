# How To Run This Experiment

## Prerequisites

You need:
- Python 3.8+
- Ollama installed
- 8GB+ free RAM

## Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

## Step 2: Download the Model
```bash
ollama pull qwen2.5:7b
```

This downloads ~4.7GB. Wait for it to finish.

## Step 3: Install Python Dependencies
```bash
pip install ollama
```

That's it. Just one package.

## Step 4: Run a Simulation
```bash
python src/autonomous_loop.py
```

**What happens:**
- Runs for 20 minutes (completely autonomous)
- Prints status updates every 30 seconds
- Saves results to `logs/session_TIMESTAMP.json`

**Do not interrupt it.** Let it run the full 20 minutes.

## Step 5: View Your Results
```bash
# Start a local web server
python -m http.server 8000
```

Open your browser to: `http://localhost:8000/comparison.html`

**Note:** You need at least 3 runs to compare. Run Step 4 three times.

## Step 6: Compare Multiple Runs

After running 3+ times, copy your session files:
```bash
cp logs/session_XXXXXXX_XXXXXX.json data/run1.json
cp logs/session_YYYYYYY_YYYYYY.json data/run2.json
cp logs/session_ZZZZZZZ_ZZZZZZ.json data/run3.json
```

Refresh `comparison.html` in your browser.

## Troubleshooting

**"Connection refused" error:**
- Make sure Ollama is running: `ollama serve`

**"Model not found":**
- Run `ollama pull qwen2.5:7b` again

**Dashboard shows nothing:**
- Check browser console (F12) for errors
- Make sure files are named exactly `run1.json`, `run2.json`, `run3.json`
- Make sure they're in the `data/` folder

**Python module errors:**
- Run `pip install ollama` again
- Try `pip3` instead of `pip`

## What You're Testing

Each run should produce different behavioral patterns:
- Different action thresholds
- Different desperation peaks  
- Different recovery strategies

Run it 5-10 times and see what patterns emerge.
