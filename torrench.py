#!/usr/bin/env python3
"""
Enhanced Torrench - Multi-site torrent search tool
Supports multiple popular torrent sites with English search
"""

import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from termcolor import colored
import time
import re
from urllib.parse import urljoin, quote

class TorrentSite:
    """Base class for torrent sites"""
    def __init__(self, name, base_urls, search_path="", result_selector=""):
        self.name = name
        self.base_urls = base_urls if isinstance(base_urls, list) else [base_urls]
        self.search_path = search_path
        self.result_selector = result_selector
        self.working_url = None
    
    def test_connection(self):
        """Test if any of the base URLs are working"""
        for url in self.base_urls:
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    self.working_url = url
                    return True
            except:
                continue
        return False
    
    def search(self, query, page=0):
        """Search for torrents on this site"""
        if not self.working_url:
            return []
        
        try:
            search_url = self.build_search_url(query, page)
            response = requests.get(search_url, timeout=15)
            if response.status_code == 200:
                return self.parse_results(response.content, query)
        except Exception as e:
            print(colored(f"Error searching {self.name}: {e}", "red"))
        
        return []
    
    def build_search_url(self, query, page=0):
        """Build search URL - to be implemented by subclasses"""
        raise NotImplementedError
    
    def parse_results(self, content, query):
        """Parse search results - to be implemented by subclasses"""
        raise NotImplementedError

class PirateBay(TorrentSite):
    def __init__(self):
        super().__init__(
            "The Pirate Bay",
            [
                "https://thepiratebay.org",
                "https://tpb.party",
                "https://piratebay.party",
                "https://thepiratebay.zone",
                "https://pirateproxy.live",
                "https://thehiddenbay.com",
                "https://piratebay.live",
                "https://thepiratebay.rocks",
                "https://tpb.pm",
                "https://piratebay.ink"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/s/?q={quote(query)}&page={page}&orderby=99"
    
    def parse_results(self, content, query):
        soup = BeautifulSoup(content, "lxml")
        results = []
        
        try:
            table = soup.find('table', id="searchResult")
            if not table:
                return results
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    name_cell = row.find('a', class_="detLink")
                    if not name_cell:
                        continue
                    
                    name = name_cell.get_text().strip()
                    detail_url = urljoin(self.working_url, name_cell['href'])
                    
                    # Get category
                    cat_cell = row.find('td', class_="vertTh")
                    category = "Unknown"
                    if cat_cell:
                        cat_links = cat_cell.find_all('a')
                        if len(cat_links) >= 2:
                            category = f"{cat_links[0].get_text()} > {cat_links[1].get_text()}"
                    
                    # Get uploader
                    uploader_cell = row.find('a', class_="detDesc")
                    uploader = uploader_cell.get_text() if uploader_cell else "Unknown"
                    
                    # Get seeds/leeches
                    seed_cells = row.find_all('td', align="right")
                    seeds = seed_cells[0].get_text() if len(seed_cells) > 0 else "0"
                    leeches = seed_cells[1].get_text() if len(seed_cells) > 1 else "0"
                    
                    # Get date and size
                    desc_cell = row.find('font', class_="detDesc")
                    date, size = "Unknown", "Unknown"
                    if desc_cell:
                        desc_text = desc_cell.get_text()
                        parts = desc_text.split(',')
                        if len(parts) >= 2:
                            date = parts[0].split()[-1] if parts[0] else "Unknown"
                            size_match = re.search(r'Size (\d+\.?\d*\s*[A-Za-z]+)', desc_text)
                            if size_match:
                                size = size_match.group(1)
                    
                    # Check uploader status
                    is_vip = row.find('img', {'title': "VIP"})
                    is_trusted = row.find('img', {'title': 'Trusted'})
                    
                    results.append({
                        'name': name,
                        'category': category,
                        'uploader': uploader,
                        'seeds': seeds,
                        'leeches': leeches,
                        'date': date,
                        'size': size,
                        'detail_url': detail_url,
                        'site': self.name,
                        'is_vip': is_vip is not None,
                        'is_trusted': is_trusted is not None
                    })
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results

class Kickass(TorrentSite):
    def __init__(self):
        super().__init__(
            "Kickass Torrents",
            [
                "https://kickasstorrents.to",
                "https://kat.cr",
                "https://katcr.co",
                "https://kickass.cm",
                "https://kat.am",
                "https://kickasstorrents.cr"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/usearch/{quote(query)}/{page + 1}/"
    
    def parse_results(self, content, query):
        soup = BeautifulSoup(content, "lxml")
        results = []
        
        try:
            table = soup.find('table', class_="data")
            if not table:
                return results
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 5:
                        continue
                    
                    name_cell = cells[0].find('a', class_="cellMainLink")
                    if not name_cell:
                        continue
                    
                    name = name_cell.get_text().strip()
                    detail_url = urljoin(self.working_url, name_cell['href'])
                    
                    size = cells[1].get_text().strip()
                    seeds = cells[4].get_text().strip()
                    leeches = cells[5].get_text().strip() if len(cells) > 5 else "0"
                    
                    results.append({
                        'name': name,
                        'category': "Unknown",
                        'uploader': "Unknown",
                        'seeds': seeds,
                        'leeches': leeches,
                        'date': "Unknown",
                        'size': size,
                        'detail_url': detail_url,
                        'site': self.name,
                        'is_vip': False,
                        'is_trusted': False
                    })
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results

class Torrentz2(TorrentSite):
    def __init__(self):
        super().__init__(
            "Torrentz2",
            [
                "https://torrentz2.eu",
                "https://torrentz2.is",
                "https://torrentz2.me",
                "https://torrentz2.cc"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/search?f={quote(query)}"
    
    def parse_results(self, content, query):
        soup = BeautifulSoup(content, "lxml")
        results = []
        
        try:
            result_divs = soup.find_all('div', class_="results")[0] if soup.find_all('div', class_="results") else None
            if not result_divs:
                return results
            
            for dl in result_divs.find_all('dl'):
                try:
                    dt = dl.find('dt')
                    dd = dl.find('dd')
                    
                    if not dt or not dd:
                        continue
                    
                    link = dt.find('a')
                    if not link:
                        continue
                    
                    name = link.get_text().strip()
                    detail_url = urljoin(self.working_url, link['href'])
                    
                    # Parse additional info from dd
                    info = dd.get_text().strip()
                    size_match = re.search(r'(\d+\.?\d*\s*[A-Za-z]+)', info)
                    size = size_match.group(1) if size_match else "Unknown"
                    
                    results.append({
                        'name': name,
                        'category': "Unknown",
                        'uploader': "Unknown",
                        'seeds': "Unknown",
                        'leeches': "Unknown",
                        'date': "Unknown",
                        'size': size,
                        'detail_url': detail_url,
                        'site': self.name,
                        'is_vip': False,
                        'is_trusted': False
                    })
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results

class LimeTorrents(TorrentSite):
    def __init__(self):
        super().__init__(
            "LimeTorrents",
            [
                "https://www.limetorrents.info",
                "https://www.limetorrents.cc",
                "https://www.limetorrents.co",
                "https://limetorrents.pro"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/search/all/{quote(query)}/{page + 1}/"
    
    def parse_results(self, content, query):
        soup = BeautifulSoup(content, "lxml")
        results = []
        
        try:
            table = soup.find('table', class_="table2")
            if not table:
                return results
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 6:
                        continue
                    
                    name_cell = cells[0].find('a')
                    if not name_cell:
                        continue
                    
                    name = name_cell.get_text().strip()
                    detail_url = urljoin(self.working_url, name_cell['href'])
                    
                    date = cells[1].get_text().strip()
                    size = cells[2].get_text().strip()
                    seeds = cells[3].get_text().strip()
                    leeches = cells[4].get_text().strip()
                    
                    results.append({
                        'name': name,
                        'category': "Unknown",
                        'uploader': "Unknown",
                        'seeds': seeds,
                        'leeches': leeches,
                        'date': date,
                        'size': size,
                        'detail_url': detail_url,
                        'site': self.name,
                        'is_vip': False,
                        'is_trusted': False
                    })
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results

class RARBG(TorrentSite):
    def __init__(self):
        super().__init__(
            "RARBG",
            [
                "https://rarbg.to",
                "https://rarbgprx.org",
                "https://rarbgenter.org",
                "https://rarbg.is",
                "https://rarbggo.org"
            ]
        )
    
    def build_search_url(self, query, page=0):
        return f"{self.working_url}/torrents.php?search={quote(query)}&page={page + 1}"
    
    def parse_results(self, content, query):
        soup = BeautifulSoup(content, "lxml")
        results = []
        
        try:
            table = soup.find('table', class_="lista2t")
            if not table:
                return results
            
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 8:
                        continue
                    
                    name_cell = cells[1].find('a')
                    if not name_cell:
                        continue
                    
                    name = name_cell.get_text().strip()
                    detail_url = urljoin(self.working_url, name_cell['href'])
                    
                    category = cells[0].get_text().strip()
                    date = cells[2].get_text().strip()
                    size = cells[3].get_text().strip()
                    seeds = cells[4].get_text().strip()
                    leeches = cells[5].get_text().strip()
                    
                    results.append({
                        'name': name,
                        'category': category,
                        'uploader': "Unknown",
                        'seeds': seeds,
                        'leeches': leeches,
                        'date': date,
                        'size': size,
                        'detail_url': detail_url,
                        'site': self.name,
                        'is_vip': False,
                        'is_trusted': False
                    })
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(colored(f"Error parsing {self.name} results: {e}", "red"))
        
        return results

class TorrentSearcher:
    def __init__(self):
        self.sites = [
            PirateBay(),
            Kickass(),
            Torrentz2(),
            LimeTorrents(),
            RARBG()
        ]
        self.working_sites = []
    
    def test_sites(self):
        """Test which sites are working"""
        print(colored("Testing torrent sites...", "cyan"))
        
        for site in self.sites:
            print(f"Testing {site.name}...", end=" ")
            if site.test_connection():
                self.working_sites.append(site)
                print(colored("✓ Working", "green"))
            else:
                print(colored("✗ Not accessible", "red"))
        
        if not self.working_sites:
            print(colored("No working torrent sites found!", "red"))
            return False
        
        print(colored(f"\nFound {len(self.working_sites)} working sites", "green"))
        return True
    
    def search_all_sites(self, query, page_limit=1):
        """Search all working sites"""
        all_results = []
        
        for site in self.working_sites:
            print(colored(f"\nSearching {site.name}...", "yellow"))
            try:
                for page in range(page_limit):
                    results = site.search(query, page)
                    if results:
                        all_results.extend(results)
                        print(colored(f"Found {len(results)} results from {site.name} (page {page + 1})", "green"))
                    else:
                        break  # No more results
            except Exception as e:
                print(colored(f"Error searching {site.name}: {e}", "red"))
        
        return all_results
    
    def format_results(self, results):
        """Format results for display"""
        formatted_results = []
        
        for i, result in enumerate(results, 1):
            name = result['name']
            
            # Apply color coding for VIP/Trusted
            if result['is_vip']:
                name = colored(name, "green")
            elif result['is_trusted']:
                name = colored(name, "magenta")
            
            formatted_results.append([
                result['site'],
                result['category'],
                name,
                f"--{i}--",
                result['uploader'],
                result['size'],
                result['seeds'],
                result['leeches'],
                result['date']
            ])
        
        return formatted_results

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Torrench - Multi-site torrent search tool"
    )
    parser.add_argument(
        "search",
        help="Search query (in English)",
        nargs="?",
        default=None,
        metavar="QUERY"
    )
    parser.add_argument(
        "-p", "--pages",
        type=int,
        help="Number of pages to search per site (default: 1)",
        default=1,
        metavar="N"
    )
    parser.add_argument(
        "-s", "--sites",
        help="Comma-separated list of sites to search (default: all)",
        default="all",
        metavar="SITES"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        help="Maximum number of results to display (default: unlimited)",
        default=None,
        metavar="N"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Enhanced Torrench v2.0"
    )
    
    args = parser.parse_args()
    
    if not args.search:
        print(colored("Please provide a search query in English", "red"))
        print("Example: python enhanced_torrench.py 'Ubuntu 22.04'")
        sys.exit(1)
    
    if args.pages <= 0 or args.pages > 10:
        print(colored("Page limit must be between 1 and 10", "red"))
        sys.exit(1)
    
    print(colored("Enhanced Torrench - Multi-site Torrent Search", "cyan", attrs=["bold"]))
    print(colored("=" * 50, "cyan"))
    
    searcher = TorrentSearcher()
    
    if not searcher.test_sites():
        print(colored("No working torrent sites available. Please check your internet connection or try using a VPN.", "red"))
        sys.exit(1)
    
    print(colored(f"\nSearching for: '{args.search}'", "yellow", attrs=["bold"]))
    
    results = searcher.search_all_sites(args.search, args.pages)
    
    if not results:
        print(colored("No results found!", "red"))
        sys.exit(0)
    
    # Sort results by seeds (descending)
    results.sort(key=lambda x: int(x['seeds']) if x['seeds'].isdigit() else 0, reverse=True)
    
    # Apply limit if specified
    if args.limit:
        results = results[:args.limit]
    
    # Display results
    formatted_results = searcher.format_results(results)
    
    print(colored("\n" + "=" * 80, "cyan"))
    print(colored("SEARCH RESULTS", "cyan", attrs=["bold"]))
    print(colored("=" * 80, "cyan"))
    
    headers = ['SITE', 'CATEGORY', 'NAME', 'INDEX', 'UPLOADER', 'SIZE', 'SEEDS', 'LEECHES', 'DATE']
    table = tabulate(formatted_results, headers=headers, tablefmt="grid")
    print(table)
    
    print(colored(f"\nTotal results: {len(results)}", "green", attrs=["bold"]))
    print(colored("Green = VIP | Magenta = Trusted", "yellow"))
    
    # Interactive detail viewing
    print(colored("\nEnter torrent index to view details (0 to exit):", "cyan"))
    
    while True:
        try:
            choice = input(colored("Index > ", "blue")).strip()
            
            if choice == '0' or choice.lower() == 'exit':
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(results):
                    result = results[index]
                    print(colored(f"\nTorrent Details:", "yellow", attrs=["bold"]))
                    print(colored("-" * 40, "yellow"))
                    print(f"Name: {result['name']}")
                    print(f"Site: {result['site']}")
                    print(f"Category: {result['category']}")
                    print(f"Uploader: {result['uploader']}")
                    print(f"Size: {result['size']}")
                    print(f"Seeds: {result['seeds']}")
                    print(f"Leeches: {result['leeches']}")
                    print(f"Date: {result['date']}")
                    print(f"Detail URL: {result['detail_url']}")
                    print(colored("-" * 40, "yellow"))
                else:
                    print(colored("Invalid index! Please try again.", "red"))
            except ValueError:
                print(colored("Please enter a valid number!", "red"))
                
        except KeyboardInterrupt:
            break
    
    print(colored("\nThank you for using Enhanced Torrench!", "green", attrs=["bold"]))

if __name__ == "__main__":
    main()
