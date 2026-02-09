# 🍅 Pomodoro Timer

Your new best friend for getting stuff done! This is a simple, friendly command-line Pomodoro timer that helps you focus, take breaks, and track your progress.

## Features

- **🎯 Pomodoro Sessions** - Work sessions with built-in breaks
- **⚙️ Easy Tweaking** - Change your timings to fit YOUR rhythm
- **📊 See Your Progress** - Watch your wins add up
- **☕ Smart Breaks** - Short breaks and longer breaks when you need them
- **⏱️ Big Timer** - Large countdown you can actually read
- **📝 Remember Everything** - Your sessions are saved so you can look back
- **💾 Zero Setup** - Just Python, nothing else to install

## Requirements

- Python 3.x

## Installation

Super easy! Just grab Python and run:

```bash
python main.py
```

That's it. No pip install, no dependencies, nothing complicated.

## Usage

Run it:
```bash
python main.py
```

### What You Can Do

1. **🚀 Start a Pomodoro** - Work for 25 min, break for 5, repeat. It's that simple.
2. **🎨 Change Settings** - Like 20 min work sessions instead? You got it.
3. **📈 Check Your Stats** - How much have you crushed today? Let's see!
4. **👋 Exit** - When you're done being awesome

## The Pomodoro Magic

Here's how it works (and why it's amazing):

1. **Focus** (25 min): Work on ONE thing, no distractions
2. **Rest** (5 min): Stretch, grab water, breathe
3. **Repeat**: Do this 4 times
4. **Long Break** (15 min): You earned this one! Recharge properly.
5. **Keep Going** or call it a day

## What Gets Saved?

We remember your sessions and settings so you can look back:

### Your Sessions (pomodoro_sessions.json)
Everything you complete gets logged:
```json
[
  {
    "type": "Work Session #1",
    "duration": 25,
    "timestamp": "2026-02-09T14:30:45.123456",
    "date": "2026-02-09"
  }
]
```

### Your Settings (pomodoro_settings.json)
Your custom times stay the same:
```json
{
  "work_duration": 25,
  "short_break": 5,
  "long_break": 15,
  "sessions_until_long_break": 4
}
```

## Pro Tips

💡 **Hide Your Phone** - It's just 25 minutes. You can do it.

💡 **One Task Per Pomodoro** - Don't try to do everything at once.

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
