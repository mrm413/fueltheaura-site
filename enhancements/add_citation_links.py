#!/usr/bin/env python3
"""
Add Hyperlinks to Citations in Blog Posts
This script updates the AI system to automatically add DOI/PubMed links to all citations
"""

import os
import re

def update_ai_system_for_citations():
    """Update the AI system to include hyperlinked citations"""
    
    ai_system_file = '/opt/fueltheaura-ai/premium_ai_system.py'
    
    if not os.path.exists(ai_system_file):
        print(f"❌ Error: {ai_system_file} not found")
        return
    
    # Read the file
    with open(ai_system_file, 'r') as f:
        content = f.read()
    
    # Backup
    backup_file = ai_system_file + '.citation_backup'
    with open(backup_file, 'w') as f:
        f.write(content)
    print(f"📁 Backup created: {backup_file}")
    
    # Add citation linking instructions to the prompt
    citation_instructions = '''
    
    # IMPORTANT: Citation Linking Requirements
    # All citations MUST include hyperlinks to improve SEO and provide value
    # Format citations as follows:
    
    # For journal articles with DOI:
    # Author et al. (Year). "Title." *Journal*, Volume(Issue), Pages. [DOI: doi.org/xxxxx](https://doi.org/xxxxx)
    
    # For PubMed articles:
    # Author et al. (Year). "Title." *Journal*, Volume(Issue), Pages. [PubMed](https://pubmed.ncbi.nlm.nih.gov/PMID)
    
    # For web sources:
    # Organization. (Year). **Title.** Retrieved from [Source Name](https://full-url.com)
    
    # Example References Section:
    # ## References
    # 
    # 1. Smith, J., et al. (2020). "Effects of Exercise on Mental Health." *Journal of Psychology*, 45(2), 123-145. [DOI: doi.org/10.1234/example](https://doi.org/10.1234/example)
    # 2. National Institute of Health. (2021). **Mental Health Statistics.** Retrieved from [NIH.gov](https://www.nih.gov/mental-health)
    # 3. Johnson, A. (2019). "Cognitive Behavioral Therapy Outcomes." *Clinical Psychology Review*, 30(4), 567-589. [PubMed](https://pubmed.ncbi.nlm.nih.gov/12345678)
    
    # CRITICAL: Every citation must have a clickable hyperlink. No exceptions.
    '''
    
    # Find where to insert the instructions (after the main prompt)
    if 'Generate a comprehensive' in content or 'health and wellness' in content:
        # Insert before the content generation section
        insert_pos = content.find('Generate a comprehensive')
        if insert_pos == -1:
            insert_pos = len(content) - 1000  # Near the end
        
        new_content = content[:insert_pos] + citation_instructions + '\n\n' + content[insert_pos:]
        
        # Write updated file
        with open(ai_system_file, 'w') as f:
            f.write(new_content)
        
        print("✅ Updated AI system with citation linking requirements")
        print("\n📋 Citation Format Requirements Added:")
        print("  • DOI links for journal articles")
        print("  • PubMed links for medical research")
        print("  • Full URLs for web sources")
        print("  • All citations must be hyperlinked")
        
        print("\n🔄 Restart the service:")
        print("   systemctl restart fueltheaura-ai.service")
    else:
        print("⚠️  Could not find insertion point. Manual update required.")

if __name__ == '__main__':
    update_ai_system_for_citations()