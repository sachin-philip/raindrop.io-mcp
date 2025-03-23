from typing import Any, List, Optional
import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Raindrop-Server")

# Constants
RAINDROP_API_BASE = "https://api.raindrop.io/rest/v1"
token = os.environ.get("RAINDROP_TOKEN")

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
    data = await make_raindrop_request(url, token)

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
        
    # Prepare the data for creating a new raindrop
    raindrop_data = {
        "link": url,
        "collection": {"$id": collection_id}
    }
    
    # Add optional fields if provided
    if title:
        raindrop_data["title"] = title
    if description:
        raindrop_data["excerpt"] = description
    if tags:
        raindrop_data["tags"] = tags
    
    endpoint = f"{RAINDROP_API_BASE}/raindrop"
    response = await make_raindrop_request(endpoint, token, method="POST", data=raindrop_data)
    
    if not response or "item" not in response:
        return "Failed to add bookmark. Please check the URL and try again."
    
    # Return a success message with the formatted bookmark
    return f"Bookmark successfully added:\n{format_bookmark(response['item'])}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')