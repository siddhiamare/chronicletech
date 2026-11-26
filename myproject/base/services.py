import json
import logging
import urllib.request
import urllib.error
from django.core.cache import cache

logger = logging.getLogger(__name__)

SUPPORTED_TOPICS = {
    'all': 'technology',
    'ai': 'ai',
    'python': 'python',
    'cloud': 'cloud',
    'devops': 'devops',
    'security': 'cybersecurity',
}


def fetch_live_tech_news(topic='all', limit=10, force_refresh=False):
    """
    Fetch real-time technology articles from live developer APIs.
    Implements in-memory caching (TTL 300s) to prevent external rate limits,
    with query-based cache busting and graceful network fallbacks.
    """
    api_tag = SUPPORTED_TOPICS.get(topic, 'technology')
    cache_key = f"live_tech_news_{api_tag}_{limit}"

    # Return cached feed unless explicitly refreshed
    if not force_refresh:
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return {
                'items': cached_data,
                'source': 'cache',
                'is_live': True,
                'topic': topic,
                'api_tag': api_tag,
            }

    url = f"https://dev.to/api/articles?tag={api_tag}&per_page={limit}"
    headers = {
        'User-Agent': 'ChronicleTech/1.0 (Portfolio Project; Live Wire Aggregator)',
        'Accept': 'application/json',
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as response:
            if response.status == 200:
                raw_data = json.loads(response.read().decode('utf-8'))
                normalized_items = []

                for item in raw_data:
                    # Filter out invalid entries
                    if not item.get('title') or not item.get('url'):
                        continue

                    user = item.get('user', {}) or {}
                    tags = item.get('tag_list', [])
                    if isinstance(tags, str):
                        tags = [t.strip() for t in tags.split(',') if t.strip()]

                    normalized_items.append({
                        'id': item.get('id'),
                        'title': item.get('title'),
                        'description': item.get('description', ''),
                        'url': item.get('url'),
                        'cover_image': item.get('cover_image'),
                        'readable_date': item.get('readable_publish_date') or 'Recent',
                        'reading_time': item.get('reading_time_minutes', 3),
                        'reactions': item.get('positive_reactions_count', 0),
                        'author_name': user.get('name') or user.get('username') or 'Tech Contributor',
                        'author_username': user.get('username', ''),
                        'author_image': user.get('profile_image_90') or user.get('profile_image'),
                        'tags': tags[:4],
                    })

                # Cache fresh results for 5 minutes (300 seconds)
                cache.set(cache_key, normalized_items, timeout=300)

                return {
                    'items': normalized_items,
                    'source': 'live_api',
                    'is_live': True,
                    'topic': topic,
                    'api_tag': api_tag,
                }
            else:
                logger.warning(f"Live tech news API returned status {response.status}")

    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception) as exc:
        logger.error(f"Error fetching live tech news from {url}: {exc}")

        # Attempt to return stale cache on network failure
        stale_data = cache.get(cache_key)
        if stale_data:
            return {
                'items': stale_data,
                'source': 'stale_cache',
                'is_live': True,
                'topic': topic,
                'api_tag': api_tag,
            }

    # Complete fallback if offline or API unreachable
    return {
        'items': [],
        'source': 'offline',
        'is_live': False,
        'topic': topic,
        'api_tag': api_tag,
    }
