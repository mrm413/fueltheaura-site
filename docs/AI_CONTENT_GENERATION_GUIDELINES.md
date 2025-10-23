# AI Content Generation Guidelines for Fuel The Aura

## Overview
This document outlines how the BlogGuru AI employee system will generate content for your website while ensuring compliance with all legal requirements and maintaining your brand voice.

## Immediate Action Required

Before the AI begins generating content for your live site, please review and confirm the legal compliance framework outlined in this document. The AI system is designed to automatically include all required disclaimers and legal notices in every piece of content it creates, but you should verify that the language meets your specific requirements.

The LEGAL_COMPLIANCE_CHECKLIST.md file contains a detailed checklist of all legal requirements that the AI will follow during content generation. Both documents work together to ensure your website operates within legal guidelines while providing valuable wellness content to your visitors.

## Legal Compliance Framework

### Medical Disclaimer Integration
The AI will automatically include the following disclaimer at the bottom of every blog post:

> **Health Information Disclaimer**: The information provided here is intended solely for informational and educational purposes and reflects personal opinions and general wellness insights, not professional medical advice. Although many articles reference reputable studies and sources, the content is not written or reviewed by licensed healthcare professionals and should not be relied upon as a substitute for medical consultation, diagnosis, or treatment. Always seek the advice of your physician or qualified healthcare provider regarding any medical condition or before starting any new health regimen, supplement, or therapy. Never disregard professional medical advice or delay seeking it because of something you read here. By using this site, you acknowledge and agree that Fuel The Aura, its authors, and affiliates are not liable for any damages, loss, or harm resulting from reliance on any information provided here. Your health decisions are your own responsibility and should always be made in consultation with a licensed medical professional.

### Affiliate Disclosure Requirements
For posts containing affiliate links, the AI will automatically include:

> **Affiliate Disclosure**: Some of the links in this post are affiliate links. This means that if you click a link and make a purchase, Fuel The Aura may receive a small commission at no additional cost to you. These commissions help support the maintenance and ongoing operation of the website, allowing us to continue providing wellness-related articles and resources. We only link to products or services that we believe may hold genuine value for readers, based on our own opinions, experience, or general knowledge. However, inclusion of any product link does not constitute an endorsement or guarantee. Please always research any product or service carefully and consult your healthcare provider before using any health-related product or supplement.

### Popup Banner Implementation
The AI will ensure that all generated pages include the following popup banner in the header:

```html
<div class="popup-banner">
  <p>⚠️ Fuel The Aura shares wellness opinions and general information only — not medical advice. Always check with your doctor before making health changes.</p>
  <a href="/terms">Review Terms</a> or <button onclick="acceptTerms()">I Understand</button>
</div>
```

## Content Generation Process

### Initial Website Population
Upon first launch, the BlogGuru AI will:
1. Generate 10-15 foundational blog posts covering various wellness topics
2. Create essential pages (About, Contact, Store) if not already present
3. Ensure all generated content includes proper disclaimers
4. Automatically tag posts with relevant categories and metadata

### Content Categories
The AI will focus on these primary content areas:
- Energy Optimization and Chronic Fatigue Management
- Supplement Guides and Reviews
- Lifestyle Wellness Tips
- Holistic Health Approaches
- Product Recommendations (with affiliate disclosure)

### Content Quality Standards
- All health claims will be supported by references to reputable sources
- Posts will be written in an accessible, conversational tone
- Content will be optimized for SEO with proper headings and keywords
- Each post will include a clear call-to-action for user engagement

## Technical Implementation Details

### File Structure
Generated content will be placed in:
- `src/content/blog/` - Blog posts in MDX format
- `src/content/products/` - Product information
- `src/pages/` - Static pages (About, Contact, etc.)

### Metadata Requirements
Each generated post will include:
```md
---
title: "Your Post Title"
description: "Brief description of the post content"
pubDate: "2025-10-21"
author: "Fuel The Aura AI"
tags: ["wellness", "energy", "health"]
disclaimer: "medical"
affiliate: false
---
```

### Automated Features
- Daily content generation schedule
- Automatic GitHub deployment upon content creation
- Built-in content validation and quality checks
- Emergency content rollback capabilities

## User Interaction and Feedback

### Reporting Mechanism
All generated content will include at the end:
> **Notice Something Wrong?** If you find any issues with this post or have concerns about the information provided, please [contact us](/contact) so we can address and review it promptly.

### Content Updates
The AI system will:
- Monitor user feedback through the reporting mechanism
- Automatically update or remove content based on feedback
- Generate follow-up posts to address common questions
- Maintain content freshness with regular updates

## Deployment Process

### First Launch Sequence
1. AI generates initial content batch (10-15 posts)
2. Content is validated for legal compliance
3. Static site is built using `npm run build`
4. Site is automatically deployed to GitHub Pages
5. All content is immediately live and accessible

### Ongoing Operations
- Content generation runs daily
- New posts are automatically deployed
- System monitors for user feedback and adjusts accordingly
- Regular backups ensure content safety

## Customization Options

You can customize the AI's behavior by modifying:
- Content frequency (daily, weekly, etc.)
- Post length and depth
- Focus topics and categories
- Disclaimer language and placement
- Affiliate link handling

## Monitoring and Maintenance

The AI system includes:
- 24/7 operation monitoring
- Automatic error detection and recovery
- Performance analytics and reporting
- Security scanning and updates
- Backup and rollback capabilities

This ensures your website remains consistently updated with fresh, compliant content while requiring zero ongoing effort from you.