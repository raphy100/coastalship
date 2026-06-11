# CoastalShip Logistics Message History API

A Django REST Framework implementation of the CoastalShip Logistics assessment task.

## Overview

This project provides a REST API endpoint for retrieving chat message history from a mock in-memory data source.

Endpoint:

GET /api/messages/history

The endpoint supports:

- Retrieving messages for a specific room
- Pagination using `since` and `limit`
- Input validation
- Proper HTTP status codes
- Error handling

No database or external service is used. All data comes from a mock Python dictionary.

---

## Technology Stack

- Python 3.10+
- Django 5.x
- Django REST Framework

---

## Dependencies

Install the required packages:

```bash
pip install django djangorestframework

pip install -r requirements.txt
git clone https://github.com/YOUR_USERNAME/coastalship-api.git

cd coastalship-api
python -m venv venv

venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
http://127.0.0.1:8000

API Endpoint
GET /api/messages/history
| Parameter | Required | Description                                        |
| --------- | -------- | -------------------------------------------------- |
| roomId    | Yes      | Room identifier                                    |
| since     | No       | ISO timestamp used for pagination                  |
| limit     | No       | Number of messages to return (default=50, max=200) |

Success Response
Status:
200 OK
Example:
[
  {
    "id": "m1",
    "senderId": "user-1",
    "content": "Cargo departed Lagos port",
    "timestamp": "2026-06-11T08:00:00Z"
  },
  {
    "id": "m2",
    "senderId": "user-2",
    "content": "Estimated arrival updated",
    "timestamp": "2026-06-11T09:15:00Z"
  }
]

Error Responses
Missing roomId

Status:

400 Bad Request

Response:

{
  "error": "roomId is required"
}
Invalid limit

Status:

400 Bad Request

Response:

{
  "error": "limit must be between 1 and 200"
}
Invalid timestamp

Status:

400 Bad Request

Response:

{
  "error": "Invalid ISO timestamp"
}
Room Not Found

Status:

404 Not Found

Response:

{
  "error": "roomId not found"
}
Internal Server Error

Status:

500 Internal Server Error

Response:

{
  "error": "Internal server error"
}
Pagination Example

Request:

GET /api/messages/history?roomId=room-1&since=2026-06-11T08:30:00Z&limit=2

Response:

[
  {
    "id": "m2",
    "senderId": "user-2",
    "content": "Estimated arrival updated",
    "timestamp": "2026-06-11T09:15:00Z"
  },
  {
    "id": "m3",
    "senderId": "user-1",
    "content": "Customs clearance completed",
    "timestamp": "2026-06-11T10:45:00Z"
  }
]
Design Decisions
Django REST Framework was used because it provides a clean and maintainable structure for REST APIs.
Mock data is stored in memory to satisfy the requirement of avoiding a database.
Validation is performed before processing requests.
Messages are sorted in ascending timestamp order before being returned.
Pagination is implemented using the since timestamp and limit parameter.
Author

Raphael Egbune


---

# Evidence That the API Works

Include these curl commands in the README or submission.

## 1. Fetch Room History

```bash
curl "http://127.0.0.1:8000/api/messages/history?roomId=room-1"

Expected Output:

[
  {
    "id": "m1",
    "senderId": "user-1",
    "content": "Cargo departed Lagos port",
    "timestamp": "2026-06-11T08:00:00Z"
  },
  {
    "id": "m2",
    "senderId": "user-2",
    "content": "Estimated arrival updated",
    "timestamp": "2026-06-11T09:15:00Z"
  },
  {
    "id": "m3",
    "senderId": "user-1",
    "content": "Customs clearance completed",
    "timestamp": "2026-06-11T10:45:00Z"
  }
]
2. Pagination
curl "http://127.0.0.1:8000/api/messages/history?roomId=room-1&since=2026-06-11T08:30:00Z&limit=2"

Expected Output:

[
  {
    "id": "m2",
    "senderId": "user-2",
    "content": "Estimated arrival updated",
    "timestamp": "2026-06-11T09:15:00Z"
  },
  {
    "id": "m3",
    "senderId": "user-1",
    "content": "Customs clearance completed",
    "timestamp": "2026-06-11T10:45:00Z"
  }
]
3. Missing roomId
curl "http://127.0.0.1:8000/api/messages/history"

Expected Output:

{
  "error": "roomId is required"
}

Status:

400 Bad Request
4. Room Not Found
curl "http://127.0.0.1:8000/api/messages/history?roomId=room-99"

Expected Output:

{
  "error": "roomId not found"
}

Status:

404 Not Found