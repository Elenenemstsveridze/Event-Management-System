Event Management System 🗓️
A Python application for managing events and participant registrations

🚀 Overview

The Event Management System is a Python-based desktop application built using Tkinter and SQLite. It allows users to create events, register participants, manage event details, and store data efficiently.

This project was developed as part of my university coursework to learn how to connect python and SQLite.

🌟 Features

1. Event Creation & Management – Users can add, edit, and delete events with details like date, time, location, and organizer information.
2. Participant Registration – Allows users to register for events, storing participant details securely.
3. SQLite Database Integration – Stores all event and participant data efficiently.
4. Data Validation – Ensures valid email formats, phone numbers, and unique participant identification.
5. User-Friendly Interface (Tkinter) – Simple and interactive UI for event and participant management.

📂 Project Structure

🔹 Database Setup (setup_db function) - The setup_db function creates tables for events and participants in an SQLite database.

    Initializes the database and ensures necessary tables exist.

🔹 Data Validation Functions - The project includes various validation functions to ensure correct user input.

    Ensures correct formatting of emails, phone numbers, and IDs.

🔹 Event Management (insert_event function) - Handles the creation of new events and checks for duplicates.

    Prevents duplicate events and ensures proper storage in SQLite.

🔹 Participant Registration (insert_participant function) - Allows users to register for an event and store participant details.

    Stores participant details securely and links them to events.

🔹 Tkinter GUI for User Interaction - The project includes a Tkinter-based UI for event and participant management.

    Provides a graphical user interface for event creation, registration, and data retrieval.

✨ Final Thoughts

This project was a great way to practice Python, SQLite, and GUI development. It helped me understand database relationships, user input validation, and event-driven programming.
