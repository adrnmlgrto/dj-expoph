# ExpoPH (1.0.0)

A **personal project** for a local marketplace platform in the Philippines, designed for selling both *digital* and *physical* products aiming to potentially provide independent creators and businesses a space to showcase their products or goods while offering a smooth shopping experience for buyers.

Future plans include integrated payouts for shop owners through designated payout accounts using local & international payment processors. This repository contains the backend implementation of the platform.

## Features
- Integrated product inventory management for shop owners.
- Scheduled payouts for shop owners. (**TO BE IMPLEMENTED**)

## Requirements

- **Python 3.12+**
- **Django 5.1**
- **Supabase**

> *Supabase is primarily used for its database (PostgreSQL) & storage backend.*

## Installation

1. Clone the Repository:

   ```bash
   git clone https://github.com/adrnmlgrto/dj-expoph.git
   ```
2. Navigate to the Project Directory:

   ```bash
   cd dj-expoph
   ```
3. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Setup the Database and Storage Backend via [Supabase](https://supabase.com/)
    - Set up an account and create a project under an organization via the dashboard.
    - Create the PostgreSQL database and storage for setting up URLs on the environment below.

5. Set Up Environment Variables
    - Create a `.env` file in the project root directory.
    - Add the environment variables.

    > Please see [`.env.example`](.env.example) file for the needed environment variables.

## Usage

1. Run the Django Development Server:

   ```bash
   python manage.py runserver
   ```
2. Access the Application via `http://localhost:8000/`.