# FuelTheAura Website

A complete energy and wellness website with homepage, blog, and store sections.

## 🌐 Live Preview
https://8081-2cd10640-3ebf-4d5d-ac89-a097d0c3e346.proxy.daytona.works

## 📁 Structure
```
src/
├── index.njk (Homepage)
├── about.njk
├── contact.njk
├── store.njk
├── _includes/
│   ├── base.njk
│   ├── nav.njk
│   └── footer.njk
├── blog/
│   ├── index.njk (Blog listing)
│   └── posts/
│       ├── sample-post.njk
│       ├── understanding-fatigue.njk
│       └── supplement-guide.njk
└── assets/
    └── css/
        └── style.css
```

## 🚀 Development

```bash
# Install dependencies
npm install

# Build site
npm run build

# Serve locally with hot reload
npx eleventy --serve --port=8080
```

## 📝 Integration with BlogGuru

This site is designed to receive content from the BlogGuru AI content generator:
1. BlogGuru generates blog posts
2. Posts are saved to `src/blog/posts/`
3. This site builds and deploys them to fueltheaura.com

## 🎨 Features

- Responsive design
- Modern UI with gradient accents
- Blog with sample posts
- Product store with affiliate links
- SEO-optimized structure
- Mobile-friendly navigation