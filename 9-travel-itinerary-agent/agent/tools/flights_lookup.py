"""Flights lookup tool using Apify actor."""

from apify_client import ApifyClient
import os

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")


def flights_lookup(
    from_location: str,
    to_location: str,
    departure_date: str,
    return_date: str = "",
    trip_type: str = "ONEWAY",
    adults: int = 1,
    cabin_class: str = "ECONOMY",
    max_items: int = 10
) -> dict:
    """Search flights via Apify actor 23hq58TAuJyQtdGCf.
    
    Args:
        from_location: Origin city/airport (e.g., "New York", "JFK")
        to_location: Destination city/airport (e.g., "London", "LHR")
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (required for ROUNDTRIP)
        trip_type: "ONEWAY" or "ROUNDTRIP"
        adults: Number of adult passengers (1-9)
        cabin_class: "ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", or "FIRST"
        max_items: Maximum number of flight options to return (default: 10)
        
    Returns:
        Dictionary with flight results: {"flights": [...], "count": int}
    """
    client = ApifyClient(APIFY_TOKEN)
    
    run_input = {
        "tripType": trip_type,
        "fromLocationQuery": from_location,
        "toLocationQuery": to_location,
        "departureDate": departure_date,
        "numberOfAdults": adults,
        "cabinClass": cabin_class,
        "sortType": "BEST",
        "isDirectFlight": False,
        "maxItems": max_items,
        "proxyConfiguration": {"useApifyProxy": False}
    }
    
    if trip_type == "ROUNDTRIP" and return_date:
        run_input["returnDate"] = return_date
    
    # Run the actor and wait for completion
    run = client.actor("23hq58TAuJyQtdGCf").call(run_input=run_input)
    
    # Fetch results from the dataset
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    
    return {"flights": items, "count": len(items)}