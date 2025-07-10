import requests
import gzip
import xml.etree.ElementTree as ET
import logging
import time

logging.basicConfig(level=logging.INFO, format='> %(message)s')

def download_sitemap(url, retry_count=0):
    try:
        response = requests.get(url, timeout=30) # Increased timeout for large files
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download sitemap from {url}: {e}")
        if retry_count < 3:
            time.sleep(5 * (2 ** retry_count)) # Exponential backoff
            return download_sitemap(url, retry_count + 1)
        return None

def parse_sitemap_index(sitemap_index_content):
    sitemap_urls = []
    try:
        root = ET.fromstring(sitemap_index_content)
        for sitemap in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
            loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is not None:
                sitemap_urls.append(loc.text)
    except ET.ParseError as e:
        logging.error(f"Failed to parse sitemap index: {e}")
    return sitemap_urls

def parse_app_sitemap(app_sitemap_content):
    app_data_list = []
    try:
        root = ET.fromstring(app_sitemap_content)
        for url_element in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is None: continue

            app_url = loc.text
            app_id_match = re.search(r'/id(\d+)', app_url)
            app_id = app_id_match.group(1) if app_id_match else None

            if not app_id: continue

            app_entry = {
                'app_id': app_id,
                'url': app_url,
                'hreflangs': []
            }

            for xhtml_link in url_element.findall('{http://www.w3.org/1999/xhtml}link'):
                hreflang = xhtml_link.get('hreflang')
                href = xhtml_link.get('href')
                if hreflang and href:
                    app_entry['hreflangs'].append({'hreflang': hreflang, 'href': href})
            app_data_list.append(app_entry)

    except ET.ParseError as e:
        logging.error(f"Failed to parse app sitemap: {e}")
    return app_data_list

def get_all_app_urls_from_sitemaps(main_sitemap_url):
    all_app_urls = []
    logging.info(f"Downloading main sitemap index from {main_sitemap_url}")
    main_sitemap_content = download_sitemap(main_sitemap_url)

    if main_sitemap_content:
        sitemap_urls = parse_sitemap_index(main_sitemap_content)
        logging.info(f"Found {len(sitemap_urls)} app sitemaps.")

        for sitemap_url in sitemap_urls:
            logging.info(f"Downloading app sitemap from {sitemap_url}")
            gzipped_content = download_sitemap(sitemap_url)
            if gzipped_content:
                try:
                    decompressed_content = gzip.decompress(gzipped_content).decode('utf-8')
                    app_data = parse_app_sitemap(decompressed_content)
                    all_app_urls.extend(app_data)
                    logging.info(f"Processed {len(app_data)} apps from {sitemap_url}")
                except Exception as e:
                    logging.error(f"Failed to decompress or parse {sitemap_url}: {e}")
    return all_app_urls
