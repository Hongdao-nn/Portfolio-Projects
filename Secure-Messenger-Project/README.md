# 🔐 SECURE MESSENGER

> **End-to-End Encrypted Platform — Threat-aware Secure Messaging Simulator**

---

## 📌 Overview

**Secure Messenger** is a web application simulating an end-to-end encrypted (E2EE) messaging system, built to demonstrate modern cryptographic concepts and real-world attack scenarios from a hacker's perspective.

The project combines an intuitive chat interface with a technical control panel (Ratchet Monitor), allowing users to observe the entire encryption pipeline — from Diffie-Hellman key exchange, AES-256 encryption and SHA-256 integrity checks, all the way to XSS attack simulation and account takeover.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔑 **Diffie-Hellman Handshake** | Secret key exchange between Alice and Bob (DH-256) |
| 🔒 **AES-256 Encryption** | Message encryption using industry-standard AES-256 |
| 🗝️ **Vigenère Cipher** | Alternative encryption mode using the Vigenère cipher |
| ✅ **SHA-256 Integrity** | Payload hashing to verify message integrity |
| ⚙️ **Ratchet Monitor** | Real-time visualization of the Double Ratchet mechanism |
| 🐛 **Hacker Console** | XSS attack simulation and session hijacking demo |
| 💬 **3-Column Chat UI** | Side-by-side view: Alice — Ratchet Monitor — Bob |
| 👥 **Friends List** | Encrypted messaging with 8 contacts, including image support |
| 🖼️ **Image Sharing** | Upload and send images within any conversation |
| 👤 **Account Management** | Edit name, email, avatar; view stats and achievement badges |
| 🌐 **Bilingual (VI / EN)** | Full UI language toggle between Vietnamese and English |
| 🌗 **Light / Dark Theme** | Instant theme switching |
| 🔔 **Seen & Typing Indicator** | "Seen" receipts and animated typing bubbles |
| 🎬 **Splash Screen** | Cinematic boot sequence with code rain effect |
| 🌊 **Parallax Background** | 3D-layered background that follows the mouse cursor |
| 🔥 **Firebase Realtime DB** | Live message sync via Firebase Realtime Database |

---

## 🔐 Cryptographic Architecture — Data Flow

Every message in Secure Messenger passes through a strict cryptographic pipeline before it reaches the recipient:

1. **Sender** types a message or selects an image.
2. **Diffie-Hellman Ratchet** exchanges public keys and rotates the root key on each send (G=5, P=23).
3. **Encryption** is applied using AES-256 or Vigenère, depending on the user's choice.
4. **SHA-256** hashes the payload to ensure data integrity.
5. **Firebase** stores the encrypted payload in the Realtime Database.
6. **Receiver** fetches the ciphertext, decrypts it, and verifies the hash before displaying the original message.

![Crypto Data Flow Diagram](assets/crypto_data_flow_diagram.svg)

> *Figure: Full processing pipeline from sender → DH Ratchet → encryption → Firebase → decryption → receiver.*

---

## 🕵️ Attack Simulation — The Hacker's View (Eve)

One of Secure Messenger's standout features is the **Hacker Console** — which lets users observe and understand how an attacker (Eve) can exploit security weaknesses in a typical messaging application.

### Eve's Attack Chain

| Step | Technique | Description |
|---|---|---|
| 1 | **Phishing Link** | Eve crafts a fake link and tricks Alice into clicking it |
| 2 | **XSS Injection** | `triggerXSSAttack()` injects a fake message bubble into Alice's chat view |
| 3 | **Fake UI Hijack** | Eve takes over the screen — a dark overlay and fake cursor appear, simulating the attacker's actions |
| 4 | **Fake Password Prompt** | `xssModal` displays a spoofed "security verification" dialog, prompting Alice to re-enter her password |
| 5 | **Account Takeover** | `executeAccountTakeover()` captures the password and simulates full account compromise |
| 6 | **Matrix Terminal** | A cyberpunk-style terminal appears, dramatizing the "hack" for the viewer |

> 💡 **Educational purpose:** The entire Eve scenario runs safely in a sandboxed environment — no real data is ever stolen. The goal is to help users recognize and guard against social engineering and XSS attacks in the real world.

![Eve Hack Attack Flow](assets/eve_hack_attack_flow.svg)

> *Figure: Attack chain from phishing → XSS injection → fake prompt → account takeover, color-coded by Eve's actions (orange), Alice's reactions (purple), and compromised system states (red).*

---

## 🧭 Interactive Tutorial

The application includes a built-in **interactive guided tour** (powered by [Driver.js](https://driverjs.com/)) to help users explore all features in just a few steps. Click the ❓ button in the navigation bar to launch the tour.

> ⚠️ **Important note:**  
> The tutorial in this version has been **independently revised and improved** compared to the original group submission. Changes focus on smoother flow, better user guidance, and more detailed step-by-step explanations.
>
> Additional independent improvements made to this codebase include:
> - **Clean Architecture refactor:** Fully separated thousands of lines of mixed JavaScript and CSS from the original `index.html` into dedicated module files (`js/script.js` and `css/style.css`), bringing the project to industry standards.
> - **Bug fixes & optimization:** Resolved duplicate functions, variable overwrites, and CSS conflicts carried over from the original group version.
> - **Tutorial Tour upgrade:** Reworked the `driver.js` interaction flow for a smoother, more polished experience.

---

## 🛠️ Tech Stack

- **HTML5 / CSS3 / JavaScript (ES Modules)**
- **CryptoJS 4.1.1** — AES-256 & SHA-256 encryption
- **Firebase Realtime Database** — Live message sync
- **Driver.js 1.0.1** — Interactive guided tour
- **Font Awesome 6** — Icon library
- **Google Fonts** — Quicksand, JetBrains Mono

---

## 🚀 Getting Started

1. Clone or download the project.
2. Make sure you have an active Internet connection (required for Firebase + CDN libraries).
3. Open `index.html` in a modern browser (Chrome, Edge, or Firefox).
4. Wait for the splash screen to finish loading (~3.6 seconds), then start exploring.

> No additional installation required — all libraries are loaded via CDN.

---

## 📁 Project Structure

```
secure-messenger/
├── index.html        # Main UI — full page structure
├── css/
│   └── style.css     # All styles (theme, animations, layout)
└── js/
    └── script.js     # Encryption logic, Firebase, UI, Tour, i18n
```

---

## 👥 Project Team

| # | Name | Role | Responsibilities |
|---|---|---|---|
| 1 | **Đinh Kỳ Vĩ** | 🏆 Team Leader | Proposed the concept and built the core processing pipeline; Developed the demo UI; Optimized the encryption algorithms |
| 2 | **Nguyễn Ngọc Hồng Đào** | 💻 Member | Refined the user interface (UI/UX); Researched and integrated features; Managed display content |
| 3 | **Nguyễn Duy Bảo Trân** | 💻 Member | Built the technical proof-of-concept (PoC) in Java; Programmed extended features; Developed Web Modules |
| 4 | **Nguyễn Bùi Minh Hằng** | 🛡️ Member | Conducted penetration testing (Pen-test); Simulated attack scenarios to validate system security |
| 5 | **Nguyễn Thị Sang** | 🤝 Member | Participated |
| 6 | **Đặng Hồng Nguyệt** | 🤝 Member | Participated |
| 7 | **Hoàng Thị Kim Ngân** | 🤝 Member | Participated |
| 8 | **Nguyễn Thanh Huyền** | 🤝 Member | Participated |
| 9 | **Nguyễn Phan Thanh Lịch** | 🤝 Member | Participated |

---

## 📄 License

This project was developed for academic and information security research purposes.  
© 2025 Secure Messenger Team. All rights reserved.
