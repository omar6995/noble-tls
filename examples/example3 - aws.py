#!/usr/bin/env python3

"""
Example 3 - AWS Mode

This example demonstrates how to use the isAws=True parameter to load 
TLS client libraries from the data directory instead of downloading them.
This is useful for AWS Lambda, Docker containers, or restricted environments.
"""

import asyncio
import noble_tls


async def main():
    print("Noble TLS - AWS Mode Example")
    print("=" * 40)
    
    # Create a session with AWS mode enabled
    # This will load .so/.dll/.dylib files from the noble_tls/data/ directory
    # instead of trying to download them from GitHub
    session = noble_tls.Session(
        client=noble_tls.Client.CHROME_131,  # Use a preset client
        isAws=True  # Enable AWS mode - load from data directory
    )
    
    print(f"AWS mode enabled: {session.isAws}")
    print("TLS client library loaded from data directory")
    
    try:
        # Make a test request
        response = await session.get("https://httpbin.org/get")
        print(f"✓ Request successful!")
        print(f"Status: {response.status_code}")
        print(f"Response length: {len(response.text)} characters")
        
        # Print some response data
        data = response.json()
        print(f"Origin IP: {data.get('origin', 'N/A')}")
        print(f"User-Agent: {data.get('headers', {}).get('User-Agent', 'N/A')}")
        
    except Exception as e:
        print(f"✗ Request failed: {e}")
        print("Note: This might fail if AWS assets are not properly configured")
    
    print("\n" + "=" * 40)
    print("AWS mode example completed")


if __name__ == "__main__":
    asyncio.run(main())
