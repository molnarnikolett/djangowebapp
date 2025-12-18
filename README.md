# Régiségek Online Aukciós Háza (Django)

Django-based website for an antiques auction house.  
The project contains multiple informational pages and an auction items page where objects
and their descriptions are stored in a local SQLite database.

## Technologies
- Python
- Django
- SQLite
- Bootstrap
- Django Templates (base template + navigation)

## Pages / Sections
- About (company introduction)
- Team (employees / coworkers)
- Contact
- Auction Items (paintings, jewelry, porcelain)

## Data Model
Auction items are stored in a SQLite database with the following fields:
- name (megnevezés)
- starting price (induló ár)
- auction time (árverés ideje)

## Implemented Features
- Base template with shared layout and navigation menu
- Bootstrap styling
- Images for auction items and team members
- SQLite-based persistence for auction items

## Notes / Scope
This project focuses on the core Django fundamentals:
template inheritance, static/media handling, and database-backed content.

Optional features such as user registration, bidding workflow, roles, pagination,
admin-side auction management beyond basic admin, and automated tests were out of scope
for this implementation.

