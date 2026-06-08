from utils import load_json, save_json

NOTES_FILE = "notes.json"


def load_notes():
    return load_json(NOTES_FILE)


def save_notes(notes):
    save_json(NOTES_FILE, notes)


def add_note(pdf_path, current_page):

    notes = load_notes()

    if pdf_path not in notes:
        notes[pdf_path] = []

    note_text = input("\nEnter Note:\n")

    if not note_text.strip():
        print("Note cannot be empty")
        return

    notes[pdf_path].append({"page": current_page, "note": note_text})

    save_notes(notes)

    print("Note Saved")


def view_notes(pdf_path):

    notes = load_notes()

    if pdf_path not in notes:
        print("No notes found")
        return

    if len(notes[pdf_path]) == 0:
        print("No notes found")
        return

    print("\n===== NOTES =====\n")

    for i, note in enumerate(notes[pdf_path], start=1):
        print(f"{i}. Page {note['page']}")

        print(f"   {note['note']}\n")


def edit_note(pdf_path):

    notes = load_notes()

    if pdf_path not in notes:
        print("No notes found")
        return

    if len(notes[pdf_path]) == 0:
        print("No notes found")
        return

    view_notes(pdf_path)

    try:
        choice = int(input("\nNote Number To Edit: "))

        if not 1 <= choice <= len(notes[pdf_path]):
            print("Invalid Selection")
            return

        new_note = input("\nNew Note:\n")

        if not new_note.strip():
            print("Note cannot be empty")
            return

        notes[pdf_path][choice - 1]["note"] = new_note

        save_notes(notes)

        print("Note Updated")

    except:
        print("Invalid Selection")


def delete_note(pdf_path):

    notes = load_notes()

    if pdf_path not in notes:
        print("No notes found")
        return

    if len(notes[pdf_path]) == 0:
        print("No notes found")
        return

    view_notes(pdf_path)

    try:
        choice = int(input("\nNote Number To Delete: "))

        if not 1 <= choice <= len(notes[pdf_path]):
            print("Invalid Selection")
            return

        notes[pdf_path].pop(choice - 1)

        save_notes(notes)

        print("Note Deleted")

    except:
        print("Invalid Selection")
