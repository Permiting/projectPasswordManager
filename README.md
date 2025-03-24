# Encrypted Password Manager

**Welcome to the Encrypted Password Manager!**  
This project is a secure, encrypted password management web application designed to help you safely store, retrieve, and manage your credentials. With robust encryption and obfuscation techniques, your data is obscured from casual prying eyes while maintaining a user-friendly experience.


----



## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [Setup & Usage](#setup--usage)
5. [Obfuscation & Encryption Process](#obfuscation--encryption-process)
6. [Customization & Deployment](#customization--deployment)
7. [License & Credits](#license--credits)


----



## Overview

The **Encrypted Password Manager** is built to handle your sensitive credentials securely.  
Key points include:

- **Encrypted Data Handling:**  
  User passwords and credentials are encrypted, ensuring that only authorized users can decrypt and use the stored information.

- **Obfuscated JavaScript Logic:**  
  Critical front‑end logic—such as theme toggling and password management—is obfuscated (via Base64 encoding and dynamic evaluation) to discourage casual code inspection.

- **Dynamic DOM Handling:**  
  The application efficiently manages the Document Object Model (DOM) using a DOM-ready check:
  
  ```javascript
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runMyCode);
  } else {
    runMyCode();
  }
