# Citizen Request Tracker

A full-stack **Django + Django REST Framework + PostgreSQL** application for managing citizen service requests with role-based access, dashboard analytics, CSV export, and audit logging.

This project was built to simulate a practical **government-style request management system** and to demonstrate backend architecture, permissions, and full CRUD workflows beyond a basic tutorial project.

---

## Features

### Core Features
- User authentication
- Role-based access control
- Create, read, update, and delete requests
- Search, filter, and pagination
- Dashboard analytics
- CSV export
- Audit logging for status changes
- Web UI and REST API support

### Business Rules
- **Admin/Staff**
  - Can view all requests
  - Can assign requests
  - Can update all statuses
  - Can manage all records
- **Regular Users**
  - Can create requests
  - Can only view their own requests
  - Cannot assign requests
  - Cannot set privileged fields freely
  - Cannot access admin-only actions

### Technical Highlights
- Custom user model
- Service-layer business logic
- Shared permission rules across UI and API
- Split settings for development and production
- PostgreSQL database integration
- Django REST Framework API endpoints

---

## Tech Stack

- **Backend:** Django
- **API:** Django REST Framework
- **Database:** PostgreSQL
- **Frontend:** Django Templates + Bootstrap 5
- **Language:** Python
- **Charts:** Chart.js

---
