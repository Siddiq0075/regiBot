# 🎟️ SWAP 2K25 Registration & Quiz Bot

A full-featured **Discord-based event management system** designed for handling participant registrations, secure entry validation, and quiz data management using MongoDB.

---

## 🚀 Project Overview

This bot is built to automate the entire workflow of a college event:

- 📝 Participant Registration
- 🎫 Ticket Generation (ID + Password)
- 📩 Automated DM Confirmation
- 🛠️ Admin Management Commands
- 📊 Data Export (Excel)
- 🧠 Quiz System Backend (MongoDB)

The system ensures **accuracy, scalability, and security** during live event operations.

---

## ⚙️ Tech Stack

- **Language:** Python
- **Framework:** discord.py
- **Database:** MongoDB
- **Libraries:**
  - `pymongo`
  - `openpyxl`
  - `discord`
  - `asyncio`

---

## 📁 Project Structure

```
regiBot/
│
├── bot.py
├── config.py
├── .env
│
├── database/
│   └── db_client.py
│
├── cogs/
│   ├── registration_commands.py
│   ├── admin_commands.py
│   └── setup.py
│
└── exports/
```

---

## 🗄️ Database Structure (MongoDB)

Database: `swapquiz`

Collections:

```
swapquiz
 ├── users
 ├── counter
 ├── questions
 ├── answers
 ├── permissions
 ├── rules
 ├── settings
 └── timers
```

---

## 👤 User Data Schema

```json
{
  "discord_id": 123456789,
  "name": "John Doe",
  "partner_name": "Jane",
  "college": "ABC College",
  "department": "CSE",
  "mobile": "9876543210",
  "reg_number": "SWAP001",
  "password": "57JMC"
}
```

---

## 🔐 Registration System

Each participant receives:

- 🆔 **Registration ID:** `SWAP001`
- 🔑 **Password:** `57JMC`

### Why this system?

- Sequential ID → easy tracking
- Random password → prevents impersonation
- DM delivery → secure communication

---

## 🤖 Bot Commands

### 🟢 Public Commands

| Command     | Description                    |
| ----------- | ------------------------------ |
| `/register` | Register for the event         |
| `/view`     | View your registration details |
| `/resend`   | Resend ticket to DM            |

---

### 🔴 Admin Commands

| Command   | Description                      |
| --------- | -------------------------------- |
| `/lookup` | Search participant by ID or user |
| `/list`   | List all registered participants |
| `/clear`  | Clear all registrations          |
| `/export` | Export data to Excel             |

---

## 📩 Ticket System

After registration, users receive a DM:

```
🎟️ SWAP 2K25 Registration Ticket

SWAP ID   : SWAP021
PASSWORD  : 57JMC
COLLEGE   : XYZ College
```

---

## 📊 Excel Export

Admin can export all data into an `.xlsx` file using:

```
/export
```

Used for:

- Offline backup
- Entry desk verification
- Event reporting

---

## 🔄 Registration Flow

1. User runs `/register`
2. Bot checks existing user
3. Generates:
   - Unique ID (`SWAPxxx`)
   - Random password (`xxJMC`)

4. Stores data in MongoDB
5. Sends DM ticket
6. Logs entry in admin channel

---

## 🛡️ Security Design

- Prevents duplicate registration
- Unique password per user
- No direct DB exposure
- Admin-only sensitive commands
- Ephemeral responses for privacy

---

## 📌 Key Features

✔ Clean modular architecture (Cogs)
✔ Centralized DB handling
✔ Async-safe operations
✔ Professional embed UI
✔ Event-ready logging system
✔ Scalable quiz backend

---

## 🧪 Setup Instructions

### 1. Clone the repository

```bash
git clone <repo-url>
cd regiBot
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup `.env`

```
DISCORD_TOKEN=your_bot_token
MONGO_URI=mongodb://localhost:27017
LOG_CHANNEL_ID=your_channel_id
```

---

### 4. Run MongoDB

Make sure MongoDB is running locally.

---

### 5. Start the bot

```bash
python bot.py
```

---

## 📈 Future Enhancements

- 🌐 Web-based quiz interface (React)
- ⏱️ Timed quiz rounds
- 📊 Leaderboard system
- 🔐 Entry verification system
- 📱 Admin dashboard

---

## 🎯 Conclusion

This project is not just a bot — it is a **complete event management system** that handles:

- Registration
- Validation
- Data storage
- Admin control
- Reporting

Built with a focus on **real-world event challenges**, ensuring smooth and error-free execution.

---

## 👨‍💻 Author

**Mohamed Siddiq**
SWAP 2K25 Project Developer

---
