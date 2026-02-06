# Hancock Website

Landing page for installhancock.com

## Deploying to GitHub Pages

### Option 1: Using GitHub Actions (Automatic)

1. Push the `website/` folder contents to a `gh-pages` branch
2. Enable GitHub Pages in repo settings
3. Set custom domain to `installhancock.com`

### Option 2: Manual Deployment

```bash
# From the website directory
cd website

# Initialize git (if not already)
git init
git add .
git commit -m "Deploy website"

# Push to gh-pages branch
git branch -M gh-pages
git remote add origin https://github.com/yourusername/hancock-cli.git
git push -u origin gh-pages
```

### Option 3: Using gh-pages npm package

```bash
npm install -g gh-pages

# From project root
gh-pages -d website
```

## Domain Setup (installhancock.com)

### 1. Configure DNS

In your domain registrar (e.g., Namecheap, GoDaddy), add these DNS records:

```
Type    Name    Value
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     yourusername.github.io
```

### 2. Enable GitHub Pages

1. Go to repo Settings → Pages
2. Source: Deploy from a branch → `gh-pages` → `/ (root)`
3. Custom domain: `installhancock.com`
4. Enforce HTTPS: ✓

### 3. Wait for DNS Propagation

- DNS changes can take 24-48 hours
- Check status: https://www.whatsmydns.net/

## Testing Locally

```bash
# Using Python
python3 -m http.server 8000

# Or using PHP
php -S localhost:8000

# Then visit: http://localhost:8000
```

## Files

- `index.html` - Main landing page
- `404.html` - Custom 404 error page
- `CNAME` - Custom domain configuration
- `robots.txt` - SEO configuration
