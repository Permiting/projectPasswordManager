# ✨🔒 Encrypted Password Manager 🔒✨

> **Secure. Obfuscated. Elegant.**

Welcome to the **Encrypted Password Manager** – a unique, encrypted web application designed to keep your passwords safe while maintaining a sleek and modern user experience. This project leverages advanced obfuscation techniques alongside robust client‐side encryption, ensuring that your sensitive data remains private and secure.


----



## 🎯 Overview

- **Security First:**  
  All sensitive data is encrypted on the client side and only decrypted under proper authentication.

- **Obfuscated JavaScript:**  
  The critical parts of the front‑end logic (such as theme toggling, encryption routines, and form handling) are obfuscated using Base64 encoding. This adds an extra layer of obscurity to deter casual snooping.

- **Dynamic & Responsive:**  
  The application smartly waits for the DOM to be fully loaded before executing the code via:
  ```javascript
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runMyCode);
  } else {
    runMyCode();
  }
