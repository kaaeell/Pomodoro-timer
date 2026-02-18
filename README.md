# 🍅 Pomodoro Timer

Your new best friend for getting stuff done! This is a simple, friendly command-line Pomodoro timer that helps you focus, take breaks, and track your progress.

## Features

* **🎯 Pomodoro Sessions** - Work sessions with built-in breaks
* **⚙️ Easy Tweaking** - Change your timings to fit YOUR rhythm
* **📊 See Your Progress** - Watch your wins add up
* **☕ Smart Breaks** - Short breaks and longer breaks when you need them
* **⏱️ Big Timer** - Large countdown you can actually read
* **📝 Remember Everything** - Your sessions are saved so you can look back
* **💾 Zero Setup** - Just Python, nothing else to install

### ✨ New in this version

* **🎨 Color UI** - ANSI-colored interface with a progress bar and big clock — way easier to read at a glance
* **⏸️ Pause / Resume** - Press `P` mid-session to pause and `P` again to resume (no lost time)
* **⏭️ Skip session** - Press `S` to skip the current work block or break and keep your flow
* **📝 Task labels** - Name what you're working on before each run; sessions are saved with the task name
* **🏁 Daily goal** - Set a target number of sessions per day and watch a progress bar fill up
* **🔔 Sound notifications** - Terminal bell rings when a session or break ends (toggle in settings)
* **🚀 Auto-start breaks** - Enable in settings and breaks kick off automatically (no prompts)
* **🗑️ Clear history** - New menu option to wipe all saved sessions with a confirmation prompt
* **📅 Weekly stats** - Stats screen now shows this week's total sessions and focus minutes
* **🏷️ Task breakdown in stats** - See which tasks you worked on today and how many sessions each got
* **🔄 Reset to defaults** - One-key reset in the settings menu

## Requirements

* Python 3.x

## Installation

Super easy! Just grab Python and run:

```
python main.py
```

That's it. No pip install, no dependencies, nothing complicated.

## Usage

Run it:

```
python main.py
```

### What You Can Do

1. **🚀 Start a Pomodoro** - Work for 25 min, break for 5, repeat. It's that simple.
2. **📊 Check Your Stats** - How much have you crushed today (and this week)? Let's see!
3. **🎨 Change Settings** - Like 20 min work sessions instead? You got it.
4. **🗑️ Clear History** - Start fresh whenever you want.
5. **👋 Exit** - When you're done being awesome.

### Keyboard shortcuts during a session

| Key | Action |
|-----|--------|
| `P` | Pause / Resume |
| `S` | Skip current session or break |

> **Note:** Live keypress detection works automatically on macOS/Linux.  
> On Windows it uses `msvcrt` (also built-in, no install needed).

## The Pomodoro Magic

Here's how it works (and why it's amazing):

1. **Focus** (25 min): Work on ONE thing, no distractions
2. **Rest** (5 min): Stretch, grab water, breathe
3. **Repeat**: Do this 4 times
4. **Long Break** (15 min): You earned this one! Recharge properly.
5. **Keep Going** or call it a day

## Settings

All settings live in `pomodoro_settings.json` and can be changed from the in-app settings menu:

| Setting | Default | Description |
|---|---|---|
| `work_duration` | 25 min | Length of each work session |
| `short_break` | 5 min | Short break after each session |
| `long_break` | 15 min | Long break after every N sessions |
| `sessions_until_long_break` | 4 | How many sessions before a long break |
| `daily_goal` | 8 sessions | Target sessions per day |
| `auto_start_breaks` | Off | Skip the "start break?" prompt |
| `sound_enabled` | On | Terminal bell at end of each block |

## What Gets Saved?

We remember your sessions and settings so you can look back.

### Your Sessions (`pomodoro_sessions.json`)

Everything you complete gets logged, including the optional task name:

```json
[
  {
    "type": "Work Session #1",
    "duration": 25,
    "timestamp": "2026-02-09T14:30:45.123456",
    "date": "2026-02-09",
    "task": "Write unit tests"
  }
]
```

### Your Settings (`pomodoro_settings.json`)

```json
{
  "work_duration": 25,
  "short_break": 5,
  "long_break": 15,
  "sessions_until_long_break": 4,
  "daily_goal": 8,
  "auto_start_breaks": false,
  "sound_enabled": true
}
```

## Pro Tips

💡 **Hide Your Phone** - It's just 25 minutes. You can do it.

💡 **Name your sessions** - Typing what you're working on makes it real and keeps you accountable.

💡 **Set a daily goal** - Even just 4 sessions = 2 hours of deep work. That's huge.

💡 **Use Pause, not distraction** - Got interrupted? Hit `P` instead of alt-tabbing away.

💡 **Check Your Wins** - Looking at your stats is SUPER motivating.

💡 **Adjust to You** - If 25 min feels long, try 20. If it feels short, try 30.

💡 **Use Your Breaks** - Actually rest! Walk, drink water, don't check Slack.

## Why This Works

✅ Focus gets easier when you have an end point
✅ Breaks keep you fresh (not burned out)
✅ Seeing your progress keeps you going
✅ It feels good to say "I did 5 sessions today!"
✅ Your brain works better in bursts

---

**Now stop reading and start working! You've got this. 🚀**
