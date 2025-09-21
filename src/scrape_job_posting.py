import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scrape a job posting URL using Firecrawl's Scrape API and print the content.",
        epilog=(
            "Set FIRECRAWL_API_KEY in your environment. Example:\n"
            "  export FIRECRAWL_API_KEY=sk-...\n\n"
            "Examples:\n"
            "  python -m src.scrape_job_posting https://example.com/job/123\n"
            "  python -m src.scrape_job_posting https://example.com/job/123\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("url", help="Job posting URL to scrape")
    parser.add_argument(
        "--only-main-content",
        action="store_true",
        help="If supported, request only the main content of the page",
    )

    args = parser.parse_args()

    try:
        # Lazy import so that --help can run even if dependencies aren't installed yet
        from firecrawl_client import FirecrawlClient, FirecrawlError  # type: ignore

        client = FirecrawlClient()
        resp = client.scrape_url(args.url, formats=["markdown"], only_main_content=args.only_main_content)
        md, html = FirecrawlClient.extract_content_fields(resp)
        content = md or html or ""
        if not content:
            print("No content returned by Firecrawl.", file=sys.stderr)
            return 3
        print(content)
        return 0
    except Exception as e:
        # Keep specific FirecrawlError messaging if available
        try:
            from firecrawl_client import FirecrawlError  # type: ignore
        except Exception:
            FirecrawlError = tuple()  # type: ignore
        if isinstance(e, FirecrawlError):
            print(f"Error: {e}", file=sys.stderr)
            return 2
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
