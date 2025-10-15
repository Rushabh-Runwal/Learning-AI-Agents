"""Hotels lookup tool using Apify actor."""

from apify_client import ApifyClient
import os

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")


def hotels_lookup(
    location: str,
    check_in: str = "",
    check_out: str = "",
    adults: int = 2,
    limit: int = 10,
    sort: str = "recommended"
) -> dict:
    """Search hotels via Apify actor pK2iIKVVxERtpwXMy.
    
    Args:
        location: City or region name (e.g., "Paris", "Bali")
        check_in: Check-in date in YYYY-MM-DD format (optional)
        check_out: Check-out date in YYYY-MM-DD format (optional)
        adults: Number of adults for room 1 (default: 2)
        limit: Maximum number of hotels to return (default: 10)
        sort: Sorting option - "recommended", "price_low", "price_high", 
              "distance", "review", "rating"
        
    Returns:
        Dictionary with hotel results: {"hotels": [...], "count": int}
    """
    client = ApifyClient(APIFY_TOKEN)
    
    run_input = {
        "location": [location],
        "limit": limit,
        "sort": sort
    }
    
    if check_in:
        run_input["check_in"] = check_in
    if check_out:
        run_input["check_out"] = check_out
    if adults:
        run_input["adults:0"] = adults
    
    # Run the actor and wait for completion
    run = client.actor("pK2iIKVVxERtpwXMy").call(run_input=run_input)
    
    # Fetch results from the dataset
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    
    return {"hotels": items, "count": len(items)}