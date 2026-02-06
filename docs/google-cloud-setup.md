# Google Cloud Service Account Setup Guide

**Complete guide to setting up a Google Cloud service account for Hancock**

Setup time: **10-15 minutes** (one-time)

---

## What You'll Need

✅ Google Workspace admin access
✅ Access to [Google Cloud Console](https://console.cloud.google.com/)
✅ 10-15 minutes

---

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top
3. Click "**New Project**"
4. Name it "**Hancock Signatures**" (or your preferred name)
5. Click "**Create**"
6. Wait for the project to be created (usually a few seconds)

---

### 2. Enable Required APIs

1. In your new project, go to **APIs & Services** → **Library**

2. Search for "**Admin SDK API**"
   - Click on it
   - Click "**Enable**"
   - Wait for it to enable

3. Search for "**Gmail API**"
   - Click on it
   - Click "**Enable**"
   - Wait for it to enable

---

### 3. Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**

2. Click "**+ CREATE SERVICE ACCOUNT**" at the top

3. Fill in the details:
   - **Name**: `hancock-service-account`
   - **Description**: `Service account for Hancock signature deployment`
   - Click "**Create and Continue**"

4. **Grant access** (optional):
   - Skip this step (no roles needed)
   - Click "**Continue**"

5. **Grant users access** (optional):
   - Skip this step
   - Click "**Done**"

---

### 4. Enable Domain-Wide Delegation

1. Click on the service account you just created

2. Go to the "**Details**" tab

3. Scroll down to "**Advanced settings**"

4. Find "**Domain-wide delegation**"
   - Click "**Enable domain-wide delegation**"
   - **Product name for consent screen**: `Hancock`
   - Click "**Save**"

5. **Copy the Client ID** (you'll need this in step 6)
   - It looks like: `1234567890-abc123def456.apps.googleusercontent.com`
   - Save it somewhere temporarily

---

### 5. Download Service Account Key

1. Go to the "**Keys**" tab

2. Click "**Add Key**" → "**Create new key**"

3. Choose "**JSON**" format

4. Click "**Create**"
   - A JSON file will download automatically
   - This is your service account key

5. **Important**: Rename the file to `service-account.json` and save it somewhere secure
   - Desktop, Documents, or a dedicated folder for credentials
   - Remember where you put it - you'll need the path later

---

### 6. Authorize in Google Workspace Admin Console

This step connects your service account to your Google Workspace domain.

1. Go to [Google Workspace Admin Console](https://admin.google.com/)

2. Navigate to: **Security** → **API Controls** → **Domain-wide Delegation**
   - Or use this direct link (if you're a super admin):
   - https://admin.google.com/ac/owl/domainwidedelegation

3. Click "**Add new**"

4. Fill in the form:
   - **Client ID**: Paste the Client ID from Step 4.5
   - **OAuth Scopes**: Copy and paste these two scopes exactly:
     ```
     https://www.googleapis.com/auth/admin.directory.user.readonly,https://www.googleapis.com/auth/gmail.settings.basic
     ```

5. Click "**Authorize**"

---

### 7. Run Hancock Init

Now you're ready to configure Hancock!

```bash
hancock init
```

When prompted:
- **Do you have a service account?** → Yes
- **Where is it?** → Enter the full path to your `service-account.json` file
- **Admin email?** → Enter your Google Workspace admin email

Hancock will validate your credentials and save the configuration.

---

## 🎉 You're Done!

Your Google Cloud service account is now set up and ready to deploy signatures.

**Next steps:**
1. Create a folder with signature HTML files
2. Name files to match users (e.g., `john.smith.html`)
3. Run: `hancock deploy signatures/`

---

## Troubleshooting

### "Authentication failed"

**Check:**
- Domain-wide delegation is enabled (Step 4)
- OAuth scopes are correct (Step 6)
- Admin email is a super admin
- Service account JSON file path is correct

**Solution:**
```bash
hancock init  # Reconfigure
```

### "Access Denied" during deployment

**Check:**
- You authorized the correct Client ID in Workspace Admin
- The OAuth scopes include both:
  - `admin.directory.user.readonly`
  - `gmail.settings.basic`

**Solution:**
- Go back to Step 6 and verify the scopes
- Delete and re-add the domain-wide delegation entry

### Can't find "Domain-wide Delegation"

**Check:**
- You're logged in as a super admin (not just a regular admin)
- You're in the correct Google Workspace account

**Solution:**
- Try this direct link: https://admin.google.com/ac/owl/domainwidedelegation
- Contact your Google Workspace super admin

### Service account file not found

**Check:**
- The file path is correct
- The file hasn't been moved or renamed
- You have read permissions for the file

**Solution:**
- Use the full absolute path (e.g., `/Users/yourname/Desktop/service-account.json`)
- Or drag the file into the terminal to paste the path

---

## Security Best Practices

✅ **Keep your service account secure:**
- Store `service-account.json` in a secure location
- Don't commit it to version control (git)
- Don't share it with others
- Set appropriate file permissions (read-only for your user)

✅ **Limit access:**
- Only authorized admins should have the service account key
- Use Hancock on trusted computers only
- Consider storing the key in an encrypted folder

✅ **Monitor usage:**
- Review Google Workspace audit logs regularly
- Check for unexpected signature deployments
- Revoke the service account if compromised

---

## What These Permissions Allow

The service account can:
- ✅ Read user directory (names, emails)
- ✅ Update Gmail signature settings

The service account **cannot**:
- ❌ Read emails
- ❌ Send emails
- ❌ Delete users
- ❌ Modify other settings

---

## Need Help?

- **Hancock Documentation**: [README.md](../README.md)
- **Google Cloud Docs**: https://cloud.google.com/iam/docs/service-accounts
- **Google Workspace Docs**: https://support.google.com/a/answer/162106

---

**Ready to deploy signatures?** Run `hancock init` to get started! 🚀
