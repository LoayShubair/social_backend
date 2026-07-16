# Social Backend API

A backend-only social media API built using Django and Django REST Framework (DRF).

The project provides authentication, posts, comments, likes, follow relationships, and notifications.

## Features

* User registration and JWT authentication
* Create, update, delete, and view posts
* Comment system
* Like and unlike posts
* Follow users
* Notifications system:

  * Like notifications
  * Comment notifications
  * New post notifications for followers
* API-based backend using Django REST Framework

## Technologies

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication
* Git & GitHub
* Postman

## Project Structure

```
social_backend/
│
├── users/
│   ├── Authentication
│   └── Follow system
│
├── posts/
│   ├── Posts
│   ├── Comments
│   └── Likes
│
├── notifications/
│   └── User notifications
│
└── social_backend/
    └── Project configuration
```

## Installation

Clone the repository:

```bash
git clone https://github.com/LoayShubair/social_backend.git
```

Go to the project directory:

```bash
cd social_backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

## Run the Project

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

## Authentication

The project uses JWT authentication.

### Obtain Token

```
POST /api/token/
```

Example request:

```json
{
    "username": "username",
    "password": "password"
}
```

Use the access token in requests:

```
Authorization: Bearer <access_token>
```

## Main API Endpoints

### Users

Register:

```
POST /api/register/
```

### Posts

Get posts:

```
GET /posts/
```

Create post:

```
POST /posts/
```

Update/Delete post:

```
PUT /posts/{id}/
DELETE /posts/{id}/
```

### Likes

Like a post:

```
POST /posts/{id}/like/
```

Remove like:

```
DELETE /posts/{id}/like/
```

### Comments

Get comments:

```
GET /comments/
```

Create comment:

```
POST /comments/?post_id={id}
```

### Follow

Follow a user:

```
POST /api/follow/?follow={user_id}
```

### Notifications

Get notifications:

```
GET /api/notifications/
```

Mark notification as read:

```
POST /api/notifications/{id}/mark-read/
```

## Testing

The API endpoints were tested using Postman.

Tested features include:

* Authentication
* CRUD operations
* Likes
* Comments
* Follow relationships
* Notifications

## Team Project

This project was developed as a backend team project using Django REST Framework.

Each team member contributed to different applications and features.
