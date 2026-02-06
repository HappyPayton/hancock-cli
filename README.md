# Hancock

**Gmail signature deployment CLI for Google Workspace**

Deploy signatures to your entire Google Workspace from the terminal. Simple, fast, and secure.

```bash
pip install hancock-cli
hancock init
hancock deploy signatures/
```

---

## ✨ Features

- **🚀 Simple Setup** - One command to configure, works with Google service accounts
- **🎯 Smart Matching** - Automatically matches signature files to users by name or email
- **📊 Beautiful UI** - Colored terminal output with progress bars and clear status
- **✅ Validation** - Checks file sizes, formats, and matching before deployment
- **🔒 Secure** - Your credentials stay on your machine, no data sent elsewhere
- **⚡ Fast** - Deploy to entire organization in minutes
- **💻 Terminal Native** - Works great standalone or with Claude Code

---

## 🚀 Quick Start

### Install

```bash
pip install hancock-cli
```

### Setup (5-15 minutes, one time only)

```bash
hancock init
```

This walks you through:
1. Locating your Google Cloud service account JSON key
2. Entering your Google Workspace admin email
3. Validating credentials

### Deploy

Create a folder with HTML signature files named to match your users:

```
signatures/
├── john.smith.html
├── jane-doe.html
└── bob.jones.html
```

Then deploy:

```bash
hancock deploy signatures/
```

---

## 📖 Commands

### `hancock init`
Interactive setup - configure credentials and validate access.

### `hancock deploy <folder>`
Deploy signatures from a folder to matched users.

**Options:**
- `--dry-run` - Show what would be deployed without actually deploying

**Example:**
```bash
hancock deploy signatures/
hancock deploy ~/my-signatures/ --dry-run
```

### `hancock preview <email>`
Preview the current signature for a user.

**Example:**
```bash
hancock preview john@company.com
```

### `hancock validate <folder>`
Validate signature files without deploying.

**Example:**
```bash
hancock validate signatures/
```

### `hancock config`
Show current configuration and status.

---

## 🎯 Creating Signatures

### File Naming

Name your HTML files to match users:
- `john.smith.html` → `john.smith@company.com`
- `jane-doe.html` → `jane.doe@company.com`
- `bobsmith.html` → `bob.smith@company.com`

Hancock handles:
- Dots, dashes, underscores
- Different name orders
- Case insensitive matching
- "sig" or "signature" suffixes

### Basic Template

```html
<!DOCTYPE html>
<html>
<body>
<table style="font-family: Arial, sans-serif; font-size: 12px;">
  <tr>
    <td>
      <p style="margin: 0; font-weight: bold;">John Smith</p>
      <p style="margin: 5px 0; color: #666;">Software Engineer</p>
      <p style="margin: 0;">
        <a href="mailto:john@company.com">john@company.com</a>
      </p>
    </td>
  </tr>
</table>
</body>
</html>
```

### Images (No External Hosting)

Use base64 encoding to embed images directly:

```bash
# Convert image to base64
base64 -i photo.jpg | tr -d '\n'
```

Then in your HTML:
```html
<img src="data:image/jpeg;base64,YOUR_BASE64_HERE"
     style="width: 80px; height: 80px;" />
```

### Size Limit

Gmail signatures must be under **10KB**. Hancock validates this automatically.

**Tips to reduce size:**
- Optimize images before base64 encoding
- Use JPEG instead of PNG for photos
- Keep HTML simple and minimal

---

## 🔐 Service Account Setup

Hancock uses a Google Cloud service account with domain-wide delegation. This is the same approach used by many enterprise tools.

### First-Time Setup (15 minutes)

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**

2. **Create a new project** (or select existing)

3. **Enable APIs:**
   - Admin SDK API
   - Gmail API

4. **Create Service Account:**
   - Go to: IAM & Admin → Service Accounts
   - Create service account
   - Download JSON key

5. **Enable Domain-Wide Delegation:**
   - Edit service account
   - Enable domain-wide delegation
   - Note the Client ID

6. **Authorize in Google Workspace:**
   - Go to [Google Workspace Admin Console](https://admin.google.com/)
   - Security → API Controls → Domain-wide Delegation
   - Add new with Client ID and scopes:
     ```
     https://www.googleapis.com/auth/admin.directory.user.readonly
     https://www.googleapis.com/auth/gmail.settings.basic
     ```

7. **Run Hancock init:**
   ```bash
   hancock init
   ```

### Security

✅ **Hancock is secure by design:**
- Your credentials stay on your machine
- No data sent to third parties
- Standard Google OAuth 2.0
- Open source - audit the code

✅ **Best practices:**
- Keep your service account JSON secure
- Don't commit credentials to git
- Review Google Workspace audit logs

---

## 💡 Use Cases

- **Company rebrand** - Update all signatures at once
- **New hires** - Standardize onboarding signatures
- **Legal compliance** - Ensure signatures meet requirements
- **Marketing campaigns** - Add promotional content
- **Department changes** - Update titles and departments

---

## ✨ Using with Claude Code

Hancock works great in [Claude Code](https://claude.com/claude-code)!

**Claude can help you:**
- Walk through the Google Cloud setup
- Find your service account JSON file
- Troubleshoot configuration issues
- Create signature HTML files
- Validate your setup

Just run `hancock init` in the Claude Code terminal and Claude will guide you through!

---

## 🛠 Troubleshooting

### "Hancock is not configured yet"
→ Run `hancock init` to set up credentials

### "Authentication failed"
→ Verify domain-wide delegation is enabled
→ Check OAuth scopes in Workspace Admin Console
→ Confirm admin email is correct

### "No signatures matched to users"
→ Check filename format (use email prefix or full name)
→ Verify users exist in Google Workspace
→ Try different separator styles (dots vs dashes)

### "File size exceeds limit"
→ Signatures must be under 10KB
→ Reduce image dimensions
→ Optimize images before base64 encoding

---

## 📦 Installation

### From PyPI (recommended)

```bash
pip install hancock-cli
```

### From source

```bash
git clone https://github.com/HappyPayton/hancock-cli.git
cd hancock-cli
pip install -e .
```

### Requirements

- Python 3.7 or higher
- Google Workspace admin access
- Google Cloud service account with domain-wide delegation

---

## 🔄 Uninstall

```bash
pip uninstall hancock-cli
```

Your configuration file (`~/.hancock/config.yaml`) will remain. Delete it manually if desired.

---

## 📝 License

MIT License - Free to use and distribute

---

## 🌟 Why Hancock?

**Simple**
- One install command
- Interactive setup
- Terminal-native workflow

**Powerful**
- Deploy to entire organization
- Smart filename matching
- Real-time progress tracking

**Secure**
- Standard Google OAuth
- Credentials stay local
- Open source

---

## 🚀 Get Started

```bash
pip install hancock-cli
hancock init
```

**Questions?** File an issue on [GitHub](https://github.com/HappyPayton/hancock-cli/issues)

---

Made with ❤️ for Google Workspace administrators
