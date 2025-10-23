"""
Persuasive Content Generator with Dark Psychology Techniques
Generates highly engaging health and wellness content optimized for conversions
"""

import json
import random
from datetime import datetime
import sqlite3
from textblob import TextBlob
import re

class PersuasiveContentGenerator:
    """
    Advanced content generator using psychological persuasion techniques
    """
    
    def __init__(self, intelligence_db="content_intelligence.db"):
        self.intelligence_db = intelligence_db
        
        # Power words for different emotions
        self.power_words = {
            'urgency': ['now', 'today', 'immediately', 'urgent', 'limited', 'hurry', 'fast', 'quick'],
            'exclusivity': ['exclusive', 'secret', 'insider', 'private', 'members-only', 'elite', 'premium'],
            'authority': ['proven', 'certified', 'expert', 'professional', 'scientific', 'research-backed', 'clinical'],
            'transformation': ['transform', 'breakthrough', 'revolutionary', 'game-changing', 'life-changing', 'powerful'],
            'safety': ['safe', 'guaranteed', 'risk-free', 'protected', 'secure', 'trusted', 'verified'],
            'curiosity': ['secret', 'hidden', 'surprising', 'shocking', 'revealed', 'discovered', 'unknown']
        }
        
        # Headline formulas that convert
        self.headline_formulas = [
            "How to {benefit} Without {pain_point}",
            "The {number} Secrets to {desired_outcome}",
            "{number} Science-Backed Ways to {benefit}",
            "Why {common_belief} is Wrong (And What to Do Instead)",
            "The Ultimate Guide to {topic} for {target_audience}",
            "{number} Signs You Need {solution}",
            "What {authority_figure} Won't Tell You About {topic}",
            "The Shocking Truth About {topic}",
            "{number} Mistakes That Are Sabotaging Your {goal}",
            "How I {achieved_result} in {timeframe} (And You Can Too)"
        ]
        
        # Psychological triggers
        self.psychological_triggers = {
            'scarcity': [
                "Limited time offer",
                "Only {number} spots available",
                "Stock running low",
                "Offer expires soon",
                "While supplies last"
            ],
            'social_proof': [
                "Join {number}+ satisfied customers",
                "Trusted by thousands",
                "Rated {rating} stars by users",
                "{number}% of users report {benefit}",
                "Featured in {publication}"
            ],
            'authority': [
                "Recommended by health professionals",
                "Backed by {number} studies",
                "Developed by experts",
                "Clinically tested",
                "FDA-approved facility"
            ],
            'reciprocity': [
                "Free guide included",
                "Bonus content inside",
                "Exclusive tips for subscribers",
                "Limited-time free shipping",
                "Free consultation available"
            ],
            'loss_aversion': [
                "Don't miss out on {benefit}",
                "Stop wasting money on {alternative}",
                "Avoid these {number} costly mistakes",
                "What you're losing by not {action}",
                "The hidden cost of ignoring {problem}"
            ]
        }
        
        # Content structure templates
        self.content_structures = {
            'problem_agitate_solve': [
                'Identify the problem',
                'Agitate the pain points',
                'Present the solution',
                'Provide proof',
                'Call to action'
            ],
            'before_after_bridge': [
                'Current situation (before)',
                'Desired outcome (after)',
                'Bridge (how to get there)',
                'Social proof',
                'Call to action'
            ],
            'storytelling': [
                'Hook with relatable story',
                'Build tension',
                'Introduce solution',
                'Show transformation',
                'Call to action'
            ]
        }
        
        # SEO optimization patterns
        self.seo_patterns = {
            'title_length': (50, 60),  # Optimal character count
            'meta_description_length': (150, 160),
            'keyword_density': (1.5, 2.5),  # Percentage
            'header_frequency': 300,  # Words between headers
            'internal_links': (3, 5),  # Per 1000 words
            'external_links': (2, 3)  # Per 1000 words
        }
    
    def generate_headline(self, topic, target_emotion='curiosity'):
        """Generate high-converting headline"""
        formula = random.choice(self.headline_formulas)
        power_word = random.choice(self.power_words[target_emotion])
        
        # Customize based on topic
        variations = {
            'energy': {
                'benefit': 'boost your energy naturally',
                'pain_point': 'caffeine crashes',
                'desired_outcome': 'all-day energy',
                'number': random.randint(5, 10)
            },
            'weight_loss': {
                'benefit': 'lose weight sustainably',
                'pain_point': 'restrictive diets',
                'desired_outcome': 'your ideal weight',
                'number': random.randint(7, 12)
            },
            'supplements': {
                'benefit': 'optimize your health',
                'pain_point': 'wasting money on ineffective supplements',
                'desired_outcome': 'maximum supplement benefits',
                'number': random.randint(5, 8)
            }
        }
        
        topic_vars = variations.get(topic, variations['energy'])
        
        # Fill in formula
        headline = formula.format(**topic_vars)
        
        # Add power word if not already present
        if power_word.lower() not in headline.lower():
            headline = f"{power_word.capitalize()}: {headline}"
        
        return headline
    
    def generate_meta_description(self, headline, primary_keyword):
        """Generate SEO-optimized meta description with psychological triggers"""
        trigger = random.choice(self.psychological_triggers['curiosity'])
        
        templates = [
            f"{trigger}. {headline}. {primary_keyword} guide with proven results. Click to learn more.",
            f"Discover {primary_keyword} secrets that experts don't want you to know. {headline}. Read now!",
            f"{headline}. Science-backed {primary_keyword} strategies. Join thousands who've transformed their health.",
            f"Stop struggling with {primary_keyword}. {headline}. Expert tips inside. Limited time access."
        ]
        
        description = random.choice(templates)
        
        # Ensure optimal length
        if len(description) > 160:
            description = description[:157] + "..."
        
        return description
    
    def create_opening_hook(self, topic, use_dark_psychology=True):
        """Create compelling opening that hooks readers"""
        hooks = {
            'pattern_interrupt': [
                "Everything you've been told about {topic} is wrong.",
                "I'm about to share something controversial about {topic}...",
                "What if I told you that {topic} could be easier than you think?"
            ],
            'curiosity_gap': [
                "There's a little-known secret about {topic} that changes everything...",
                "Most people don't know this about {topic} (but they should)...",
                "The {topic} industry doesn't want you to know this..."
            ],
            'empathy': [
                "If you've been struggling with {topic}, you're not alone...",
                "I know how frustrating {topic} can be. I've been there too...",
                "You've tried everything for {topic}, but nothing seems to work..."
            ],
            'shocking_stat': [
                "Did you know that 87% of people fail at {topic}? Here's why...",
                "Studies show that {topic} affects 1 in 3 people. Are you one of them?",
                "Research reveals a shocking truth about {topic}..."
            ]
        }
        
        if use_dark_psychology:
            hook_type = random.choice(['pattern_interrupt', 'curiosity_gap'])
        else:
            hook_type = random.choice(['empathy', 'shocking_stat'])
        
        hook = random.choice(hooks[hook_type]).format(topic=topic)
        
        return hook
    
    def generate_content_body(self, topic, word_count=1500, structure='problem_agitate_solve'):
        """Generate full article body with persuasive elements"""
        
        sections = []
        current_structure = self.content_structures[structure]
        words_per_section = word_count // len(current_structure)
        
        for section_type in current_structure:
            section_content = self.generate_section(topic, section_type, words_per_section)
            sections.append(section_content)
        
        # Combine sections
        full_content = "\n\n".join(sections)
        
        # Add psychological triggers throughout
        full_content = self.inject_psychological_triggers(full_content)
        
        # Add internal linking opportunities
        full_content = self.add_internal_link_anchors(full_content)
        
        return full_content
    
    def generate_section(self, topic, section_type, word_count):
        """Generate individual section based on type"""
        
        section_templates = {
            'Identify the problem': f"""
## The Hidden Problem with {topic.title()}

Many people struggle with {topic} without realizing the root cause. You might be experiencing:

- Constant frustration despite trying everything
- Wasting money on solutions that don't work
- Feeling overwhelmed by conflicting information
- Watching others succeed while you stay stuck

The truth is, most approaches to {topic} are fundamentally flawed. They focus on symptoms rather than addressing the underlying issues.
""",
            'Agitate the pain points': f"""
## Why This Problem Gets Worse Over Time

Ignoring {topic} doesn't make it go away. In fact, it compounds:

**Financial Cost**: You continue spending money on ineffective solutions, potentially thousands of dollars per year.

**Time Lost**: Every day without proper {topic} management is a day you can't get back.

**Health Impact**: The longer you wait, the more difficult it becomes to reverse the effects.

**Emotional Toll**: The constant disappointment and frustration takes a serious toll on your mental health.

The question isn't whether you can afford to address {topic} - it's whether you can afford NOT to.
""",
            'Present the solution': f"""
## The Science-Backed Solution

After analyzing thousands of success stories and reviewing the latest research, we've identified what actually works for {topic}.

The key is a three-pronged approach:

1. **Foundation Building**: Establishing the right baseline through proven methods
2. **Strategic Implementation**: Using evidence-based techniques that deliver results
3. **Sustainable Maintenance**: Creating habits that last long-term

This isn't another quick fix or fad. This is a comprehensive system backed by science and proven by real results.
""",
            'Provide proof': f"""
## Real Results from Real People

Don't just take our word for it. Here's what others have experienced:

> "I tried everything for {topic} before finding this approach. Within 30 days, I saw changes I never thought possible." - Sarah M.

> "The difference is night and day. I wish I had discovered this years ago." - Michael T.

> "Finally, something that actually works. I've recommended it to all my friends." - Jennifer L.

**Clinical Evidence**: Multiple peer-reviewed studies support this approach, with success rates exceeding 85%.

**Long-term Results**: Follow-up studies show sustained improvements even years later.
""",
            'Call to action': f"""
## Take Action Today

You have two choices:

**Option 1**: Continue struggling with {topic}, wasting time and money on approaches that don't work.

**Option 2**: Take action now and start seeing real results within days.

The decision is yours, but remember: every day you wait is another day of unnecessary struggle.

**Limited Time Offer**: Get started today and receive exclusive bonuses worth $197 absolutely free.

[Get Started Now] - Risk-free with our 60-day money-back guarantee.

Don't let another day go by. Your future self will thank you.
"""
        }
        
        return section_templates.get(section_type, f"## {section_type}\n\nContent for {topic}...")
    
    def inject_psychological_triggers(self, content):
        """Inject psychological triggers throughout content"""
        
        # Add scarcity
        scarcity_trigger = random.choice(self.psychological_triggers['scarcity'])
        content = content.replace('[Get Started Now]', f'[{scarcity_trigger} - Get Started Now]')
        
        # Add social proof
        social_proof = random.choice(self.psychological_triggers['social_proof'])
        content = content.replace('Real Results', f'Real Results - {social_proof}')
        
        # Add authority
        authority = random.choice(self.psychological_triggers['authority'])
        content = content.replace('Science-Backed', f'Science-Backed ({authority})')
        
        return content
    
    def add_internal_link_anchors(self, content):
        """Add natural internal linking opportunities"""
        
        link_phrases = [
            'learn more about',
            'discover how',
            'read our guide on',
            'check out our article about',
            'explore our comprehensive guide to'
        ]
        
        # This would be enhanced to actually link to relevant content
        # For now, just mark opportunities
        for phrase in link_phrases:
            if phrase in content.lower():
                # Mark as internal link opportunity
                pass
        
        return content
    
    def generate_product_description(self, product_name, benefits, price):
        """Generate conversion-optimized product description"""
        
        description = f"""
# {product_name}

## Transform Your Health with {product_name}

{random.choice(self.psychological_triggers['authority'])}

### Why {product_name} is Different

Unlike other products that make empty promises, {product_name} delivers real, measurable results:

"""
        
        # Add benefits with psychological framing
        for i, benefit in enumerate(benefits, 1):
            trigger = random.choice(['authority', 'social_proof', 'transformation'])
            power_word = random.choice(self.power_words[trigger])
            description += f"**{i}. {power_word.capitalize()} {benefit}**\n\n"
        
        # Add pricing with anchoring
        original_price = price * 1.5
        description += f"""
### Special Pricing

~~${original_price:.2f}~~ **${price:.2f}**

{random.choice(self.psychological_triggers['scarcity'])}

### Risk-Free Guarantee

Try {product_name} for 60 days. If you're not completely satisfied, we'll refund every penny. No questions asked.

{random.choice(self.psychological_triggers['social_proof'])}

[Add to Cart Now] - {random.choice(self.psychological_triggers['reciprocity'])}
"""
        
        return description
    
    def optimize_for_seo(self, content, primary_keyword, secondary_keywords):
        """Optimize content for SEO"""
        
        # Ensure keyword density
        word_count = len(content.split())
        keyword_count = content.lower().count(primary_keyword.lower())
        current_density = (keyword_count / word_count) * 100
        
        target_density = 2.0  # 2% keyword density
        
        if current_density < target_density:
            # Add keyword naturally in strategic locations
            content = self.inject_keywords_naturally(content, primary_keyword, secondary_keywords)
        
        # Add schema markup opportunities
        content = self.add_schema_markup_hints(content)
        
        return content
    
    def inject_keywords_naturally(self, content, primary_keyword, secondary_keywords):
        """Inject keywords naturally into content"""
        
        # Strategic locations for keywords
        locations = [
            'first 100 words',
            'last 100 words',
            'subheadings',
            'image alt text',
            'internal links'
        ]
        
        # This would be enhanced with actual NLP to inject naturally
        # For now, return content as-is
        return content
    
    def add_schema_markup_hints(self, content):
        """Add hints for schema markup implementation"""
        
        # Mark FAQ sections
        if 'Q:' in content or 'Question:' in content:
            content = '<!-- FAQ Schema -->\n' + content
        
        # Mark how-to sections
        if 'Step 1' in content or 'How to' in content:
            content = '<!-- HowTo Schema -->\n' + content
        
        # Mark product sections
        if '$' in content and 'price' in content.lower():
            content = '<!-- Product Schema -->\n' + content
        
        return content
    
    def generate_complete_article(self, topic, primary_keyword, word_count=2000):
        """Generate complete article with all optimizations"""
        
        # Generate headline
        headline = self.generate_headline(topic)
        
        # Generate meta description
        meta_description = self.generate_meta_description(headline, primary_keyword)
        
        # Generate opening hook
        opening = self.create_opening_hook(topic, use_dark_psychology=True)
        
        # Generate body content
        body = self.generate_content_body(topic, word_count)
        
        # Combine all elements
        article = f"""---
title: "{headline}"
description: "{meta_description}"
pubDate: "{datetime.now().strftime('%Y-%m-%d')}"
author: "Fuel The Aura"
tags: ["{topic}", "health", "wellness"]
disclaimer: "medical"
affiliate: true
---

{opening}

{body}

---

**Health Information Disclaimer**: The information provided here is intended solely for informational and educational purposes and reflects personal opinions and general wellness insights, not professional medical advice. Although many articles reference reputable studies and sources, the content is not written or reviewed by licensed healthcare professionals and should not be relied upon as a substitute for medical consultation, diagnosis, or treatment. Always seek the advice of your physician or qualified healthcare provider regarding any medical condition or before starting any new health regimen, supplement, or therapy. Never disregard professional medical advice or delay seeking it because of something you read here. By using this site, you acknowledge and agree that Fuel The Aura, its authors, and affiliates are not liable for any damages, loss, or harm resulting from reliance on any information provided here. Your health decisions are your own responsibility and should always be made in consultation with a licensed medical professional.

**Affiliate Disclosure**: Some of the links in this post are affiliate links. This means that if you click a link and make a purchase, Fuel The Aura may receive a small commission at no additional cost to you. These commissions help support the maintenance and ongoing operation of the website, allowing us to continue providing wellness-related articles and resources. We only link to products or services that we believe may hold genuine value for readers, based on our own opinions, experience, or general knowledge. However, inclusion of any product link does not constitute an endorsement or guarantee. Please always research any product or service carefully and consult your healthcare provider before using any health-related product or supplement.

**Notice Something Wrong?** If you find any issues with this post or have concerns about the information provided, please [contact us](/contact) so we can address and review it promptly.
"""
        
        return article

# Example usage
if __name__ == "__main__":
    generator = PersuasiveContentGenerator()
    
    # Generate sample article
    article = generator.generate_complete_article(
        topic="energy",
        primary_keyword="boost energy naturally",
        word_count=2000
    )
    
    print(article)
    
    # Save to file
    with open('sample_persuasive_article.md', 'w') as f:
        f.write(article)
    
    print("\nArticle generated successfully!")