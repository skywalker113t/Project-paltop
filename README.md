# PROJECT PALTOP

**A tiny desktop companion that makes productivity feel a little more alive.**

PALTOP is a lightweight desktop-pet concept: a character stays on your desktop, reacts when you interact with it, and earns cosmetic unlocks as you complete useful tasks.

## Current prototype

This starter version is intentionally dependency-free beyond Python's built-in Tkinter:

- A small, draggable desktop companion window
- Click the pet to receive a rotating reaction
- Add and complete tasks
- Earn PAL points for completed tasks
- Unlock a few free character looks with earned points
- A simple focus timer
- Saves points, tasks, and the selected character locally in `paltop_save.json`

This is an early prototype, not a finished commercial app. The current UI is deliberately simple so the core loop can be tested before investing in artwork or a larger framework.

## Run it on Windows

1. Install Python 3.10 or newer from [python.org](https://www.python.org/).
2. During installation, enable **Add Python to PATH**.
3. Open this folder in VS Code.
4. Run:

   ```bash
   python src/main.py
   ```

Tkinter is included with most standard Windows Python installations. If Python reports that Tkinter is missing, rerun the Python installer and enable the Tcl/Tk component.

## Suggested Git setup

From this folder:

```bash
git init
git add .
git commit -m "Initial PROJECT PALTOP prototype"
```

Then create an empty repository named `PROJECT PALTOP` on your preferred Git hosting service and add its remote URL:

```bash
git remote add origin YOUR_REPOSITORY_URL
git branch -M main
git push -u origin main
```

## Product direction

### Core experience
- Desktop companion with idle, happy, focused, and sleepy states
- Customizable characters, colors, accessories, and desk themes
- Tasks, focus sessions, gentle reminders, and streaks
- Earnable cosmetics that never require payment

### Fair unlock system
- Free characters and cosmetics remain available through play and productivity
- Optional paid cosmetic packs can be considered later, with clear fixed prices
- No loot boxes, random paid rewards, pay-to-win boosts, or pressure-based streak mechanics
- Any purchases should use a trusted payment provider and require appropriate account-holder approval

### Privacy principles
- Tasks and progress stay local by default
- No screenshots, keystroke logging, or invasive activity tracking
- Any future cloud sync or analytics must be opt-in and clearly explained

## Roadmap

- [x] Initial desktop companion prototype
- [x] Task list and earned points
- [x] Basic character selection
- [x] Local save file
- [ ] Character animation and custom artwork
- [ ] Settings panel and theme editor
- [ ] Optional notifications
- [ ] Portable Windows build
- [ ] Accessibility and keyboard navigation
- [ ] Plugin-style character packs

## Project structure

```text
PROJECT_PALTOP/
├── assets/
├── src/
│   └── main.py
├── .gitignore
├── LICENSE
└── README.md
```

## License

MIT. See `LICENSE`.
