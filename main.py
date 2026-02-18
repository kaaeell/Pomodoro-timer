import time
import json
import os
import sys
import datetime
import threading

# ── ANSI Colors ────────────────────────────────────────────────────────────────
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

def colored(text, *codes):
    return "".join(codes) + text + C.RESET

# ── File paths ─────────────────────────────────────────────────────────────────
SESSIONS_FILE = "pomodoro_sessions.json"
SETTINGS_FILE = "pomodoro_settings.json"

DEFAULT_SETTINGS = {
    "work_duration": 25,
    "short_break": 5,
    "long_break": 15,
    "sessions_until_long_break": 4,
    "daily_goal": 8,
    "auto_start_breaks": False,
    "sound_enabled": True,
}

# ── Persistence helpers ────────────────────────────────────────────────────────
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return default.copy() if isinstance(default, dict) else list(default)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_settings():
    s = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    # fill in any missing keys added in later versions
    for k, v in DEFAULT_SETTINGS.items():
        s.setdefault(k, v)
    return s

def save_settings(settings):
    save_json(SETTINGS_FILE, settings)

def load_sessions():
    return load_json(SESSIONS_FILE, [])

def save_sessions(sessions):
    save_json(SESSIONS_FILE, sessions)

# ── Terminal helpers ───────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def beep(n=1):
    """Terminal bell beep."""
    for _ in range(n):
        sys.stdout.write("\a")
        sys.stdout.flush()
        time.sleep(0.3)

def hr(char="─", width=50, color=C.DIM):
    print(colored(char * width, color))

def banner():
    clear()
    print()
    print(colored("  🍅  POMODORO TIMER", C.BOLD, C.RED))
    hr()

# ── Countdown with pause/skip ─────────────────────────────────────────────────
_paused = False
_skip   = False

def _listen_for_keys(settings):
    """Background thread: read single keypresses without Enter."""
    global _paused, _skip
    import tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ("p", "P"):
                _paused = not _paused
            elif ch in ("s", "S"):
                _skip = True
                break
            elif ch in ("q", "Q"):
                _skip = True
                break
    except Exception:
        pass
    finally:
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except Exception:
            pass

def _listen_windows():
    """Windows key listener using msvcrt."""
    global _paused, _skip
    import msvcrt
    while not _skip:
        if msvcrt.kbhit():
            ch = msvcrt.getwch().lower()
            if ch == "p":
                _paused = not _paused
            elif ch == "s":
                _skip = True
                break

def countdown(total_seconds, label, color, settings, task_name=""):
    global _paused, _skip
    _paused = False
    _skip   = False

    # Start key-listener thread
    use_raw = os.name != "nt"
    if use_raw:
        t = threading.Thread(target=_listen_for_keys, args=(settings,), daemon=True)
    else:
        t = threading.Thread(target=_listen_windows, daemon=True)
    t.start()

    remaining = total_seconds
    while remaining >= 0 and not _skip:
        if _paused:
            clear()
            print()
            print(colored("  ⏸  PAUSED", C.BOLD, C.YELLOW))
            hr()
            if task_name:
                print(colored(f"  Task: {task_name}", C.CYAN))
            print(colored(f"  {label}", C.BOLD))
            print()
            mm, ss = divmod(remaining, 60)
            print(colored(f"  ⏱  {mm:02d}:{ss:02d}", C.BOLD, color))
            print()
            print(colored("  [P] Resume   [S] Skip session", C.DIM))
            time.sleep(0.5)
            continue

        clear()
        print()
        print(colored("  🍅  POMODORO TIMER", C.BOLD, C.RED))
        hr()
        if task_name:
            print(colored(f"  Task: {task_name}", C.CYAN))
        print(colored(f"  {label}", C.BOLD))

        # Progress bar
        pct = 1 - remaining / total_seconds if total_seconds > 0 else 1
        filled = int(pct * 40)
        bar = "█" * filled + "░" * (40 - filled)
        print(colored(f"\n  [{bar}] {int(pct*100):3d}%\n", color))

        mm, ss = divmod(remaining, 60)
        print(colored(f"  ⏱  {mm:02d}:{ss:02d}", C.BOLD, color))
        print()
        print(colored("  [P] Pause   [S] Skip session", C.DIM))
        time.sleep(1)
        remaining -= 1

    skipped = _skip
    # Restore terminal if raw mode was used
    if use_raw and os.name != "nt":
        os.system("stty sane 2>/dev/null")

    return not skipped  # True = completed, False = skipped

# ── Stats helpers ─────────────────────────────────────────────────────────────
def today_str():
    return datetime.date.today().isoformat()

def sessions_today(sessions):
    td = today_str()
    return [s for s in sessions if s.get("date") == td and s.get("type", "").startswith("Work")]

def sessions_this_week(sessions):
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    result = []
    for s in sessions:
        try:
            d = datetime.date.fromisoformat(s.get("date", ""))
            if start <= d <= today and s.get("type", "").startswith("Work"):
                result.append(s)
        except ValueError:
            pass
    return result

# ── Core session runner ───────────────────────────────────────────────────────
def run_pomodoro(settings):
    sessions = load_sessions()
    session_count = len(sessions_today(sessions))
    pomodoro_num  = 0          # resets each new run; session_count tracks lifetime today

    task_name = input(colored("\n  📝 What are you working on? (Enter to skip): ", C.CYAN)).strip()

    print(colored("\n  Starting your Pomodoro session! 🚀\n", C.GREEN))
    time.sleep(1)

    while True:
        pomodoro_num  += 1
        session_count += 1

        # ── Work ──────────────────────────────────────────────────────────────
        label = colored(f"🎯 Work Session #{session_count}", C.BOLD)
        work_secs = settings["work_duration"] * 60
        completed = countdown(work_secs, label, C.GREEN, settings, task_name)

        if completed:
            sessions.append({
                "type": f"Work Session #{session_count}",
                "duration": settings["work_duration"],
                "timestamp": datetime.datetime.now().isoformat(),
                "date": today_str(),
                "task": task_name or None,
            })
            save_sessions(sessions)

            if settings.get("sound_enabled"):
                beep(2)

            # Daily goal check
            daily = [s for s in sessions if s.get("date") == today_str() and s.get("type","").startswith("Work")]
            goal   = settings.get("daily_goal", 8)
            if len(daily) == goal:
                clear()
                print()
                print(colored(f"  🎉  DAILY GOAL REACHED! {goal} sessions done today!", C.BOLD, C.YELLOW))
                hr()
                input(colored("  Press Enter to continue...", C.DIM))

        else:
            print(colored("\n  ⏭  Session skipped.\n", C.YELLOW))
            time.sleep(1)

        # ── Break decision ────────────────────────────────────────────────────
        is_long = (pomodoro_num % settings["sessions_until_long_break"] == 0)
        break_mins = settings["long_break"] if is_long else settings["short_break"]
        break_type = "Long Break 🛋️" if is_long else "Short Break ☕"
        break_color = C.YELLOW if is_long else C.CYAN

        clear()
        print()
        print(colored(f"  ✅  Nice work! Time for a {break_type}", C.BOLD))
        hr()

        today_done = len([s for s in sessions if s.get("date") == today_str() and s.get("type","").startswith("Work")])
        goal       = settings.get("daily_goal", 8)
        print(colored(f"  Today: {today_done}/{goal} sessions", C.DIM))
        print()

        if settings.get("auto_start_breaks"):
            print(colored(f"  Break starting in 3 seconds…\n", C.DIM))
            time.sleep(3)
            start_break = True
        else:
            ans = input(colored(f"  Start {break_type}? [Y/n]: ", C.CYAN)).strip().lower()
            start_break = ans in ("", "y", "yes")

        if start_break:
            label = colored(f"⏳ {break_type}", C.BOLD)
            countdown(break_mins * 60, label, break_color, settings, "")
            if settings.get("sound_enabled"):
                beep(1)
        else:
            print(colored("  Break skipped.", C.DIM))
            time.sleep(0.5)

        # ── Continue? ─────────────────────────────────────────────────────────
        clear()
        print()
        print(colored("  Ready for another round? 🍅", C.BOLD))
        hr()
        today_done = len([s for s in sessions if s.get("date") == today_str() and s.get("type","").startswith("Work")])
        print(colored(f"  Today: {today_done}/{goal} sessions\n", C.DIM))
        ans = input(colored("  [Enter] Keep going   [q] Back to menu: ", C.CYAN)).strip().lower()
        if ans == "q":
            break

# ── Stats display ──────────────────────────────────────────────────────────────
def show_stats(settings):
    banner()
    sessions = load_sessions()

    today_sessions = sessions_today(sessions)
    week_sessions  = sessions_this_week(sessions)
    total_work     = len([s for s in sessions if s.get("type","").startswith("Work")])
    goal           = settings.get("daily_goal", 8)

    print(colored("  📊  YOUR STATS", C.BOLD, C.CYAN))
    print()

    # Today
    done_today = len(today_sessions)
    pct = min(done_today / goal, 1.0) if goal else 0
    filled = int(pct * 30)
    bar = "█" * filled + "░" * (30 - filled)
    goal_color = C.GREEN if done_today >= goal else C.YELLOW
    print(colored(f"  Today          [{bar}] {done_today}/{goal}", goal_color, C.BOLD))

    # This week
    print(colored(f"  This week      {len(week_sessions)} sessions ({len(week_sessions)*25} min of focus)", C.WHITE))
    print(colored(f"  All time       {total_work} sessions", C.WHITE))

    # Minutes today
    mins_today = sum(s.get("duration", 0) for s in today_sessions)
    print(colored(f"  Focus time     {mins_today} min today / {len(week_sessions)*25} min this week", C.DIM))

    # Tasks today
    tasks = list({s.get("task") for s in today_sessions if s.get("task")})
    if tasks:
        print()
        print(colored("  Tasks today:", C.BOLD))
        for task in tasks:
            task_sessions = [s for s in today_sessions if s.get("task") == task]
            print(colored(f"    • {task}  ({len(task_sessions)} sessions)", C.CYAN))

    # Recent sessions
    recent = [s for s in sessions[-10:] if s.get("type","").startswith("Work")]
    if recent:
        print()
        print(colored("  Recent sessions:", C.BOLD))
        for s in reversed(recent[-5:]):
            ts  = s.get("timestamp","")[:16].replace("T", " ")
            tp  = s.get("type","")
            tsk = f"  [{s['task']}]" if s.get("task") else ""
            print(colored(f"    {ts}  {tp}{tsk}", C.DIM))

    print()
    hr()
    input(colored("  Press Enter to go back…", C.DIM))

# ── Settings menu ─────────────────────────────────────────────────────────────
def show_settings(settings):
    while True:
        banner()
        print(colored("  ⚙️   SETTINGS", C.BOLD, C.YELLOW))
        print()
        options = [
            ("Work duration",             f"{settings['work_duration']} min"),
            ("Short break",               f"{settings['short_break']} min"),
            ("Long break",                f"{settings['long_break']} min"),
            ("Sessions until long break", str(settings["sessions_until_long_break"])),
            ("Daily goal",                f"{settings['daily_goal']} sessions"),
            ("Auto-start breaks",         "On" if settings["auto_start_breaks"] else "Off"),
            ("Sound notifications",       "On" if settings["sound_enabled"] else "Off"),
        ]
        keys = [
            "work_duration", "short_break", "long_break",
            "sessions_until_long_break", "daily_goal",
            "auto_start_breaks", "sound_enabled",
        ]
        for i, (name, val) in enumerate(options, 1):
            print(colored(f"  [{i}] {name:<30} {val}", C.WHITE))

        print(colored("\n  [r] Reset to defaults", C.DIM))
        print(colored("  [0] Back\n", C.DIM))
        hr()

        choice = input(colored("  Pick a setting to change: ", C.CYAN)).strip()
        if choice == "0":
            break
        elif choice == "r":
            settings.update(DEFAULT_SETTINGS)
            save_settings(settings)
            print(colored("  Settings reset!\n", C.GREEN))
            time.sleep(1)
            continue

        try:
            idx = int(choice) - 1
            key = keys[idx]
            name = options[idx][0]
        except (ValueError, IndexError):
            continue

        if key in ("auto_start_breaks", "sound_enabled"):
            settings[key] = not settings[key]
            save_settings(settings)
        else:
            try:
                val = int(input(colored(f"  New value for {name}: ", C.CYAN)).strip())
                if val > 0:
                    settings[key] = val
                    save_settings(settings)
                    print(colored("  ✅ Saved!\n", C.GREEN))
                    time.sleep(0.8)
            except ValueError:
                print(colored("  ❌  Invalid input.\n", C.RED))
                time.sleep(0.8)

# ── Clear history ─────────────────────────────────────────────────────────────
def clear_history():
    banner()
    print(colored("  ⚠️   CLEAR HISTORY", C.BOLD, C.RED))
    print()
    print(colored("  This will delete ALL saved sessions permanently.", C.YELLOW))
    ans = input(colored("  Type 'yes' to confirm: ", C.CYAN)).strip().lower()
    if ans == "yes":
        save_sessions([])
        print(colored("  ✅  History cleared.\n", C.GREEN))
    else:
        print(colored("  Cancelled.\n", C.DIM))
    time.sleep(1)

# ── Main menu ─────────────────────────────────────────────────────────────────
def main():
    settings = load_settings()

    while True:
        banner()
        sessions = load_sessions()
        today_done = len(sessions_today(sessions))
        goal       = settings.get("daily_goal", 8)

        # Quick status bar
        pct = min(today_done / goal, 1.0) if goal else 0
        bar_w = 30
        filled = int(pct * bar_w)
        bar = "█" * filled + "░" * (bar_w - filled)
        bar_color = C.GREEN if today_done >= goal else C.CYAN
        print(colored(f"  Today  [{bar}]  {today_done}/{goal} sessions", bar_color))
        print()
        hr()
        print()

        print(colored("  [1]  🚀 Start Pomodoro", C.WHITE))
        print(colored("  [2]  📊 Stats", C.WHITE))
        print(colored("  [3]  ⚙️  Settings", C.WHITE))
        print(colored("  [4]  🗑️  Clear history", C.WHITE))
        print(colored("  [0]  👋 Exit", C.WHITE))
        print()
        hr()

        choice = input(colored("  Choose: ", C.CYAN)).strip()

        if choice == "1":
            run_pomodoro(settings)
        elif choice == "2":
            show_stats(settings)
        elif choice == "3":
            show_settings(settings)
        elif choice == "4":
            clear_history()
        elif choice == "0":
            clear()
            print(colored("\n  Goodbye! Keep crushing it. 🍅\n", C.BOLD, C.RED))
            break

if __name__ == "__main__":
    main()
