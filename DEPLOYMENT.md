# Hancock Deployment Guide

Complete guide to publishing Hancock to PyPI and deploying the website.

---

## 1. Create GitHub Repository

### Steps:

1. Go to https://github.com/new
2. Repository name: `hancock-cli`
3. Description: `Gmail signature deployment CLI for Google Workspace`
4. Public repository
5. Don't initialize with README (we have one)
6. Create repository

### Push code to GitHub:

```bash
cd /Users/paytonkleinsasser/Desktop/hancock-cli

# Initialize git (if not already)
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Hancock v1.0.0"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/hancock-cli.git

# Push to main
git branch -M main
git push -u origin main
```

---

## 2. Deploy Website to GitHub Pages

### Method A: Automatic (GitHub Actions)

The workflow is already set up! Just:

1. Go to repo Settings → Pages
2. Source: GitHub Actions
3. The website will auto-deploy on every push to `main`

### Method B: Manual

```bash
# From project root
cd website
git init
git add .
git commit -m "Deploy website"
git branch -M gh-pages
git remote add origin https://github.com/YOUR_USERNAME/hancock-cli.git
git push -u origin gh-pages
```

Then:
1. Go to Settings → Pages
2. Source: Deploy from branch → `gh-pages` → `/ (root)`

---

## 3. Configure Custom Domain (installhancock.com)

### A. DNS Configuration

In your domain registrar (Namecheap, GoDaddy, etc.), add these records:

```
Type    Name    Value                   TTL
----    ----    -----                   ---
A       @       185.199.108.153         Automatic
A       @       185.199.109.153         Automatic
A       @       185.199.110.153         Automatic
A       @       185.199.111.153         Automatic
CNAME   www     YOUR_USERNAME.github.io Automatic
```

**Important:** Replace `YOUR_USERNAME` with your GitHub username!

### B. GitHub Configuration

1. Go to Settings → Pages
2. Custom domain: `installhancock.com`
3. Wait for DNS check to pass (may take a few minutes)
4. Enable "Enforce HTTPS" (wait 24 hours if not available yet)

### C. Verify DNS Propagation

Check if DNS is working:
- https://www.whatsmydns.net/#A/installhancock.com
- Should show the GitHub Pages IPs (185.199.108-111.153)

**Note:** DNS can take 24-48 hours to fully propagate worldwide.

---

## 4. Publish to PyPI

### A. Register on PyPI

1. Create account: https://pypi.org/account/register/
2. Verify email
3. Enable 2FA (recommended)

### B. Create API Token

1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. "Add API token"
   - Name: `hancock-cli`
   - Scope: "Entire account" (or specific project after first upload)
4. Copy the token (starts with `pypi-...`)

### C. Add Token to GitHub Secrets

1. Go to repo Settings → Secrets and variables → Actions
2. "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: paste your PyPI token
5. Add secret

### D. Create a Release

```bash
# Tag the release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases → "Create a new release"
2. Choose tag: `v1.0.0`
3. Release title: `v1.0.0 - Initial Release`
4. Description: Copy from CHANGELOG.md
5. Publish release

The GitHub Action will automatically build and publish to PyPI! 🎉

### E. Manual Publish (Alternative)

If you want to publish manually:

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Upload to Test PyPI first
python -m twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ hancock-cli

# If all good, upload to real PyPI
python -m twine upload dist/*
```

---

## 5. Verify Everything Works

### Test PyPI Install

```bash
# Install from PyPI
pip install hancock-cli

# Test
hancock --version
hancock --help
```

### Test Website

1. Visit https://installhancock.com
2. Verify it loads correctly
3. Test "pip install" command copy
4. Check mobile responsiveness

---

## 6. Update README URLs

After creating the repo, update these in `README.md` and `website/index.html`:

```
Find: yourusername
Replace: YOUR_ACTUAL_GITHUB_USERNAME
```

Files to update:
- `README.md`
- `website/index.html`
- `pyproject.toml`

Then commit and push:

```bash
git add .
git commit -m "Update GitHub URLs"
git push
```

---

## 7. Post-Launch Checklist

- [ ] GitHub repo created and code pushed
- [ ] Website deployed to GitHub Pages
- [ ] Custom domain configured (installhancock.com)
- [ ] DNS propagated and HTTPS working
- [ ] Package published to PyPI
- [ ] `pip install hancock-cli` works
- [ ] README URLs updated
- [ ] GitHub repo description and topics added
- [ ] Create GitHub Discussion for support
- [ ] Tweet/share the launch! 🚀

---

## Troubleshooting

### "DNS_PROBE_FINISHED_NXDOMAIN"
→ DNS not propagated yet, wait 24-48 hours

### "PyPI upload failed"
→ Check API token is correct in GitHub Secrets
→ Ensure version number in pyproject.toml is unique

### "GitHub Actions workflow failed"
→ Check workflow logs in Actions tab
→ Verify secrets are set correctly

### "Website shows 404"
→ Ensure CNAME file is in website/ folder
→ Verify custom domain is set in Settings → Pages

---

## Need Help?

- **GitHub Issues:** Report bugs or ask questions
- **GitHub Discussions:** Community support
- **Email:** your@email.com

---

Good luck with the launch! 🎉
