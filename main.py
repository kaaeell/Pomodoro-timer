import time
import os
from datetime import datetime, timedelta
import json


SESSIONS_FILE = "pomodoro_sessions.json"
SETTINGS_FILE = "pomodoro_settings.json"


# Default Pomodoro settings (in minutes)
DEFAULT_SETTINGS = {
    "work_duration": 25,
    "short_break": 5,
    "long_break": 15,
    "sessions_until_long_break": 4
}


def load_settings():
    """Say hi to your saved settings, or use the defaults if it's your first time."""
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Remember your awesome settings for next time."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=2)


def load_sessions():
    """Grab all your past Pomodoro victories from memory."""
    try:
        with open(SESSIONS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_sessions(sessions):
    """Save Pomodoro sessions to file."""
    with open(SESSIONS_FILE, "w") as file:
        json.dump(sessions, file, indent=2)


def add_session(duration, session_type):
    """Add a completed session to history."""
    sessions = load_sessions()
    session = {
        "type": session_type,
        "duration": duration,
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    sessions.append(session)
    save_sessions(sessions)


def format_time(seconds):
    """Format seconds to MM:SS format."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def display_timer(remaining_seconds, session_name):
    """Display the countdown timer."""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n" + "=" * 50)
    print(f"       {session_name}")
    print("=" * 50)
    print(f"\n    {format_time(remaining_seconds)}\n")
    print("=" * 50)


def run_timer(duration_minutes, session_name):
    """Start your timer and watch it count down. You've got this!"""
    total_seconds = duration_minutes * 60
    remaining_seconds = total_seconds
    start_time = time.time()
    paused_time = 0
    
    print(f"\n⏱️  Let's go! {session_name} for {duration_minutes} minutes")
    print("(Hit Ctrl+C if you need to stop)\n")
    time.sleep(2)
    
    try:
        while remaining_seconds > 0:
            display_timer(remaining_seconds, session_name)
            print("Controls: [Space] to pause/resume, [Q] to quit")
            
            # Wait 1 second
            time.sleep(1)
            
            # Update remaining time
            elapsed = time.time() - start_time - paused_time
            remaining_seconds = total_seconds - int(elapsed)
            
    except KeyboardInterrupt:
        user_input = input("\n\nOops! Want to save what you did? (y/n): ").strip().lower()
        if user_input == "y":
            actual_duration = total_seconds - remaining_seconds
            add_session(actual_duration // 60, session_name)
        return
    
    # Woohoo! Timer's done!
    print("\n" + "=" * 50)
    print(f"     🎉 {session_name} Done! Great job!")
    print("=" * 50)
    add_session(duration_minutes, session_name)
    time.sleep(2)


def run_pomodoro_session():
    """Let's rock a Pomodoro session! Work, break, work, break - you know the deal."""
    settings = load_settings()
    work_duration = settings["work_duration"]
    short_break = settings["short_break"]
    long_break = settings["long_break"]
    sessions_until_long = settings["sessions_until_long_break"]
    
    completed_sessions = 0
    
    print("\n🍅 Alright, let's crush some Pomodoros!")
    input("Ready? Hit Enter to begin...")
    
    while True:
        # Work session
        completed_sessions += 1
        run_timer(work_duration, f"Work Session #{completed_sessions}")
        
        # Check if it's time for a long break
        if completed_sessions % sessions_until_long == 0:
            print(f"\n🎉 Woah! You just crushed {completed_sessions} sessions in a row!")
            print("Time for a longer break - you earned it!")
            run_timer(long_break, "Long Break")
        else:
            print(f"\n☕ Fantastic work! Quick break, then back at it.")
            run_timer(short_break, "Short Break")
        
        # Time to decide: keep going or call it a day?
        print("\n" + "=" * 50)
        choice = input("Another round? (yes or just hit enter / no to quit): ").strip().lower()
        if choice in ["no", "n", "quit"]:
            print(f"\n🌟 Amazing! You crushed {completed_sessions} work sessions today.")
            print("You should be proud of yourself! 💪\n")
            break


def customize_settings():
    """Tweak your settings to feel just right for you."""
    settings = load_settings()
    
    print("\n🎭 Let's customize your Pomodoro!")
    print(f"Right now you've got:")
    print(f"  1. Work Time: {settings['work_duration']} minutes")
    print(f"  2. Quick Break: {settings['short_break']} minutes")
    print(f"  3. Long Break: {settings['long_break']} minutes")
    print(f"  4. Sessions before long break: {settings['sessions_until_long_break']}")
    print(f"  5. Nevermind, back to menu\n")
    
    choice = input("What do you want to change? (1-5): ").strip()
    
    try:
        if choice == "1":
            settings["work_duration"] = int(input("How many minutes to work? "))
        elif choice == "2":
            settings["short_break"] = int(input("How many minutes for quick breaks? "))
        elif choice == "3":
            settings["long_break"] = int(input("How many minutes for long breaks? "))
        elif choice == "4":
            settings["sessions_until_long_break"] = int(input("How many work sessions before long break? "))
        elif choice == "5":
            return
        else:
            print("Hmm, that's not an option. Try again.\n")
            return
        
        save_settings(settings)
        print("✅ Got it! Your settings are saved.\n")
    except ValueError:
        print("Oops, I need a number. Try again.\n")


def view_statistics():
    """Let's check out how awesome you've been!"""
    sessions = load_sessions()
    
    if not sessions:
        print("\nNo sessions yet - but you can start right now! 💪\n")
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_sessions = [s for s in sessions if s["date"] == today]
    
    print("\n📋 Your Productivity Wins:")
    print(f"  Total sessions ever: {len(sessions)} 🎉")
    print(f"  Today's sessions: {len(today_sessions)}")
    
    # Calculate total focus time
    total_minutes = sum(s["duration"] for s in sessions)
    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    print(f"  Your total focus time: {total_hours} hours {remaining_minutes} minutes 🔥")
    
    # Today's specific stats
    if today_sessions:
        today_minutes = sum(s["duration"] for s in today_sessions)
        print(f"  Focus time today: {today_minutes} minutes ⭐")
    
    print()





def main():
    """Main function to run the Pomodoro Timer."""
    print("\n" + "=" * 50)
    print("     🍅 POMODORO TIMER 🍅")
    print("=" * 50)
    print("\nHey! Ready to get focused and productive?")
    print("Let's do this with some awesome Pomodoro sessions.\n")
    
    while True:
        print("=" * 50)
        print("What's next?")
        print("=" * 50)
        print("1. 🚀 Start a Pomodoro Session")
        print("2. 🎭 Tweak my settings")
        print("3. 📋 Check my stats")
        print("4. 🚻 Exit")
        choice = input("\nYour choice (1-4): ").strip()
        
        if choice == "1":
            run_pomodoro_session()
        elif choice == "2":
            customize_settings()
        elif choice == "3":
            view_statistics()
        elif choice == "4":
            print("\n🍅 Thanks for crushing it! Keep up the great work! 🙋\n")
            break
        else:
            print("Hmm, try 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()
