from tkinter import *
from tkinter import messagebox

from aihelper import Browse, Popup, OkButton

from crplog import PersonalLogFiles
from crplog import initial


def looper():
    root = Tk()

    file = Browse(
        root,
        type="dir",
        title="Select Directory with User Planning",
        initial=initial,
    )
    OkButton(root, function=lambda: close(file_path=file, root=root))
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(parent=root))
    root.mainloop()


def on_closing(parent):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        parent.destroy()


def error(original, ins_text):
    original.insert(0, ins_text)
    return "\n".join(original)


def close(file_path, root):
    try:
        file_path = file_path.get()
        data = PersonalLogFiles(path=file_path)
        data.extract_data()
        data.save()
        permission = data.permission
        badlogs = data.badlogs
        if permission:
            unable_to_fetch = error(permission,
                                    "The following user log files are open. The data will not reflect their logs")
            Popup(text=unable_to_fetch, parent=root)
        if badlogs:
            bad_log_files = error(badlogs,
                                  "The following users have bad log data. An attempt was made to repair it in the compiled file", )
            Popup(text=bad_log_files, parent=root)
        Popup(text="All done", parent=root)
    except Exception as e:
        Popup(
            text=f"Something I failed to account for came up. The Following:  {e}",
            parent=root,
        )


if __name__ == "__main__":
    looper()
