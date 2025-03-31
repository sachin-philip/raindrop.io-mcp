from typing import Any, List, Optional
import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Raindrop-Server")

# Constants
RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"
RAINDROP_TOKEN = os.environ.get("RAINDROP_TOKEN")

async def make_raindrop_request(url: str, token: str, method: str = "GET", data: dict = None) -> dict[str, Any] | None:
    """Make a request to the Raindrop.io API with proper error handling."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            else:
                print(f"Unsupported method: {method}")
                return None
                
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making Raindrop request: {e}")
            return None


def format_bookmark(item: dict) -> str:
    """Format a Raindrop bookmark into a readable string."""
    return f"""
Title: {item.get('title', 'Untitled')}
URL: {item.get('link', 'No URL')}
Tags: {', '.join(item.get('tags', [])) or 'No tags'}
Created: {item.get('created', 'Unknown date')}
Description: {item.get('excerpt', 'No description available')}
"""

@mcp.tool()
async def get_latest_feed(count: int = 10) -> str:
    """Get latest bookmarks from Raindrop.io feed.

    Args:
        count: Number of bookmarks to fetch (default: 10)
    """
    url = f"{RAINDROP_API_BASE}/raindrops/0?perpage={count}&sort=-created"
    data = await make_raindrop_request(url, RAINDROP_TOKEN)

    if not data or "items" not in data:
        return "Unable to fetch bookmarks or no bookmarks found."

    if not data["items"]:
        return "No bookmarks found in your collection."

    bookmarks = [format_bookmark(item) for item in data["items"]]
    return "\n---\n".join(bookmarks)


@mcp.tool()
async def add_bookmark(url: str, title: str = "", description: str = "", tags: List[str] = None, collection_id: int = 0) -> str:
    """Add a new bookmark to Raindrop.io
    
    Args:
        url: The URL to bookmark (required)
        title: Title for the bookmark (optional, will be extracted from URL if not provided)
        description: Description/excerpt for the bookmark (optional)
        tags: List of tags to apply to the bookmark (optional)
        collection_id: ID of the collection to add the bookmark to (default: 0 for Unsorted)
    """
    if not url:
        return "Error: URL is required"
        
    raindrop_data = {
        "link": url,
        "collection": {"$id": collection_id}
    }
    
    if title:
        raindrop_data["title"] = title
    if description:
        raindrop_data["excerpt"] = description
    if tags:
        raindrop_data["tags"] = tags
    
    endpoint = f"{RAINDROP_API_BASE}/raindrop"
    response = await make_raindrop_request(endpoint, RAINDROP_TOKEN, method="POST", data=raindrop_data)
    
    if not response or "item" not in response:
        return "Failed to add bookmark. Please check the URL and try again."
    
    return f"Bookmark successfully added:\n{format_bookmark(response['item'])}"


@mcp.tool()
async def search_by_tag(tag: str, collection_id: int = 0, count: int = 10, from_date: str = "", to_date: str = "") -> str:
    """Search for bookmarks with a specific tag in Raindrop.io with optional date range filtering
    
    Args:
        tag: The tag to search for (required)
        collection_id: ID of the collection to search in (default: 0 for all collections)
        count: Maximum number of bookmarks to return (default: 10)
        from_date: Start date in YYYY-MM-DD format (optional)
        to_date: End date in YYYY-MM-DD format (optional)
    """
    if not tag:
        return "Error: Tag is required"
    
    # Build search filters
    search_filters = [f"-tags:\"{tag}\""]
    
    # Add date range filters if provided
    if from_date:
        search_filters.append(f"created>={from_date}")
    if to_date:
        search_filters.append(f"created<={to_date}")
    
    # Combine all search filters
    search_query = " ".join(search_filters)
    
    url = f"{RAINDROP_API_BASE}/raindrops/{collection_id}?perpage={count}&search={search_query}&sort=-created"
    data = await make_raindrop_request(url, RAINDROP_TOKEN)
    
    if not data or "items" not in data:
        return "Unable to fetch bookmarks or no bookmarks found with this tag."
    
    if not data["items"]:
        return f"No bookmarks found with tag '{tag}' within the specified criteria."
    
    bookmarks = [format_bookmark(item) for item in data["items"]]
    result_msg = f"Found {len(data['items'])} bookmarks with tag '{tag}'"
    if from_date or to_date:
        date_range = f" (Date range: {from_date or 'any'} to {to_date or 'any'})"
        result_msg += date_range
    return result_msg + ":\n\n" + "\n---\n".join(bookmarks)


@mcp.tool()
async def search_bookmarks(query: str, collection_id: int = 0, count: int = 10, from_date: str = "", to_date: str = "") -> str:
    """Search for bookmarks by keyword/text in Raindrop.io with optional date range filtering
    
    Args:
        query: The search term to look for in bookmarks (required)
        collection_id: ID of the collection to search in (default: 0 for all collections)
        count: Maximum number of bookmarks to return (default: 10)
        from_date: Start date in YYYY-MM-DD format (optional)
        to_date: End date in YYYY-MM-DD format (optional)
    """
    if not query:
        return "Error: Search query is required"
    
    # Build search filters
    search_filters = [f"\"{query}\""]
    
    # Add date range filters if provided
    if from_date:
        search_filters.append(f"created>={from_date}")
    if to_date:
        search_filters.append(f"created<={to_date}")
    
    # Combine all search filters
    search_query = " ".join(search_filters)
    
    url = f"{RAINDROP_API_BASE}/raindrops/{collection_id}?perpage={count}&search={search_query}&sort=-created"
    data = await make_raindrop_request(url, RAINDROP_TOKEN)
    
    if not data or "items" not in data:
        return "Unable to fetch bookmarks or no bookmarks found for your search."
    
    if not data["items"]:
        return f"No bookmarks found matching '{query}' within the specified criteria."
    
    bookmarks = [format_bookmark(item) for item in data["items"]]
    result_msg = f"Found {len(data['items'])} bookmarks matching '{query}'"
    if from_date or to_date:
        date_range = f" (Date range: {from_date or 'any'} to {to_date or 'any'})"
        result_msg += date_range
    return result_msg + ":\n\n" + "\n---\n".join(bookmarks)


if __name__ == "__main__":
    mcp.run(transport='stdio')