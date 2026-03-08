# Citizen Request Tracker

A Django + Django REST Framework + PostgreSQL application for managing citizen service requests with role-based access, dashboard analytics, CSV export, and audit logging.

## Features

- User authentication
- Role-based access control
- Create, read, update, and delete requests
- Search, filter, and pagination
- Dashboard charts and summary cards
- CSV export
- Audit log for status changes
- Web UI and REST API

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Bootstrap 5
- Chart.js

## User Roles

**Admin / Staff**
- Can view all requests
- Can assign requests
- Can update statuses
- Can manage all records

**Regular User**
- Can create requests
- Can view only their own requests
- Cannot access admin-only actions

## Main Models

- `CustomUser`
- `Category`
- `Request`
- `StatusChange`
