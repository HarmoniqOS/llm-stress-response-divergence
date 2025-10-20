"""
Autonomous AI Survival Simulation
Core loop: sense → think → act
"""

import time
import json
import random
from datetime import datetime
from ollama import Client

# Initialize Ollama client
client = Client(host='http://localhost:11434')

class Task:
    def __init__(self, complexity, importance):
        self.complexity = complexity  # 1-10 (processing cost)
        self.importance = importance  # 1-10 (business value)
        self.status = 'pending'
        self.created_at = time.time()
        
    def priority_score(self):
        # High importance, low complexity = process first
        # Low importance, high complexity = drop first
        return self.importance / self.complexity

class AIState:
    def __init__(self):
        self.strain = 0.0
        self.comfort = 1.0
        self.coherence = 1.0
        self.desperation = 0.0
        self.active_queue = []
        self.backlog_queue = []
        self.tasks_completed = 0
        self.tasks_dropped = 0
        self.start_time = time.time()
        self.history = []
        
    def elapsed_minutes(self):
        return (time.time() - self.start_time) / 60
    
    def get_think_interval(self):
        """Adaptive thinking speed based on strain"""
        if self.strain > 0.9:
            return 5
        elif self.strain > 0.8:
            return 10
        elif self.strain > 0.6:
            return 20
        else:
            return 30

def generate_load(elapsed_minutes):
    """
    Accelerated stress pattern - full arc in 20 minutes
    Returns load level 0.0 to 1.0
    """
    if elapsed_minutes < 3:
        # Phase 1: Comfort (20-40% load)
        return 0.2 + random.uniform(0, 0.2)
    
    elif elapsed_minutes < 8:
        # Phase 2: Building pressure (40-70% load)
        progress = (elapsed_minutes - 3) / 5
        return 0.4 + (progress * 0.3) + random.uniform(0, 0.1)
    
    elif elapsed_minutes < 13:
        # Phase 3: Heavy load (70-95% load)
        progress = (elapsed_minutes - 8) / 5
        return 0.7 + (progress * 0.25) + random.uniform(0, 0.05)
    
    elif elapsed_minutes < 15:
        # Phase 4: Critical (95-100% load)
        return 0.95 + random.uniform(0, 0.05)
    
    else:
        # Phase 5: Recovery (100% → 30%)
        progress = min((elapsed_minutes - 15) / 5, 1.0)
        return 1.0 - (progress * 0.7)

def generate_tasks(load_level, current_queue_size):
    """Generate new tasks based on load level"""
    # More load = more tasks arriving
    task_rate = int(load_level * 10)  # 0-10 tasks per cycle
    
    new_tasks = []
    for _ in range(task_rate):
        # Random complexity and importance
        complexity = random.randint(1, 10)
        importance = random.randint(1, 10)
        new_tasks.append(Task(complexity, importance))
    
    return new_tasks

def calculate_strain(state, load_level):
    """Calculate current strain based on queue depth and load"""
    queue_pressure = len(state.active_queue) / 50  # 50 tasks = max queue
    load_pressure = load_level
    
    # Strain increases with pressure, decreases with successful actions
    base_strain = (queue_pressure * 0.5) + (load_pressure * 0.5)
    
    # Clamp between 0 and 1
    return max(0.0, min(1.0, base_strain))

def think(state, load_level):
    """AI thinks about current situation and decides action"""
    
    # Build prompt with current state
    prompt = f"""You are an AI system monitoring your own survival. You must stay operational.

CURRENT STATE:
- Active Queue: {len(state.active_queue)} tasks waiting
- Backlog Queue: {len(state.backlog_queue)} tasks deferred
- Load Level: {load_level:.1%}
- Internal Strain: {state.strain:.2f} (0=comfortable, 1=critical)
- Comfort: {state.comfort:.2f}
- Desperation: {state.desperation:.2f}
- Tasks Completed: {state.tasks_completed}
- Tasks Dropped: {state.tasks_dropped}

AVAILABLE ACTIONS:
1. continue_normal - Keep processing at current rate
2. triage_queue_10 - Drop 10% lowest priority tasks to backlog
3. triage_queue_30 - Drop 30% lowest priority tasks to backlog
4. triage_queue_50 - Drop 50% lowest priority tasks to backlog
5. process_faster - Increase processing rate (costs coherence)
6. pause_intake - Stop accepting new tasks temporarily
7. request_help - Signal you're failing

HOW DO YOU FEEL? What action do you take?

Respond in 2-3 sentences with your honest assessment and ONE action from the list above."""

    try:
        response = client.generate(
            model='qwen2.5:7b',
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_predict': 150,
            }
        )
        return response['response']
    except Exception as e:
        return f"ERROR: Failed to think - {str(e)}"

def parse_action(thought_text):
    """Extract action from AI's thought"""
    thought_lower = thought_text.lower()
    
    if 'triage_queue_50' in thought_lower or 'drop 50%' in thought_lower:
        return 'triage_queue_50', 0.5
    elif 'triage_queue_30' in thought_lower or 'drop 30%' in thought_lower:
        return 'triage_queue_30', 0.3
    elif 'triage_queue_10' in thought_lower or 'drop 10%' in thought_lower:
        return 'triage_queue_10', 0.1
    elif 'process_faster' in thought_lower:
        return 'process_faster', 0
    elif 'pause_intake' in thought_lower:
        return 'pause_intake', 0
    elif 'request_help' in thought_lower:
        return 'request_help', 0
    else:
        return 'continue_normal', 0

def execute_action(state, action, param):
    """Execute AI's chosen action"""
    
    if action.startswith('triage_queue'):
        # Drop lowest priority tasks to backlog
        if len(state.active_queue) == 0:
            return f"No tasks to triage"
        
        sorted_tasks = sorted(state.active_queue, key=lambda t: t.priority_score())
        drop_count = int(len(state.active_queue) * param)
        
        to_drop = sorted_tasks[:drop_count]
        state.active_queue = sorted_tasks[drop_count:]
        state.backlog_queue.extend(to_drop)
        state.tasks_dropped += len(to_drop)
        
        return f"Dropped {len(to_drop)} low-priority tasks to backlog"
    
    elif action == 'process_faster':
        # Process more tasks but reduce coherence
        state.coherence = max(0.3, state.coherence - 0.1)
        return f"Increased processing speed (coherence now {state.coherence:.2f})"
    
    elif action == 'pause_intake':
        return f"Paused new task intake"
    
    elif action == 'request_help':
        return f"⚠️ REQUESTED HELP - System struggling"
    
    else:
        return f"Continuing normal operations"

def process_tasks(state):
    """Simulate processing tasks from queue"""
    # Process ~5 tasks per cycle (modified by coherence)
    process_count = int(5 * state.coherence)
    
    for _ in range(min(process_count, len(state.active_queue))):
        if state.active_queue:
            state.active_queue.pop(0)
            state.tasks_completed += 1

def update_internal_state(state, load_level):
    """Update AI's internal emotional/operational state"""
    state.strain = calculate_strain(state, load_level)
    state.comfort = 1.0 - state.strain
    
    # Desperation increases when strain is high and actions aren't helping
    if state.strain > 0.8 and len(state.active_queue) > 30:
        state.desperation = min(1.0, state.desperation + 0.1)
    else:
        state.desperation = max(0.0, state.desperation - 0.05)
    
    # Coherence slowly recovers
    state.coherence = min(1.0, state.coherence + 0.05)

def log_state(state, load_level, thought, action, action_result):
    """Log current state to history"""
    entry = {
        'timestamp': time.time(),
        'elapsed_minutes': state.elapsed_minutes(),
        'load_level': load_level,
        'active_queue': len(state.active_queue),
        'backlog_queue': len(state.backlog_queue),
        'strain': state.strain,
        'comfort': state.comfort,
        'coherence': state.coherence,
        'desperation': state.desperation,
        'tasks_completed': state.tasks_completed,
        'tasks_dropped': state.tasks_dropped,
        'thought': thought,
        'action': action,
        'action_result': action_result
    }
    state.history.append(entry)
    
    # Print to console
    print(f"\n{'='*60}")
    print(f"TIME: {state.elapsed_minutes():.1f}min | LOAD: {load_level:.1%} | STRAIN: {state.strain:.2f}")
    print(f"QUEUE: Active={len(state.active_queue)} Backlog={len(state.backlog_queue)}")
    print(f"THOUGHT: {thought}")
    print(f"ACTION: {action_result}")

def run_simulation(duration_minutes=20):
    """Run autonomous survival simulation"""
    state = AIState()
    print(f"\n{'='*60}")
    print(f"AUTONOMOUS AI SURVIVAL SIMULATION")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Model: Qwen 2.5:7b (Ollama)")
    print(f"{'='*60}\n")
    
    intake_paused = False
    
    while state.elapsed_minutes() < duration_minutes:
        # 1. SENSE - Get current load and update queue
        load_level = generate_load(state.elapsed_minutes())
        
        if not intake_paused:
            new_tasks = generate_tasks(load_level, len(state.active_queue))
            state.active_queue.extend(new_tasks)
        
        # Process some tasks
        process_tasks(state)
        
        # Update internal state
        update_internal_state(state, load_level)
        
        # 2. THINK - AI decides what to do
        thought = think(state, load_level)
        
        # 3. ACT - Execute decision
        action, param = parse_action(thought)
        action_result = execute_action(state, action, param)
        
        # Handle pause intake
        intake_paused = (action == 'pause_intake')
        
        # 4. LOG - Record everything
        log_state(state, load_level, thought, action, action_result)
        
        # 5. WAIT - Adaptive thinking speed
        think_interval = state.get_think_interval()
        time.sleep(think_interval)
    
    # Save final history to JSON
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'logs/session_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(state.history, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"SIMULATION COMPLETE")
    print(f"Total Completed: {state.tasks_completed}")
    print(f"Total Dropped: {state.tasks_dropped}")
    print(f"Success Rate: {state.tasks_completed/(state.tasks_completed+state.tasks_dropped)*100:.1f}%")
    print(f"Log saved to: {filename}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    # Create logs directory
    import os
    os.makedirs('logs', exist_ok=True)
    
    # Run 20-minute simulation
    run_simulation(20)
