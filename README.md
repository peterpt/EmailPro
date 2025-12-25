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

### 🚨 The Red Protocol (Emergency Data Wipe)

CorreioPro Ultimate includes a built-in "Panic Button" designed for hostile environments or emergency hardware disposal. Located in the Profile Manager, this feature performs a destructive sanitation of the local environment.

How it works:

    Secure Overwrite: The app calculates the exact size of your sensitive files (secret.key, profiles.json, pgp_keys.json, email_cache.json).

    Shredding: It overwrites the file content on the disk with cryptographically strong random noise (os.urandom), making forensic recovery impossible.

    Deletion: It unlinks (deletes) the files from the file system.

    Termination: The application process kills itself immediately.

⚠️ WARNING: This action is IRREVERSIBLE.

    What is gone: All local passwords, PGP keys, contacts, and offline email cache. You will lose access to any PGP-encrypted emails if you did not backup your key elsewhere.

    What remains: This does not delete emails from the remote server (e.g., Gmail/Outlook). It only sanitizes the local device.

## Pictures 
# MAin App
<img width="1024" height="741" alt="image" src="https://github.com/user-attachments/assets/ccb7be80-2b4f-40ab-913c-82405144484b" />
# Profile Configuration
<img width="608" height="628" alt="image" src="https://github.com/user-attachments/assets/df18d569-cae7-4864-b952-ea39bd80251f" />
# Main Email App
<img width="1024" height="741" alt="image" src="https://github.com/user-attachments/assets/fc5e79d4-6948-4c03-82a6-9dff19bfb0b8" />
# PGP Key Generation
<img width="608" height="528" alt="image" src="https://github.com/user-attachments/assets/d948c513-127a-4dc0-bda7-99f80e679472" />
# Forensic
<img width="558" height="578" alt="image" src="https://github.com/user-attachments/assets/c2a35169-7257-4c44-9b36-c34b593a6b6d" />
# Temporary Email Discarter
<img width="808" height="578" alt="image" src="https://github.com/user-attachments/assets/cb306bcc-00e4-4a28-99eb-2567bf55e05d" />
# Ghost ID generator
<img width="308" height="248" alt="image" src="https://github.com/user-attachments/assets/2583eb2c-0427-4b13-ad87-51841e02bdc4" />
# Compose Email with multiples options
<img width="1024" height="741" alt="image" src="https://github.com/user-attachments/assets/d08cf736-640c-4016-a480-a21dcd0dbd21" />


## 🛠️ Installation & Requirements

1. **Clone the repo:**
   ```bash
   git clone https://github.com/peterpt/EmailPro.git

  

    Install Dependencies:
    This app avoids heavy frameworks, but requires a few security libs:
    code Bash

    
pip install -r requirements.txt

 apt install python3 python3-tk 

Run:
code Bash

        
    python3 emailpro.py

      

⚠️ Disclaimer

This tool is for educational and privacy-protection purposes. Use the forensic and anonymity tools responsibly.

# Credits
Peterpt (Idea , bug finder and testing)
Google Gemini AI (Code Generation)
Flaticon.com (Icons Inside this App)

# Others
Initially i wanted only a simple email client because the others public email cleintes available
in market were not able to connect to my email server to fetch the data , after we achieved this
 i gave Gemini permission to use its creativity on this app to make it more secure for the user ,
 and the result was this app witch i believe it is one of the best email clients i have ever seen 
 regarded to security .


