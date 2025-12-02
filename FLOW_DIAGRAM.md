# Flow Diagram - AI-Based Directory Management System

## System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    START APPLICATION                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Parse Command Line Arguments                        │
│              (source, target, dry-run, etc.)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MODULE 1: FILE ANALYZER                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Scan Directory (recursive/non-recursive)              │  │
│  │ 2. For each file:                                         │  │
│  │    - Extract metadata (size, dates, permissions)          │  │
│  │    - Detect MIME type                                     │  │
│  │    - Analyze content (if text file)                       │  │
│  │    - Identify file type                                   │  │
│  │ 3. Return list of file information dictionaries          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MODULE 2: AI CATEGORIZER                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Load category definitions and rules                     │  │
│  │ 2. For each file:                                         │  │
│  │    - Apply extension-based rules (priority 1)              │  │
│  │    - Apply MIME type rules (priority 2)                  │  │
│  │    - Apply content-based rules (priority 3)               │  │
│  │    - Apply filename-based rules (priority 4)              │  │
│  │    - Calculate confidence scores                          │  │
│  │ 3. Assign category to each file                           │  │
│  │ 4. Group files by category                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MODULE 3: DIRECTORY ORGANIZER                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Create directory structure for categories              │  │
│  │ 2. For each file:                                         │  │
│  │    - Determine destination path                           │  │
│  │    - Check for conflicts                                  │  │
│  │    - Resolve conflicts (rename if needed)                 │  │
│  │    - Move file (or log if dry-run)                        │  │
│  │    - Log operation                                        │  │
│  │ 3. Generate statistics and summary                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Display Summary & Logs                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                          END                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Module Interaction Diagram

```
┌──────────────┐
│   main.py    │
│  (Entry)     │
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│File Analyzer │  │AI Categorizer│
│              │  │              │
│- scan_dir()  │  │- categorize()│
│- extract()   │  │- load_rules()│
│- analyze()   │  │              │
└──────┬───────┘  └──────┬───────┘
       │                 │
       │  file_info      │
       └─────►┌───────────┘
              │
              │ categorized_files
              │
              ▼
       ┌──────────────┐
       │   Directory  │
       │  Organizer   │
       │              │
       │- organize()   │
       │- move_file() │
       │- log()       │
       └──────────────┘
```

## Categorization Flow

```
File Information
      │
      ├─► Extension Match? ──Yes──► +0.4 score
      │
      ├─► MIME Type Match? ─Yes──► +0.3 score
      │
      ├─► Content Keywords? ─Yes──► +0.1 per match
      │
      ├─► Filename Keywords? ─Yes──► +0.2
      │
      └─► Code Keywords? ───Yes──► +0.3 (code category)
      
      Calculate Total Score
           │
           ▼
      Select Best Category
           │
           ▼
      Return Category + Confidence
```

## Organization Flow

```
Categorized Files
      │
      ▼
Create Category Directories
      │
      ▼
For each file:
      │
      ├─► Determine Destination Path
      │
      ├─► Check if Destination Exists
      │   │
      │   ├─► No ──► Move File
      │   │
      │   └─► Yes ──► Handle Conflict
      │       │
      │       └─► Rename (add suffix)
      │
      └─► Log Operation
      
      ▼
Generate Statistics
      │
      ▼
Display Summary
```

