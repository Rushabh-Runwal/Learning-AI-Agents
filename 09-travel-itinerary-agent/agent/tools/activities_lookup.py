"""Activities lookup tool using Apify actor."""

from apify_client import ApifyClient
import os

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")


def activities_lookup(
    country_code: str = "US",
    geo_hash: str = "",
    distance: int = 100,
    max_items: int = 50,
    concerts: bool = True
) -> dict:
    """Search events/activities via Apify actor PVOL6Qt15hukudGiu.
    
    Args:
        country_code: Two-letter country code (e.g., "US", "GB", "FR")
        geo_hash: Geohash for location-based search (optional)
        distance: Search radius in miles (default: 100)
        max_items: Maximum number of events to return (default: 50, max: 200)
        concerts: Include concert events (default: True)
        
    Returns:
        Dictionary with event results: {"events": [...], "count": int}
    """
    client = ApifyClient(APIFY_TOKEN)
    
    run_input = {
        "concerts": concerts,
        "sortBy": "date",
        "maxItems": max_items,
        "countryCode": country_code,
        "distance": distance,
        "includeTBA": "yes",
        "includeTBD": "yes"
    }
    
    if geo_hash:
        run_input["geoHash"] = geo_hash
    
    # Run the actor and wait for completion
    run = client.actor("PVOL6Qt15hukudGiu").call(run_input=run_input)
    
    # Fetch results from the dataset
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    
    return {"events": items, "count": len(items)}