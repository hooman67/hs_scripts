## 🐍 Python Scheduler (Recommended for Development)

**File:** `pita_daily_scheduler.py`

A Python-based scheduler using the `schedule` library. Best for development environments and when you need programmatic control.

### Features
- Easy to configure and modify
- Built-in logging
- Configuration file support
- Test mode for immediate execution
- Cross-platform compatibility

### Installation
```bash
# Install required Python package
pip install schedule

# Or if using the project's virtual environment
cd /mnt/localssd/colligo
source .venvs/colligo/bin/activate  # or your venv path
pip install schedule
```

### Usage

#### Command Line
```bash
# Run a command daily at 9:00 AM
python pita_daily_scheduler.py --command "echo 'Hello World!'" --time "09:00"

# Run a Python script daily at 2:30 PM
python pita_daily_scheduler.py --command "python3 /path/to/script.py" --time "14:30"

# Test the command once (don't schedule)
python pita_daily_scheduler.py --command "echo 'Test run'" --time "09:00" --test

# Use a configuration file
python pita_daily_scheduler.py --config pita_daily_scheduler_config.json

# If a configuration file contains a list of entries, run them all in individual tmux sessions
python pita_daily_scheduler.py --config pita_daily_scheduler_multiple_config.json --tmux
```

#### Configuration File
Create a JSON configuration file (see `pita_daily_scheduler_config.json` for example):
```json
{
  "command": "echo 'Hello from daily scheduler!' && date",
  "time": "09:00",
  "log_file": "pita_daily_scheduler.log",
  "working_dir": "/mnt/localssd/colligo"
}
```

#### Configuration File With Multiple Entries
Create a JSON configuration file (see `pita_daily_scheduler_multiple_config.json` for example):
```json
[
  {
    "command": "echo 'Hello from daily scheduler!' && date",
    "time": "09:00",
    "log_file": "pita_daily_scheduler.log",
    "working_dir": "/mnt/localssd/colligo"
  },
  {
    "command": "echo 'Hello from the second daily scheduler!' && date",
    "time": "21:00",
    "log_file": "pita_daily_scheduler.log",
    "working_dir": "/mnt/localssd/colligo"
  }
]
```

#### Running in Background
```bash
# Use --tmux argument
python pita_daily_scheduler.py --config pita_daily_scheduler_config.json --tmux

# Or run in background with nohup
nohup python pita_daily_scheduler.py --config pita_daily_scheduler_config.json > scheduler.out 2>&1 &

# Or use screen persistent sessions
screen -S daily_scheduler
python pita_daily_scheduler.py --config pita_daily_scheduler_config.json
# Press Ctrl+A, D to detach
```