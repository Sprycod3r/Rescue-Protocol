# Rescue Protocol

A text-based tactical rescue game written in Python for SNHU IT 140 — Intro to Scripting.

## Story

You're embedded behind enemy lines with no resources and no comms. A local informant spotted soldiers taking a captured teammate into a bombed-out district. Navigate the area, scavenge six mission-critical items, and extract your teammate from the Enemy Commander's Post before it's too late.

## How to Play

Requires Python 3. No external libraries needed.

```
python TextBasedGame.py
```

Navigate using cardinal directions and collect items to progress:

- `north` / `south` / `east` / `west` — or `go north`, `head east`, `n`, etc.
- `get [item]` / `grab [item]` / `pick up [item]` — pick up items in your current room
- `inventory` — check what you're carrying
- `help` — show available commands
- `quit` — exit the game

## Objective

Collect all six items scattered across the district before confronting the enemy commander. Missing gear has consequences — some failures are immediate, others play out in the ending.

## What This Demonstrates

- Modular function design (game loop, input normalization, movement, item handling)
- Input normalization handling multiple natural-language phrasings for commands
- Dictionary-driven game map and item data
- Conditional game state logic with multiple win/fail outcomes
- Clean separation of data and logic

## Context

Built as a course project for SNHU IT 140 — Intro to Scripting. The game design, narrative, and code are entirely my own work.
