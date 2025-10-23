"""
Setup script for Fuel The Aura AI Content System
Install all dependencies and configure the system
"""

from setuptools import setup, find_packages

setup(
    name="fueltheaura-ai-system",
    version="2.0.0",
    description="Advanced AI Content Generation System for Health & Wellness Websites",
    author="Fuel The Aura",
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.8.0',
        'beautifulsoup4>=4.11.0',
        'nltk>=3.8.0',
        'textblob>=0.17.0',
        'lxml>=4.9.0',
        'requests>=2.28.0',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'fueltheaura-ai=INTEGRATED_AI_SYSTEM_FINAL:main',
        ],
    },
)