import os
import time
from typing import Dict, List, Optional, Tuple

import requests


class FirecrawlError(Exception):
    """Custom exception for Firecrawl API errors."""


class FirecrawlClient:
    """
    Minimal Firecrawl API client.

    Environment variables:
      - FIRECRAWL_API_KEY: API key for Firecrawl

    Notes:
      - Uses the REST endpoint: POST https://api.firecrawl.dev/v1/scrape
      - Request body accepts at least: { "url": string, "formats": ["markdown" | "html"] }
      - Response shape can evolve; this client tries to be resilient and supports
        common shapes observed in Firecrawl SDKs (data.markdown/html or top-level fields).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.firecrawl.dev",
        timeout: int = 60,
        session: Optional[requests.Session] = None,
    ) -> None:
        # Try loading from .env if present
        try:
            from dotenv import load_dotenv  # type: ignore
            # Load .env from project root if available
            load_dotenv()
        except Exception:
            # dotenv is optional; if not installed, skip without failing
            pass

        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise FirecrawlError(
                "FIRECRAWL_API_KEY is not set. Export it or pass api_key explicitly."
            )
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def scrape_url(
        self,
        url: str,
        formats: Optional[List[str]] = None,
        only_main_content: Optional[bool] = None,
        retry: int = 2,
        backoff: float = 1.5,
    ) -> Dict:
        """
        Call Firecrawl's scrape endpoint for a single URL.

        Args:
          url: The webpage URL to scrape.
          formats: The desired output formats. Common values: ["markdown"], ["html"].
          only_main_content: If supported by the API, hint to extract only main content.
          retry: Number of retries for transient errors.
          backoff: Exponential backoff factor between retries.

        Returns:
          Parsed JSON response as dict.
        """

        if not url or not isinstance(url, str):
            raise ValueError("url must be a non-empty string")

        payload: Dict[str, object] = {"url": url}
        if formats:
            payload["formats"] = formats
        if only_main_content is not None:
            payload["onlyMainContent"] = only_main_content

        endpoint = f"{self.base_url}/v1/scrape"
        attempt = 0
        while True:
            attempt += 1
            try:
                resp = self.session.post(
                    endpoint, json=payload, headers=self._headers(), timeout=self.timeout
                )
                if resp.status_code >= 400:
                    # Try to include server-provided message
                    try:
                        err_json = resp.json()
                    except Exception:
                        err_json = None
                    msg = (
                        f"Firecrawl scrape failed: {resp.status_code} {resp.reason}. "
                        f"Response: {err_json or resp.text[:500]}"
                    )
                    # Retry on 429/5xx with backoff
                    if resp.status_code in (429, 500, 502, 503, 504) and attempt <= retry + 1:
                        time.sleep(backoff ** (attempt - 1))
                        continue
                    raise FirecrawlError(msg)

                return resp.json()
            except requests.RequestException as e:
                if attempt <= retry + 1:
                    time.sleep(backoff ** (attempt - 1))
                    continue
                raise FirecrawlError(f"Network error calling Firecrawl: {e}") from e

    @staticmethod
    def extract_content_fields(data: Dict) -> Tuple[Optional[str], Optional[str]]:
        """
        Attempt to normalize output from Firecrawl across potential response shapes.

        Returns a tuple (markdown, html).
        Either can be None if not present.
        """
        if not isinstance(data, dict):
            return None, None

        # Common shape: { success, data: { markdown, html, ... } }
        node = data.get("data") if isinstance(data.get("data"), dict) else data

        md = node.get("markdown") if isinstance(node, dict) else None
        html = node.get("html") if isinstance(node, dict) else None

        # Fallbacks: sometimes "content" holds markdown-like text
        if md is None and isinstance(node, dict):
            content = node.get("content") or node.get("text")
            if isinstance(content, str):
                md = content

        return md, html
