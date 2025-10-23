"""
Mass Content Scraping and Analysis System for Fuel The Aura
This system scrapes thousands of health and wellness websites to learn content strategies
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse
import time
from collections import Counter
import nltk
from textblob import TextBlob

class HealthContentScraper:
    """
    Advanced web scraper for health and wellness content analysis
    """
    
    def __init__(self, db_path="content_intelligence.db"):
        self.db_path = db_path
        self.setup_database()
        
        # Major health and wellness sites to scrape
        self.target_sites = [
            # Health Authority Sites
            "https://www.healthline.com",
            "https://www.webmd.com",
            "https://www.medicalnewstoday.com",
            "https://www.verywellhealth.com",
            "https://www.mayoclinic.org",
            "https://www.clevelandclinic.org",
            
            # Fitness Sites
            "https://www.bodybuilding.com",
            "https://www.menshealth.com",
            "https://www.womenshealthmag.com",
            "https://www.shape.com",
            "https://www.self.com",
            "https://www.runnersworld.com",
            
            # Nutrition Sites
            "https://www.eatright.org",
            "https://www.precisionnutrition.com",
            "https://www.nutritiondata.self.com",
            
            # Supplement Review Sites
            "https://examine.com",
            "https://www.consumerlab.com",
            
            # Holistic Health
            "https://www.mindbodygreen.com",
            "https://www.wellandgood.com",
            "https://www.goop.com",
            
            # Scientific Sources
            "https://pubmed.ncbi.nlm.nih.gov",
            "https://www.nih.gov",
        ]
        
        # Headers to avoid being blocked
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def setup_database(self):
        """Initialize SQLite database for storing scraped content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                meta_description TEXT,
                word_count INTEGER,
                headline_structure TEXT,
                keywords TEXT,
                internal_links INTEGER,
                external_links INTEGER,
                images_count INTEGER,
                social_shares INTEGER,
                estimated_traffic INTEGER,
                scraped_date TIMESTAMP,
                source_domain TEXT
            )
        ''')
        
        # Headlines analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS headlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                headline TEXT,
                word_count INTEGER,
                power_words TEXT,
                emotional_score REAL,
                click_potential REAL,
                article_id INTEGER,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        # Keywords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT,
                frequency INTEGER,
                search_volume INTEGER,
                competition REAL,
                article_id INTEGER,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        # Content patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                effectiveness_score REAL,
                usage_count INTEGER,
                last_updated TIMESTAMP
            )
        ''')
        
        # Conversion elements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversion_elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                element_type TEXT,
                element_text TEXT,
                placement TEXT,
                conversion_score REAL,
                article_id INTEGER,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def scrape_site(self, session, url, max_pages=100):
        """Scrape a single website for content"""
        try:
            async with session.get(url, headers=self.headers, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract article links
                    article_links = self.extract_article_links(soup, url)
                    
                    # Scrape individual articles
                    for article_url in article_links[:max_pages]:
                        await self.scrape_article(session, article_url)
                        await asyncio.sleep(1)  # Rate limiting
                        
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
    
    def extract_article_links(self, soup, base_url):
        """Extract article links from a page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Filter for article URLs
            if self.is_article_url(full_url):
                links.append(full_url)
        
        return list(set(links))  # Remove duplicates
    
    def is_article_url(self, url):
        """Determine if URL is likely an article"""
        article_patterns = [
            r'/article/',
            r'/blog/',
            r'/post/',
            r'/\d{4}/\d{2}/',  # Date-based URLs
            r'/health/',
            r'/fitness/',
            r'/nutrition/',
            r'/wellness/',
        ]
        
        return any(re.search(pattern, url) for pattern in article_patterns)
    
    async def scrape_article(self, session, url):
        """Scrape individual article and analyze content"""
        try:
            async with session.get(url, headers=self.headers, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract article data
                    article_data = self.extract_article_data(soup, url)
                    
                    # Analyze content
                    analysis = self.analyze_content(article_data)
                    
                    # Store in database
                    self.store_article(article_data, analysis)
                    
        except Exception as e:
            print(f"Error scraping article {url}: {str(e)}")
    
    def extract_article_data(self, soup, url):
        """Extract all relevant data from an article"""
        data = {
            'url': url,
            'title': self.extract_title(soup),
            'content': self.extract_content(soup),
            'meta_description': self.extract_meta_description(soup),
            'word_count': 0,
            'headline_structure': '',
            'keywords': [],
            'internal_links': len(soup.find_all('a', href=lambda x: x and urlparse(url).netloc in x)),
            'external_links': len(soup.find_all('a', href=lambda x: x and urlparse(url).netloc not in x)),
            'images_count': len(soup.find_all('img')),
            'source_domain': urlparse(url).netloc,
            'scraped_date': datetime.now()
        }
        
        # Calculate word count
        if data['content']:
            data['word_count'] = len(data['content'].split())
        
        # Extract keywords
        data['keywords'] = self.extract_keywords(data['content'])
        
        # Analyze headline structure
        data['headline_structure'] = self.analyze_headline_structure(soup)
        
        return data
    
    def extract_title(self, soup):
        """Extract article title"""
        title_tags = ['h1', 'title']
        for tag in title_tags:
            element = soup.find(tag)
            if element:
                return element.get_text().strip()
        return ""
    
    def extract_content(self, soup):
        """Extract main article content"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try common article containers
        article_selectors = [
            'article',
            '[class*="article"]',
            '[class*="content"]',
            '[class*="post"]',
            'main'
        ]
        
        for selector in article_selectors:
            content = soup.select_one(selector)
            if content:
                return content.get_text(separator=' ', strip=True)
        
        # Fallback to body
        return soup.get_text(separator=' ', strip=True)
    
    def extract_meta_description(self, soup):
        """Extract meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta:
            return meta.get('content', '')
        return ""
    
    def extract_keywords(self, text):
        """Extract keywords from content"""
        if not text:
            return []
        
        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        word_freq = Counter(words)
        
        # Return top 20 keywords
        return [word for word, freq in word_freq.most_common(20)]
    
    def analyze_headline_structure(self, soup):
        """Analyze headline structure and hierarchy"""
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
        return json.dumps(headings)
    
    def analyze_content(self, article_data):
        """Perform advanced content analysis"""
        analysis = {
            'emotional_score': 0,
            'readability_score': 0,
            'power_words': [],
            'persuasion_elements': [],
            'cta_elements': [],
            'social_proof': []
        }
        
        content = article_data.get('content', '')
        title = article_data.get('title', '')
        
        # Emotional analysis
        if content:
            blob = TextBlob(content)
            analysis['emotional_score'] = blob.sentiment.polarity
        
        # Power words detection
        power_words = [
            'proven', 'guaranteed', 'exclusive', 'limited', 'secret',
            'amazing', 'revolutionary', 'breakthrough', 'discover',
            'transform', 'ultimate', 'essential', 'powerful', 'effective'
        ]
        
        found_power_words = [word for word in power_words if word in content.lower()]
        analysis['power_words'] = found_power_words
        
        # CTA detection
        cta_patterns = [
            r'click here',
            r'learn more',
            r'get started',
            r'buy now',
            r'shop now',
            r'sign up',
            r'subscribe',
            r'download',
            r'try now'
        ]
        
        for pattern in cta_patterns:
            if re.search(pattern, content.lower()):
                analysis['cta_elements'].append(pattern)
        
        # Social proof detection
        social_proof_patterns = [
            r'\d+\s+(people|users|customers)',
            r'testimonial',
            r'review',
            r'rated',
            r'trusted by'
        ]
        
        for pattern in social_proof_patterns:
            matches = re.findall(pattern, content.lower())
            if matches:
                analysis['social_proof'].extend(matches)
        
        return analysis
    
    def store_article(self, article_data, analysis):
        """Store article and analysis in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert article
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (url, title, content, meta_description, word_count, headline_structure,
                 keywords, internal_links, external_links, images_count, scraped_date, source_domain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_data['url'],
                article_data['title'],
                article_data['content'],
                article_data['meta_description'],
                article_data['word_count'],
                article_data['headline_structure'],
                json.dumps(article_data['keywords']),
                article_data['internal_links'],
                article_data['external_links'],
                article_data['images_count'],
                article_data['scraped_date'],
                article_data['source_domain']
            ))
            
            article_id = cursor.lastrowid
            
            # Insert headline analysis
            cursor.execute('''
                INSERT INTO headlines 
                (headline, word_count, power_words, emotional_score, article_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                article_data['title'],
                len(article_data['title'].split()),
                json.dumps(analysis['power_words']),
                analysis['emotional_score'],
                article_id
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"Error storing article: {str(e)}")
            conn.rollback()
        
        finally:
            conn.close()
    
    async def run_mass_scraping(self):
        """Execute mass scraping operation"""
        print("Starting mass content scraping...")
        print(f"Target sites: {len(self.target_sites)}")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for site in self.target_sites:
                task = asyncio.create_task(self.scrape_site(session, site))
                tasks.append(task)
            
            await asyncio.gather(*tasks)
        
        print("Mass scraping completed!")
        self.generate_insights()
    
    def generate_insights(self):
        """Generate insights from scraped data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Top performing headline patterns
        cursor.execute('''
            SELECT headline, emotional_score, power_words
            FROM headlines
            ORDER BY emotional_score DESC
            LIMIT 50
        ''')
        
        top_headlines = cursor.fetchall()
        
        # Most common keywords
        cursor.execute('''
            SELECT keywords, COUNT(*) as frequency
            FROM articles
            GROUP BY keywords
            ORDER BY frequency DESC
            LIMIT 100
        ''')
        
        common_keywords = cursor.fetchall()
        
        # Average article metrics
        cursor.execute('''
            SELECT 
                AVG(word_count) as avg_words,
                AVG(internal_links) as avg_internal_links,
                AVG(external_links) as avg_external_links,
                AVG(images_count) as avg_images
            FROM articles
        ''')
        
        avg_metrics = cursor.fetchone()
        
        conn.close()
        
        # Save insights
        insights = {
            'top_headlines': [h[0] for h in top_headlines],
            'common_keywords': common_keywords,
            'average_metrics': {
                'word_count': avg_metrics[0],
                'internal_links': avg_metrics[1],
                'external_links': avg_metrics[2],
                'images': avg_metrics[3]
            },
            'generated_date': datetime.now().isoformat()
        }
        
        with open('content_insights.json', 'w') as f:
            json.dump(insights, f, indent=2)
        
        print("Insights generated and saved to content_insights.json")

# Main execution
if __name__ == "__main__":
    scraper = HealthContentScraper()
    asyncio.run(scraper.run_mass_scraping())