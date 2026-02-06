# 🚀 Hancock Launch Checklist

Everything is ready to launch! Follow these steps to make Hancock public.

---

## ✅ What's Already Done

- [x] Hancock CLI fully built and tested
- [x] Beautiful terminal UI with Rich
- [x] Smart file-to-user matching
- [x] Deployment workflow working (tested with spacecampers.xyz)
- [x] Website created (terminal-themed landing page)
- [x] Documentation complete (README, CONTRIBUTING, etc.)
- [x] GitHub Actions workflows configured
- [x] PyPI package structure ready
- [x] MIT License

---

## 📋 Launch Steps (Do These Now)

### 1. Create GitHub Repository (5 minutes)

```bash
# Go to: https://github.com/new
# Repository name: hancock-cli
# Description: Gmail signature deployment CLI for Google Workspace
# Public: ✓
# Don't initialize with README

# Then push your code:
cd /Users/paytonkleinsasser/Desktop/hancock-cli

git init
git add .
git commit -m "Initial commit: Hancock v1.0.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hancock-cli.git
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### 2. Update URLs in Files (2 minutes)

After creating the repo, update these files:

**Files to update:**
- `README.md` - Line 353, 356, 357 (GitHub URLs)
- `website/index.html` - Line 281, 282 (GitHub links)
- `pyproject.toml` - Lines 29-32 (project URLs)
- `hancock/commands/init.py` - Line 62 (setup guide URL)

**Find and replace:**
```
Find: yourusername
Replace: YOUR_ACTUAL_GITHUB_USERNAME
```

Then commit:
```bash
git add .
git commit -m "Update GitHub URLs"
git push
```

### 3. Enable GitHub Pages (3 minutes)

1. Go to your repo → Settings → Pages
2. Source: "GitHub Actions"
3. Save

The website will automatically deploy! Visit it at:
- https://YOUR_USERNAME.github.io/hancock-cli/

### 4. Configure Custom Domain (5 minutes + wait time)

**A. Buy domain (if not already done):**
- Go to Namecheap, GoDaddy, or your preferred registrar
- Purchase `installhancock.com`

**B. Configure DNS:**

Add these records in your domain registrar:

```
Type    Name    Value                   TTL
----    ----    -----                   ---
A       @       185.199.108.153         Automatic
A       @       185.199.109.153         Automatic
A       @       185.199.110.153         Automatic
A       @       185.199.111.153         Automatic
CNAME   www     YOUR_USERNAME.github.io Automatic
```

**C. Enable in GitHub:**
1. Repo → Settings → Pages
2. Custom domain: `installhancock.com`
3. Save
4. Wait for DNS check (few minutes)
5. Enable "Enforce HTTPS" (might need to wait 24 hours)

**Note:** DNS takes 24-48 hours to fully propagate

### 5. Publish to PyPI (10 minutes)

**A. Create PyPI account:**
1. Go to https://pypi.org/account/register/
2. Verify email
3. Enable 2FA (recommended)

**B. Create API token:**
1. https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. "Add API token"
   - Name: `hancock-cli`
   - Scope: "Entire account"
4. Copy token (starts with `pypi-...`)

**C. Add token to GitHub:**
1. Repo → Settings → Secrets and variables → Actions
2. "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: paste your token
5. Add secret

**D. Create release:**
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Then on GitHub:
1. Releases → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Release`
4. Description: Copy from website or write launch notes
5. Publish release

GitHub Actions will automatically publish to PyPI! 🎉

### 6. Test Everything (5 minutes)

```bash
# Test PyPI install (wait a few minutes after release)
pip install hancock-cli

# Test CLI
hancock --version
hancock --help

# Test website
# Visit: https://installhancock.com (after DNS propagates)
```

---

## 🎯 Post-Launch

### Recommended Actions:

1. **Add GitHub Topics:**
   - Go to repo main page
   - Click the gear icon next to "About"
   - Add topics: `gmail`, `google-workspace`, `cli`, `python`, `signatures`, `email`

2. **Create GitHub Discussions:**
   - Settings → Features → Discussions → Enable
   - Pin a "Welcome" discussion

3. **Share the Launch:**
   - Tweet about it
   - Post on Reddit (r/Python, r/commandline)
   - Share on LinkedIn
   - Post on Hacker News

4. **Monitor:**
   - Watch GitHub Issues
   - Check PyPI download stats
   - Monitor website analytics (add Google Analytics if desired)

---

## 📊 Expected Timeline

| Step | Time | When |
|------|------|------|
| GitHub repo creation | 5 min | Now |
| Update URLs | 2 min | Now |
| Enable GitHub Pages | 3 min | Now |
| Configure domain | 5 min | Now |
| DNS propagation | 24-48 hours | Automatic |
| Publish to PyPI | 10 min | Now |
| Package available | 5 min | After release |
| Full launch complete | ~30 min + wait | Total |

---

## 🆘 Need Help?

See `DEPLOYMENT.md` for detailed instructions and troubleshooting.

---

## 🎉 Launch Announcement Template

Once everything is live, share this:

```
🚀 Launching Hancock!

Deploy Gmail signatures to your entire Google Workspace from the terminal.

✨ Features:
• One-command setup
• Smart file-to-user matching
• Beautiful terminal UI
• Secure (credentials stay local)
• Fast deployment

Install:
pip install hancock-cli

Docs:
https://installhancock.com

#Python #CLI #GoogleWorkspace #DevTools
```

---

**Ready to launch? Let's go! 🚀**
