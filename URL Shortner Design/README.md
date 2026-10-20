# Simple URL Shortener 🚀

A lightweight, high-performance URL shortener prototype built with **Python (Flask)** and **SQLite**, designed around core distributed system principles like **Base62 encoding** and **HTTP 302 redirection tracking**.

---

## 🏗️ System Architecture & Design Choices

### 1. Core Flows
* **Write Path (Shortening):** A user submits a long URL $\rightarrow$ The database assigns an auto-incrementing ID $\rightarrow$ The ID is converted into a compact **Base62 string** (`a-z`, `A-Z`, `0-9`) $\rightarrow$ Saved to SQLite.
* **Read Path (Redirection):** A user visits the short link $\rightarrow$ The server decodes the Base62 key back to its numeric ID $\rightarrow$ Queries the database $\rightarrow$ Issues an **HTTP 302 Temporary Redirect** to the destination URL.

### 2. Why Base62 Encoding?
Instead of using cryptographic hashes (like MD5 or SHA-256) which can cause collisions and require costly collision-resolution loops, this system uses a **Base62 encoder**. 
* **Zero Collisions:** Every generated key maps directly to a unique integer ID.
* **Compact Size:** Base62 allows us to store billions of unique links using very short character strings.

### 3. Why HTTP 302 instead of HTTP 301?
* **301 (Moved Permanently):** Browsers aggressively cache 301 redirects, meaning subsequent clicks bypass our servers entirely. While faster, **we lose click analytics**.
* **302 (Found / Temporary):** Forces the browser to ping our server on every single click, enabling real-time analytics, click counters, and traffic tracking.

---

## 🛠️ Project Structure
```text
simple-url-shortener/
│
├── app.py             # Main Flask application (Routes & Base62 logic)
├── requirements.txt   # Project dependencies
└── README.md          # System design & documentation