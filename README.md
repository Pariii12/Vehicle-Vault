# 🚗 Vehicle Vault

Vehicle Vault is a full-stack Django-based web platform designed to simplify used-vehicle buying and selling. It enables users to list vehicles, explore inspections, communicate with buyers/sellers, schedule test drives, and securely complete transactions.

It includes role-based dashboards, OTP-based first-time account activation and a modern template-based UI.

__________________


## 🚀 Key Highlights

+ Custom authentication system with role-based access (Admin, Buyer, Seller), account states (Inactive, Active, Blocked, Deleted)

+ Secure OTP-based account activation

+ Complete vehicle listing lifecycle management

+ Buyer–Seller real-time communication system

+ Integrated Razorpay payment gateway (Payment hosted page)

+ Test drive scheduling and tracking

+ Role-specific dashboards with activity tracking

+ Fully responsive UI using Django templates

____

## ✨ Core Features

### 🔐 Authentication & User Management

+ User registration and login system

+ OTP-based first-time account verification
  
+ Resend OTP functionality
  
+ Role-based user handling (Admin, Buyer, Seller)

+ Account status control (Active, Inactive, Blocked, Deleted)


### 🚗 Vehicle Lists
+ Add, edit, and delete vehicle lists
+ Upload vehicle images and details
+ Lists status tracking:
    + Active
    + Pending
    + Sold
+ Browse vehicles by price/brand
+ Detailed vehicle information pages
+ Vehicle comparison functionality

### 💬 Messaging & Deal Flow

+ Buyer ↔ Seller messaging system
+ Conversation-based deal negotiation
+ Deal acceptance directly from chat
+ Automatic transaction creation on deal confirmation

### 💳 Payments & Transactions

+ Razorpay payment integration
+ Secure order creation and verification
+ Transaction history tracking
+ Automatic update of listing status after payment

### 📅 Test Drive Management

+ Request test drives for vehicles
+ Manage test drive schedules
+ Track test drive status updates

### 📊 Dashboard & Activity
+ Role-based dashboards:
   + Admin Dashboard
   + Buyer Dashboard
   + Seller Dashboard
    
+ Activity tracking modules:
   + Tasks / To-do list
   + Meeting scheduling
   + Activity history logs
    
+ Sales and purchase insights

_____

## 🧰 Tech Stack

+ Backend: Django
+ Database: PostgreSQL
+ Frontend: HTML, CSS, JavaScript (Django Templates)
+ Payments: Razorpay
+ Media Handling: Pillow

_____

## 📁 Project Structure  

	DJANGO_VEHICLEVAULT/
	│
	├── vehiclevault/                     # Main Django project folder
	│   │
	│   ├── vehiclevault/                # Project configuration (settings)
	│   │   ├── __init__.py
	│   │   ├── settings.py              # Global settings (DB, apps, static/media)
	│   │   ├── urls.py                  # Root URL routing
	│   │   ├── asgi.py
	│   │   └── wsgi.py
	│   │
	│   ├── core/                        # Authentication & core logic
	│   │   ├── migrations/              # Database migrations
	│   │   ├── __pycache__/
	│   │   ├── __init__.py
	│   │   ├── admin.py                 # Admin configuration
	│   │   ├── apps.py
	│   │   ├── auth_backend.py          # Custom authentication backend
	│   │   ├── forms.py                 # Login/Signup/OTP forms
	│   │   ├── models.py                # User and core models
	│   │   ├── tests.py
	│   │   ├── urls.py                  # Core routes (auth, etc.)
	│   │   └── views.py                 # Authentication & OTP logic
	│   │
	│   ├── vehicle/                     # Vehicle & business logic module
	│   │   ├── migrations/
	│   │   ├── __pycache__/
	│   │   ├── __init__.py
	│   │   ├── admin.py
	│   │   ├── apps.py
	│   │   ├── decorators.py            # Role-based access decorators
	│   │   ├── forms.py                 # Vehicle, offer, payment forms
	│   │   ├── models.py                # Vehicle, offers, payments, transactions
	│   │   ├── tests.py
	│   │   ├── urls.py                  # Vehicle-related routes
	│   │   └── views.py                 # Listings, offers, payments logic
	│   │
	│   ├── templates/                   # HTML Templates
	│   │   │
	│   │   ├── core/                    # Authentication pages
	│   │   │   ├── login.html
	│   │   │   ├── logout.html
	│   │   │   ├── signup.html
	│   │   │   └── verify_otp.html
	│   │   │
	│   │   ├── home/
	│   │   │   └── index.html
	│   │   │
	│   │   ├── favourites/
	│   │   │   └── favourite_list.html
	│   │   │
	│   │   ├── inspections/
	│   │   │   └── inspection_report.html
	│   │   │
	│   │   ├── messages/
	│   │   │   ├── chat.html
	│   │   │   └── inbox.html
	│   │   │
	│   │   ├── offers/
	│   │   │   ├── make_offer.html
	│   │   │   ├── my_offer.html
	│   │   │   └── offer_details.html
	│   │   │
	│   │   ├── payments/
	│   │   │   ├── checkout.html
	│   │   │   └── payment_list.html
	│   │   │
	│   │   ├── testdrives/
	│   │   │   ├── my_testdrive.html
	│   │   │   └── schedule_testdrive.html
	│   │   │
	│   │   ├── transactions/
	│   │   │   ├── add_transaction.html
	│   │   │   ├── transaction_detail.html
	│   │   │   └── transaction_list.html
	│   │   │
	│   │   ├── vehicles/                # Vehicle UI pages
	│   │   │   ├── admin/
	│   │   │   │   ├── admin_dashboard.html
	│   │   │   │   └── adminnavbar.html
	│   │   │   │
	│   │   │   ├── buyer/
	│   │   │   │   ├── buyer_dashboard.html
	│   │   │   │   └── buyernavbar.html
	│   │   │   │
	│   │   │   ├── seller/
	│   │   │   │   ├── seller_dashboard.html
	│   │   │   │   └── sellernavbar.html
	│   │   │   │
	│   │   │   ├── add_vehicle.html
	│   │   │   ├── edit_vehicle.html
	│   │   │   ├── delete_vehicle.html
	│   │   │   ├── vehicle_detail.html
	│   │   │   ├── vehicle_list.html
	│   │   │   └── compare_vehicle.html
	│   │   │
	│   │   ├── base.html
	│   │   ├── navbar.html
	│   │   └── footer.html
	│   │
	│   ├── static/                      # Static files (CSS, JS, Images)
	│   │   ├── css/
	│   │   │   └── style.css
	│   │   ├── brands/
	│   │   └── home/img/
	│   │       └── bmw-m4-hero.jpg
	│   │
	│   ├── media/                       # Uploaded media files
	│   │   └── vehicle_images/
	│   │       ├── bmw_3series.jpeg
	│   │       ├── hyundai_creta.jpeg
	│   │       ├── rr_ghost_front.jpeg
	│   │       └── ...
	│   │
	│   ├── manage.py                    # Django management script
	│   └── db.sqlite3                  # Local database (development)
	│
	├── venv/                            # Virtual environment (not for GitHub)
	├── .gitignore                       # Git ignored files
	└── README.md                        # Project documentation
 ______

 ## 🏁 Quick Start (Local Setup)
 ### 1) Clone and enter project
   + Clone the repository
   + Open the project folder in VS Code or terminal
### 2) Create virtual environment
   + Windows (PowerShell): python -m venv .venv
   + Activate: .venv\Scripts\Activate.ps1
### 3) Install dependencies
   + pip install -r requirements.txt

### 4) Configure environment

Create a .env file and add:

		SECRET_KEY=your_secret_key
		DEBUG=True
		
		DB_NAME=vehicle_vault
		DB_USER=postgres
		DB_PASSWORD=your_password
		DB_HOST=localhost
		DB_PORT=5432
		EMAIL_HOST_USER=your_email
		EMAIL_HOST_PASSWORD=your_email_password

### 5️) Setup Database
 + Create PostgreSQL database
 + Name it vehicle_vault

### 6️) Run Migrations
  + python manage.py makemigrations
  + python manage.py migrate

### 7️) Create Superuser
  + python manage.py createsuperuser

###	8) Run server
  + python manage.py runserver
  + Open: http://127.0.0.1:8000/
_____

## 🔐 Authentication Flow

### Signup
1. User registers from /signup/
2. Account is created with status = Inactive
3. OTP is generated and emailed

### First Login (OTP required)
1. User logs in from /login/
2. If status is Inactive, OTP is requested
3. OTP verification endpoint: /verify-otp/
4. On success:
    + status changes to Active
    + enter otpp code and user is logged in
      
### After Activation
  + Future logins do not require OTP (unless status is manually changed back to Inactive)

### Account Status Handling
+ Active → normal login allowed
+ Inactive → OTP verification required
+ Blocked → login denied
+ Deleted → login denied
_____

## 🔄 Main Workflows

### 📌 Listings
 + Sellers create vehicle listings
 + Buyers browse and view details
   
### 📌 Messaging
 + Buyers contact sellers
 + Deals are negotiated via chat
### 📌 Transactions
 + Payment processed via Razorpay
 + Listing marked as Sold automatically
### 📌 Test Drives
 + Buyers request test drives
 + Sellers manage scheduling

_______

## 🧪 Testing
Run all tests:

 + python manage.py test

________

## ⚠️ Security Notes

 + Do not expose secret keys
 + Use environment variables
 + Set DEBUG=False in production
 + Configure ALLOWED_HOSTS properly
 + Use HTTPS in deployment

_______

## 📌 Current Project Status
This repository contains a working Django application with integrated core flows (auth, listings, messaging, test drives, dashboards). Some setup docs may still reflect older stack notes; this README is the authoritative high-level workflow document for the current codebase.

