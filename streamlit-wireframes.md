# Streamlit App Wireframes

## Goal
The app should behave like a working desk for the OECD written assessment, not like a generic file explorer.

## Structure

### 1. Home
Purpose: give direct entry points into the study flow.

Wireframe:

```text
+---------------------------------------------------------------+
| OECD Assessment Desk                                          |
| Short explanation of how to use the app during the exercise   |
+---------------------------------------------------------------+
| Recommended flow                                              |
| 1. Prep notes -> 2. Source research -> 3. Case -> 4. Tone     |
+---------------------------+-----------------------------------+
| Assessment prep           | Practice case                     |
| [Open library] [Search]   | [Open library] [Search]           |
+---------------------------+-----------------------------------+
| OECD tone of voice        | LLM research                      |
| [Open library] [Search]   | [Open library] [Search]           |
+---------------------------+-----------------------------------+
| OECD communications       | OECD AI                           |
| [Open library] [Search]   | [Open library] [Search]           |
+---------------------------+-----------------------------------+
```

### 2. Library
Purpose: browse one focus area at a time.

Wireframe:

```text
+-----------------------------+----------------------------------+
| Focus card                  | Preview panel                    |
| Section root | Up           | File path                        |
| Filter current folder       | File title                       |
|                             | Download                         |
| Folders                     | File content / PDF preview       |
| - folder A                  |                                  |
| - folder B                  |                                  |
| Files                       |                                  |
| - file 1                    |                                  |
| - file 2                    |                                  |
+-----------------------------+----------------------------------+
```

### 3. Search
Purpose: find evidence fast, then jump back to the library.

Wireframe:

```text
+---------------------------------------------------------------+
| Search                                                        |
| Scope: [Current section] [All sections]                       |
| Query box                                                     |
| [Run search]                                                  |
+---------------------------------------------------------------+
| Result card                                                   |
| path                                                          |
| title                                                         |
| snippet with highlighted terms                                |
| [Open in library]                                             |
+---------------------------------------------------------------+
```

## Sidebar

```text
+-----------------------+
| Navigator             |
| Page: Home/Library/...|
| Focus area selector   |
| Recent files          |
| - file A              |
| - file B              |
+-----------------------+
```

## Design rules
- One focus area at a time.
- No raw workspace root as the main landing experience.
- No startup indexing.
- Search only on submit.
- PDF preview disabled by default for speed.
- Markdown should read like documents, not raw source.
