# Winky AI 🤖
**An Upgraded Winky Talk Project** *Developed by Yuvraj Chandra (14 years old)* *Student at Police DAV School*

---

## 🌟 Overview
Winky AI is a powerful, locally-hosted assistant designed for seamless automation and interaction. Formerly known as Jarvis, this upgraded version features improved stability and a refined user interface.

## 🛠️ Prerequisites
Before installation, ensure your system has the following tools:

### 1. MSVC Build Tools
Required for compiling C++ components.
* [Download Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)
* **Installation Step:** During setup, ensure you check the box for **"Desktop development with C++"**.

### 2. Python Environment
* **Recommended Versions:** Python 3.11 or 3.12 (Stable).
* **Note:** If using Python 3.13 and you encounter errors, please downgrade to 3.12.
* [Download Python](https://www.python.org/downloads/windows/)

### 3. Node.js
* **Version:** v20.19.6
* [Download Node.js](https://nodejs.org/en/download)

---

## 🚀 Installation & Setup

1. **Extract the Project:** Move the downloaded folder to your **Desktop**.
2. **Rename the Folder:** Ensure the folder is named `agent-starter-react`. THIS IS THE FRONTEND WEB AND STARTER
3. **Open Terminal:** Launch the Command Prompt (CMD).
4. **Execute Commands:**

```cmd
cd upgraded-winkytalk/agent-starter-react
npm install -g pnpm
pnpm install
pnpm dev

And that your WinkyAi running on your PC.
# 1. Delete the old Git history
rm -rf .git

# 2. Configure your identity (if you haven't yet)
git config --global user.name "Yuvraj Chandra"
git config --global user.email "spitfire1official@gmail.com"

# 3. Initialize your new repository
git init

# 4. Add all your files
git add .

# 5. Create your first commit
git commit -m "Initial release of Winky AI by Yuvraj Chandra"

# 6. Link to your GitHub (Create a new empty repo on GitHub first)
git remote add origin https://github.com/Winky-x/Upgraded-WinkyTalk.git
git branch -M main
git push -u origin main