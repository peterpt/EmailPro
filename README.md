# 🦅 Email Pro: The "Paranoid" Email Client
> *Built with Python, Cryptography, and Paranoia.*

**Email Pro** is not a standard email client. It is a communications terminal designed for privacy, anonymity, and digital forensics. It was built from scratch (~1600 lines of code) to offer features that big tech providers (Outlook, Gmail) typically block or hide from you.

## 🚀 Key Features

### 👻 Identity & Anonymity
*   **Burner Mail Integration:** Generate disposable email addresses instantly to sign up for shady sites.
*   **Ghost ID Generator:** One-click generation of fake personas (Name, User, Password) to go with your burner email.
*   **Proxy/Tor Support:** Native SOCKS5 tunneling for all connections.

### 🕵️‍♂️ Forensics & Security
*   **Identity Profiler:** Analyze senders to see if they are real people, bots, or spoofed domains (MX Records & Gravatar checks).
*   **Link Hunter:** Extracts all links from an email and scans them for redirects/trackers *without* opening the browser.
*   **Header Analysis:** "Forensic Scan" scores emails based on routing data, detecting potential spoofing or proxy usage.

### ⚔️ Digital Warfare
*   **🦎 AI Camouflage:** "Poisons" your text with invisible characters. To a human, it looks normal. To an AI or keyword scanner, it is unreadable gibberish.
*   **🖼️ Image Injector (Steganography):** Hide secret text messages *inside* image attachments. Only another Email Pro user can scan and read them.
*   **PGP Encryption:** Native support for PGP encrypting/decrypting messages.

### 🛡️ Core Functions
*   **Local AES-256 Vault:** All credentials and cache are stored encrypted on your local disk.
*   **"Safe View":** Sandbox mode to view HTML emails without loading tracking pixels.
*   **Multi-Profile:** Manage unlimited accounts (Gmail, Outlook, Custom SMTP).

## 🛠️ Installation & Requirements

1. **Clone the repo:**
   ```bash
   git clone https://github.com/peterpt/EmailPro.git

  

    Install Dependencies:
    This app avoids heavy frameworks, but requires a few security libs:
    code Bash

    
pip install -r requests.txt

 apt install python3-tk 

Run:
code Bash

        
    python3 EmailPro.py

      

⚠️ Disclaimer

This tool is for educational and privacy-protection purposes. Use the forensic and anonymity tools responsibly.
