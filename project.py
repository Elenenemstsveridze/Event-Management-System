import sqlite3
from tkinter import *
from tkinter import messagebox, ttk


def setup_db():
    conn = sqlite3.connect('EventManagementSystem.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
        Event_id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
        Event_name NVARCHAR NOT NULL,
        Event_date DATE NOT NULL,
        Event_time NVARCHAR NOT NULL,
        Location NVARCHAR NOT NULL,
        Description NVARCHAR,
        Organizer_name NVARCHAR NOT NULL,
        Organizer_last_name NVARCHAR NOT NULL,
        Organizer_email VARCHAR NOT NULL,
        Personal_id VARCHAR NOT NULL CHECK (length(Personal_id) = 11 AND Personal_id GLOB '[0-9]*')
    )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Participants (
        Participant_id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
        Event_id INTEGER NOT NULL,
        Name NVARCHAR NOT NULL,
        Last_name NVARCHAR NOT NULL,
        Email VARCHAR NOT NULL,
        Phone VARCHAR NOT NULL CHECK (length(Phone) = 9 AND Phone GLOB '[0-9]*'),
        Gender NVARCHAR NOT NULL CHECK (Gender IN ('მდედრობითი', 'მამრობითი', 'სხვა')),
        FOREIGN KEY (Event_id) REFERENCES Events (Event_id)
    )''')

    conn.commit()
    conn.close()


def is_alphabetic(s):
    for char in s:
        if not (char.isalpha() or char.isspace()):
            return False
    return True


def is_valid_email(email):
    if "@" not in email or "." not in email:
        return False
    return True


def validate_event(event):
    event_time = event[2]
    event_date = event[1]

    if len(event_time) != 5 or event_time[2] != ':' or not event_time.replace(':', '').isdigit():
        return "დრო უნდა იყოს ფორმატში HH:MM."

    if len(event_date) != 10 or event_date[4] != '-' or event_date[7] != '-' or not event_date.replace('-', '').isdigit():
        return "თარიღი უნდა იყოს ფორმატში YYYY-MM-DD."

    if len(event[8]) != 11 or not event[8].isdigit():
        return "პირადი ნომერი უნდა იყოს 11 ციფრი"

    if not is_alphabetic(event[0]):
        return "ღონისძიების სახელი უნდა შეიცავდეს მხოლოდ ანბანის სიმბოლოებს."
    if not is_alphabetic(event[3]):
        return "მისამართი უნდა შეიცავდეს მხოლოდ ანბანის სიმბოლოებს."
    if event[4] and not is_alphabetic(event[4]):
        return "აღწერა უნდა შეიცავდეს მხოლოდ ანბანის სიმბოლოებს."
    if not is_alphabetic(event[5]):
        return "ორგანიზატორის სახელი უნდა შეიცავდეს მხოლოდ ანბანის სიმბოლოებს."
    if not is_alphabetic(event[6]):
        return "ორგანიზატორის გვარი უნდა შეიცავდეს მხოლოდ ანბანის სიმბოლოებს."
    if not is_valid_email(event[7]):
        return "გთხოვთ შეიყვანოთ სწორი ელ. ფოსტის მისამართი."


def validate_input():
    if not selected_event_name.get():
        return "გთხოვთ შეავსოთ ფორმა მთლიანად."
    if not participant_name_entry.get().strip():
        return "გთხოვთ შეავსოთ ფორმა მთლიანად."
    if not participant_last_name_entry.get().strip():
        return "გთხოვთ შეავსოთ ფორმა მთლიანად."
    if not participant_email_entry.get().strip():
        return "გთხოვთ შეავსოთ ფორმა მთლიანად."
    if not participant_gender_var.get().strip():
        return "გთხოვთ შეავსოთ ფორმა მთლიანად."

    phone = participant_phone_entry.get().strip()
    if not phone or len(phone) != 9 or not phone.isdigit():
        return "გთხოვთ შეიყვანოთ სწორი მობილური ნომერი (9 ციფრი)."

    if not is_alphabetic(participant_name_entry.get().strip()):
        return "სახელი უნდა შეიცავდეს მხოლოდ ანბანის სიმბოლოებს."
    if not is_alphabetic(participant_last_name_entry.get().strip()):
        return "გვარი უნდა შეიცავდეს მხოლოდ ანბანის სიმბოლოებს."
    if not is_valid_email(participant_email_entry.get().strip()):
        return "გთხოვთ შეიყვანოთ სწორი ელ. ფოსტის მისამართი."

    return ""


def insert_event(event, add_event_window=None):
    error_message = validate_event(event)
    if error_message:
        messagebox.showwarning("Input Error", error_message)
        return

    conn = sqlite3.connect('EventManagementSystem.db')
    conn.text_factory = str
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT Event_id FROM Events WHERE Event_name = ? AND Event_date = ?
        ''', (event[0], event[1]))
        existing_event = cursor.fetchone()

        if existing_event:
            messagebox.showwarning("Warning", "ეს ღონისძიება უკვე არსებობს: {}".format(event[0]))
        else:
            cursor.execute('''
                INSERT INTO Events (Event_name, Event_date, Event_time, Location, Description, Organizer_name, Organizer_last_name, Organizer_email, Personal_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', event)
            conn.commit()
            messagebox.showinfo("Success", "ღონისძიება დაემატა წარმატებით")
            if add_event_window:
                add_event_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()


def populate_events():
    events = [
        ("კონფერენცია", "2024-06-20", "09:00", "საკონფერენციო ცენტრი A", "წლიური კონფერენცია ტექნოლოგიაზე", "ჯონ", "დოუ", "john.doe@example.com", "12345678901"),
        ("ვორქშოპი", "2024-07-05", "14:30", "სავარჯიშო ოთახი B", "შესავალი პითონის პროგრამირებაში", "ჯეინი", "სმიტი", "jane.smith@example.com", "10987654321"),
        ("სემინარი", "2024-07-15", "10:00", "სემინარის დარბაზი C", "მარკეტინგის სტრატეგიები სტარტაპებისთვის", "მაიკლ", "ჯონსონი", "michael.johnson@example.com", "11223344556")
    ]
    for event in events:
        insert_event(event)


def insert_participant(add_participant_window):
    error_message = validate_input()
    if error_message:
        messagebox.showwarning("Input Error", error_message)
        return

    conn = sqlite3.connect('EventManagementSystem.db')
    conn.text_factory = str
    cursor = conn.cursor()
    try:
        event_name = selected_event_name.get()
        cursor.execute('SELECT Event_id FROM Events WHERE Event_name = ?', (event_name,))
        event_id = cursor.fetchone()
        if event_id:
            event_id = event_id[0]
            cursor.execute('''
                INSERT INTO Participants (Event_id, Name, Last_name, Email, Phone, Gender)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                event_id,
                participant_name_entry.get(),
                participant_last_name_entry.get(),
                participant_email_entry.get(),
                participant_phone_entry.get(),
                participant_gender_var.get()
            ))
            conn.commit()
            messagebox.showinfo("Success", "წარმატებით გაიარეთ რეგისტრაცია.")
            add_participant_window.destroy()
        else:
            messagebox.showerror("Error", "ღონისძიებები ვერ მოიძებნა.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()


def open_add_participant_window():
    try:
        add_participant_window = Toplevel(root)
        add_participant_window.title("მონაწილის რეგისტრაცია")
        add_participant_window.configure(bg="#e6f7ff")
        add_participant_window.geometry("450x350")

        add_participant_window.grid_rowconfigure(0, pad=20)
        add_participant_window.grid_rowconfigure(1, pad=20)
        add_participant_window.grid_rowconfigure(2, pad=20)
        add_participant_window.grid_rowconfigure(3, pad=20)
        add_participant_window.grid_rowconfigure(4, pad=20)
        add_participant_window.grid_rowconfigure(5, pad=20)
        add_participant_window.grid_rowconfigure(6, pad=20)
        add_participant_window.grid_rowconfigure(7, pad=20)

        add_participant_window.grid_columnconfigure(0, pad=20)
        add_participant_window.grid_columnconfigure(1, pad=20)
        add_participant_window.grid_columnconfigure(2, pad=20)
        add_participant_window.grid_columnconfigure(3, pad=20)
        add_participant_window.grid_columnconfigure(4, pad=20)
        add_participant_window.grid_columnconfigure(5, pad=20)

        Label(add_participant_window, text="ღონისძიების სახელი", bg="#e6f7ff", fg="#00064b").grid(row=0, column=0)

        conn = sqlite3.connect('EventManagementSystem.db')
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('SELECT Event_name FROM Events')
        event_names = [row[0] for row in cursor.fetchall()]
        conn.close()

        global selected_event_name
        selected_event_name = StringVar()
        selected_event_name.set(event_names[0] if event_names else "")

        style = ttk.Style()
        style.configure("TMenubutton", background="#B3E7FF", foreground="#00064b")

        event_name_menu = ttk.OptionMenu(add_participant_window, selected_event_name, *event_names)
        event_name_menu.grid(row=0, column=1, sticky='ew')

        menu = event_name_menu["menu"]
        menu.configure(bg="#B3E7FF", fg="#00064b")

        for i in range(len(event_names)):
            menu.entryconfig(i, background="#B3E7FF", foreground="#00064b", activebackground="#A3D7EF", activeforeground="#00064b")

        Label(add_participant_window, text="სახელი", bg="#e6f7ff", fg="#00064b").grid(row=1, column=0)
        global participant_name_entry
        participant_name_entry = Entry(add_participant_window)
        participant_name_entry.grid(row=1, column=1)

        Label(add_participant_window, text="გვარი", bg="#e6f7ff", fg="#00064b").grid(row=2, column=0)
        global participant_last_name_entry
        participant_last_name_entry = Entry(add_participant_window)
        participant_last_name_entry.grid(row=2, column=1)

        Label(add_participant_window, text="ელ. ფოსტა", bg="#e6f7ff", fg="#00064b").grid(row=3, column=0)
        global participant_email_entry
        participant_email_entry = Entry(add_participant_window)
        participant_email_entry.grid(row=3, column=1)

        Label(add_participant_window, text="მობილური", bg="#e6f7ff", fg="#00064b").grid(row=4, column=0)
        global participant_phone_entry
        participant_phone_entry = Entry(add_participant_window)
        participant_phone_entry.grid(row=4, column=1)

        Label(add_participant_window, text="გენდერი", bg="#e6f7ff", fg="#00064b").grid(row=5, column=0)
        global participant_gender_var
        participant_gender_var = StringVar()
        participant_gender_var.set("მდედრობითი")

        gender_frame = Frame(add_participant_window, bg="#e6f7ff")
        gender_frame.grid(row=5, column=1, sticky='w')

        Radiobutton(gender_frame, text="მდედრობითი", variable=participant_gender_var, value="მდედრობითი", bg="#e6f7ff").pack(side=LEFT)
        Radiobutton(gender_frame, text="მამრობითი", variable=participant_gender_var, value="მამრობითი", bg="#e6f7ff").pack(side=LEFT)
        Radiobutton(gender_frame, text="სხვა", variable=participant_gender_var, value="სხვა", bg="#e6f7ff").pack(side=LEFT)

        Button(add_participant_window, text="რეგისტრაცია", bg="#B3E7FF", activebackground="#A3D7EF", command=lambda: insert_participant(add_participant_window)).grid(row=6, column=0, columnspan=2)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ვერ დაუკავშირდა მონაცემთა ბაზას: {str(e)}")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))


def open_add_event_window():
    add_event_window = Toplevel(root)
    add_event_window.title("ღონისძიების დამატება")
    add_event_window.configure(bg="#e6f7ff")
    add_event_window.geometry("340x440")

    Label(add_event_window, text="ღონისძიების სახელი", bg="#e6f7ff", fg="#00064b").grid(row=0, column=0, pady=10, padx=10)
    global event_name_entry
    event_name_entry = Entry(add_event_window)
    event_name_entry.grid(row=0, column=1, pady=10, padx=10)

    Label(add_event_window, text="თარიღი", bg="#e6f7ff", fg="#00064b").grid(row=1, column=0, pady=10, padx=10)
    global event_date_entry
    event_date_entry = Entry(add_event_window)
    event_date_entry.grid(row=1, column=1, pady=10, padx=10)

    Label(add_event_window, text="დრო", bg="#e6f7ff", fg="#00064b").grid(row=2, column=0, pady=10, padx=10)
    global event_time_entry
    event_time_entry = Entry(add_event_window)
    event_time_entry.grid(row=2, column=1, pady=10, padx=10)

    Label(add_event_window, text="მისამართი", bg="#e6f7ff", fg="#00064b").grid(row=3, column=0, pady=10, padx=10)
    global location_entry
    location_entry = Entry(add_event_window)
    location_entry.grid(row=3, column=1, pady=10, padx=10)

    Label(add_event_window, text="მოკლე აღწერა", bg="#e6f7ff", fg="#00064b").grid(row=4, column=0, pady=10, padx=10)
    global description_entry
    description_entry = Entry(add_event_window)
    description_entry.grid(row=4, column=1, pady=10, padx=10)

    Label(add_event_window, text="ორგანიზატორის სახელი", bg="#e6f7ff", fg="#00064b").grid(row=5, column=0, pady=10, padx=10)
    global organizer_name_entry
    organizer_name_entry = Entry(add_event_window)
    organizer_name_entry.grid(row=5, column=1, pady=10, padx=10)

    Label(add_event_window, text="ორგანიზატორის გვარი", bg="#e6f7ff", fg="#00064b").grid(row=6, column=0, pady=10, padx=10)
    global organizer_last_name_entry
    organizer_last_name_entry = Entry(add_event_window)
    organizer_last_name_entry.grid(row=6, column=1, pady=10, padx=10)

    Label(add_event_window, text="ელ. ფოსტა", bg="#e6f7ff", fg="#00064b").grid(row=7, column=0, pady=10, padx=10)
    global organizer_email_entry
    organizer_email_entry = Entry(add_event_window)
    organizer_email_entry.grid(row=7, column=1, pady=10, padx=10)

    Label(add_event_window, text="პირადი ნომერი", bg="#e6f7ff", fg="#00064b").grid(row=8, column=0, pady=10, padx=10)
    global personal_id_entry
    personal_id_entry = Entry(add_event_window)
    personal_id_entry.grid(row=8, column=1, pady=10, padx=10)

    Button(add_event_window, text="დამატება", bg="#B3E7FF", activebackground="#A3D7EF", command=lambda: insert_event(
        (
            event_name_entry.get(),
            event_date_entry.get(),
            event_time_entry.get(),
            location_entry.get(),
            description_entry.get(),
            organizer_name_entry.get(),
            organizer_last_name_entry.get(),
            organizer_email_entry.get(),
            personal_id_entry.get()
        ), add_event_window
    )).grid(row=9, column=0, columnspan=2, pady=20, padx=10)


def open_changes_window():
    try:
        changes_window = Toplevel(root)
        changes_window.title("ორგანიზატორის ცვლილებები")
        changes_window.configure(bg="#e6f7ff")
        changes_window.geometry("270x90")

        changes_window.grid_rowconfigure(0, pad=20)
        changes_window.grid_rowconfigure(1, pad=20)
        changes_window.grid_columnconfigure(0, pad=20)
        changes_window.grid_columnconfigure(1, pad=20)

        Label(changes_window, text="პირადი ნომერი", bg="#e6f7ff", fg="#00064b").grid(row=0, column=0)
        global organizer_personal_id_entry
        organizer_personal_id_entry = Entry(changes_window)
        organizer_personal_id_entry.grid(row=0, column=1)

        Button(changes_window, text="ძიება", bg="#B3E7FF", activebackground="#A3D7EF", command=lambda: search_events_by_personal_id(changes_window)).place(x=110, y=45)

    except Exception as ex:
        messagebox.showerror("Error", str(ex))


def search_events_by_personal_id(changes_window):
    try:
        personal_id = organizer_personal_id_entry.get()
        if len(personal_id) != 11 or not personal_id.isdigit():
            messagebox.showerror("Error", "პირადი ნომერი უნდა იყოს 11 ციფრი")
            return

        conn = sqlite3.connect('EventManagementSystem.db')
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Events WHERE Personal_id = ?', (personal_id,))
        events = cursor.fetchall()
        conn.close()

        if not events:
            messagebox.showinfo("Info", "ამ პირადი ნომრით არ არის ღონისძიებები ნაპოვნი")
            return

        global events_window
        events_window = Toplevel(root)
        events_window.title("ორგანიზატორის ღონისძიებები")
        events_window.geometry("330x150")
        events_window.configure(bg="#e6f7ff")

        for idx, event in enumerate(events):
            event_id, event_name, event_date, event_time, location, description, organizer_name, organizer_last_name, organizer_email, personal_id = event
            event_text = f"ღონისძიება: {event_name}\nღონისძიების ჩატარების თარიღი: {event_date}\nღონისძიების ჩატარების საათი: {event_time}\nმისამართი: {location}"
            event_label = Label(events_window, text=event_text, bg="#e6f7ff", fg="#00064b", anchor="w", justify=CENTER)
            event_label.place(x=30, y=10)

            Button(events_window, text="წაშლა", bg="#B3E7FF", activebackground="#A3D7EF", command=lambda e_id=event_id: delete_event(e_id)).place(x=50, y=100)
            Button(events_window, text="განახლება", bg="#B3E7FF", activebackground="#A3D7EF", command=lambda e=event: open_update_event_window(e)).place(x=200, y=100)

        changes_window.destroy()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ვერ დაუკავშირდა მონაცემთა ბაზას: {str(e)}")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))


def delete_event(event_id):
    answer = messagebox.askyesno("Confirm Delete", "დარწმუნებული ხართ, რომ გსურთ ამ ღონისძიების სამუდამოდ წაშლა?")
    if not answer:
        return

    conn = sqlite3.connect('EventManagementSystem.db')
    conn.text_factory = str
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM Events WHERE Event_id = ?', (event_id,))
        conn.commit()
        messagebox.showinfo("Success", "ღონისძიება წაიშალა წარმატებით")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))
    finally:
        conn.close()


def open_update_event_window(event):
    try:
        global update_event_window
        events_window.destroy()
        event_id, event_name, event_date, event_time, location, description, organizer_name, organizer_last_name, organizer_email, personal_id = event

        update_event_window = Toplevel(root)
        update_event_window.title("ღონისძიების განახლება")
        update_event_window.configure(bg="#e6f7ff")
        update_event_window.geometry("350x200")

        update_event_window.grid_rowconfigure(0, pad=20)
        update_event_window.grid_rowconfigure(1, pad=20)
        update_event_window.grid_rowconfigure(2, pad=20)

        update_event_window.grid_columnconfigure(0, pad=20)
        update_event_window.grid_columnconfigure(1, pad=20)
        update_event_window.grid_columnconfigure(2, pad=20)

        Label(update_event_window, text="ღონისძიების ჩატარების თარიღი", bg="#e6f7ff", fg="#00064b").grid(row=0, column=0)
        event_date_entry = Entry(update_event_window)
        event_date_entry.insert(0, event_date)
        event_date_entry.grid(row=0, column=1)

        Label(update_event_window, text="ღონისძიების ჩატარების საათი", bg="#e6f7ff", fg="#00064b").grid(row=1, column=0)
        event_time_entry = Entry(update_event_window)
        event_time_entry.insert(0, event_time)
        event_time_entry.grid(row=1, column=1)

        Label(update_event_window, text="მისამართი", bg="#e6f7ff", fg="#00064b").grid(row=2, column=0)
        location_entry = Entry(update_event_window)
        location_entry.insert(0, location)
        location_entry.grid(row=2, column=1)

        Button(update_event_window, text="განახლება", bg="#B3E7FF", activebackground="#A3D7EF", command=lambda: update_event(event_id, event_date_entry.get(), event_time_entry.get(), location_entry.get())).place(x=140, y=160)

    except Exception as ex:
        messagebox.showerror("Error", str(ex))


def update_event(event_id, new_date, new_time, new_location):
    conn = sqlite3.connect('EventManagementSystem.db')
    conn.text_factory = str
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE Events
            SET Event_date = ?, Event_time = ?, Location = ?
            WHERE Event_id = ?
        ''', (new_date, new_time, new_location, event_id))
        conn.commit()
        messagebox.showinfo("Success", "ღონისძიება განახლდა წარმატებით")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ვერ დაუკავშირდა მონაცემთა ბაზას: {str(e)}")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))
    finally:
        conn.close()


def open_information_window():
    try:
        info_window = Toplevel(root)
        info_window.title("ინფორმაციის ფანჯარა")
        info_window.geometry("500x600")
        info_window.configure(bg="#e6f7ff")

        Label(info_window, text="ღონისძიების სია", bg="#e6f7ff", fg="#00064b", font=(None, 14, 'bold')).pack(pady=10)

        global event_listbox
        event_listbox = Listbox(info_window, width=50, height=20)
        event_listbox.pack(pady=10)
        event_listbox.bind('<<ListboxSelect>>', display_event_details)

        conn = sqlite3.connect('EventManagementSystem.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Event_name FROM Events")
        events = cursor.fetchall()

        for event in events:
            event_listbox.insert(END, event[0])

        global event_details_text
        event_details_text = Text(info_window, width=50, height=10, wrap=WORD)
        event_details_text.pack(pady=10)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ვერ დაუკავშირდა მონაცემთა ბაზას: {str(e)}")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))


def display_event_details(event):
    try:
        selected_event_index = event_listbox.curselection()
        if selected_event_index:
            selected_event_name = event_listbox.get(selected_event_index)

            conn = sqlite3.connect('EventManagementSystem.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Events WHERE Event_name = ?", (selected_event_name,))
            event_details = cursor.fetchone()

            if event_details:
                cursor.execute("SELECT Name, Last_name FROM Participants WHERE Event_id = ?", (event_details[0],))
                participants = cursor.fetchall()

                event_details_text.delete(1.0, END)
                event_details_text.insert(END, f"ღონისძიების სახელი: {event_details[1]}\n")
                event_details_text.insert(END, f"ღონისძიების ჩატარების თარიღი: {event_details[2]}\n")
                event_details_text.insert(END, f"ღონისძიების ჩატარების საათი: {event_details[3]}\n")
                event_details_text.insert(END, f"მისამართი: {event_details[4]}\n")
                event_details_text.insert(END, f"მოკლე აღწერა: {event_details[5]}\n")
                event_details_text.insert(END, f"ორგანიზატორის სახელი: {event_details[6]} {event_details[7]}\n")
                event_details_text.insert(END, f"ორგანიზატორის მეილი: {event_details[8]}\n")

                event_details_text.insert(END, "\nᲛონაწილეები:\n")
                for participant in participants:
                    event_details_text.insert(END, f"{participant[0]} {participant[1]}\n")
            else:
                messagebox.showwarning("No Event Found", "არჩეული ღონისძიება ვერ მოიძებნა მონაცემთა ბაზაში.")

            conn.close()
        else:
            messagebox.showwarning("Selection Error", "გთხოვთ, აირჩიოთ ღონისძიება სიიდან.")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"ვერ დაუკავშირდა მონაცემთა ბაზას: {str(e)}")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))


try:
    setup_db()
    populate_events()

    root = Tk()
    root.geometry("300x210")
    root.title("ღონისძიებების მართვის სისტემა")
    root.configure(bg="#e6f7ff")

    Label(root, text="აირჩიეთ ერთ-ერთი:", bg="#e6f7ff", fg="#00064b", font=(None, 14, 'bold')).place(x=60, y=20)

    b1 = Button(root, text="ღონისძიების დამატება", bg="#B3E7FF", activebackground="#A3D7EF", command=open_add_event_window)
    b1.place(x=75, y=60)
    b2 = Button(root, text="რეგისტრაცია", bg="#B3E7FF", activebackground="#A3D7EF", command=open_add_participant_window)
    b2.place(x=105, y=95)
    b3 = Button(root, text="ცვლილებები", bg="#B3E7FF", activebackground="#A3D7EF", command=open_changes_window)
    b3.place(x=105, y=130)
    b4 = Button(root, text="ინფორმაცია", bg="#B3E7FF", activebackground="#A3D7EF", command=open_information_window)
    b4.place(x=106, y=165)

    root.mainloop()

except Exception as ex:
    print(ex.args[0])
