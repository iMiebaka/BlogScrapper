from decouple import config
from scrapper.bot import LinkedInBlogScraper
import argparse


if __name__ == "__main__":

    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="A url to linkedin.")

    # Add arguments
    parser.add_argument("url_path", type=str, help="Input file or text")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    # Parse arguments
    args = parser.parse_args()



    email = config("LINKEDIN_EMAIL")
    password = config("LINKEDIN_PASSWORD")

    scraper = LinkedInBlogScraper(email, password)
    try:
        scraper.login()
        result, blogs_found, total_articles = scraper.scrape_articles(url_path=args.url_path)
        print(f"Total articles scraped: {total_articles}")
        print(f"Blogs found: {blogs_found}")
        print(f"Articles links scraped: {len(result)}")
        print(result)

    finally:
        scraper.close()
