#!/usr/bin/env python3
"""
Simple test script for Noble TLS custom profiles.
Tests Edge 137 profile by loading it directly and making a request to tls.peet.ws API.
"""

import asyncio
import json
import sys
import os



# Add the noble_tls package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    # Import directly to avoid circular imports
    from noble_tls.profiles.profiles import ProfileLoader
    from noble_tls.sessions import Session
    from noble_tls.utils.identifiers import Client
    from noble_tls.profiles.session_factory import create_session
    from noble_tls.utils.custom_identifiers import CustomClient
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the correct directory and noble_tls is properly installed")
    import traceback
    traceback.print_exc()
    sys.exit(1)


async def test_chrome_137_profile():
    """
    Test the Edge 137 custom profile by loading it and making a request to tls.peet.ws API.
    
    Returns:
        dict: The fingerprint data from tls.peet.ws API
    """
    print("🚀 Testing Safari 18.3 iOS Custom Profile")
    print("=" * 50)
    
    try:
        # Load the Edge 137 profile directly
        print("📋 Loading Safari 18.3 iOS profile...")
        profile_loader = ProfileLoader()
        
        # Load the chrome profile by name (Chrome has complete TLS data, Edge profile is incomplete)
        profile_name = "edge_137_windows"
        session_params = profile_loader.load_profile(profile_name)
        print('-------------------------------- Session Params --------------------------------')
        print(session_params)
        
      
        
      
        
        # Add a client identifier to avoid "Custom-1" error
        #valid_session_params['client'] = Client.CHROME_133
        
        #session = Session(**valid_session_params)
        session = create_session(CustomClient.CHROME_137)
        # Set User-Agent from profile
        if session_params.get('user_agent'):
            session.headers['User-Agent'] = session_params['user_agent']
        
        print("✅ Session created successfully!")
       
        
        # Make request to tls.peet.ws API
        print(f"\n🌐 Making request to https://tls.peet.ws/api/all...")
        response = await session.get("https://tls.peet.ws/api/all")
        
        print(f"✅ Request successful!")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {len(response.headers)} headers")
        
        # Parse and analyze the response
        if response.status_code == 200:
            fingerprint_data = response.json()
            print(f"✅ JSON response parsed successfully")
            
            # Extract key fingerprinting information
            print(f"\n🔍 Fingerprint Analysis:")
            
            # Check response format - try both nested and direct formats
            if 'tls.peet.ws' in fingerprint_data:
                # Nested format
                tls_data = fingerprint_data['tls.peet.ws']
                tls_info = tls_data.get('tls', {})
                h2_info = tls_data.get('http2', {})
                user_agent = tls_data.get('user_agent', 'N/A')
            else:
                # Direct format
                tls_info = fingerprint_data.get('tls', {})
                h2_info = fingerprint_data.get('http2', {})
                user_agent = fingerprint_data.get('user_agent', 'N/A')
            
            # TLS information
            if tls_info:
                print(f"  📊 TLS Fingerprints:")
                print(f"    JA3: {tls_info.get('ja3', 'N/A')}")
                print(f"    JA3 Hash: {tls_info.get('ja3_hash', 'N/A')}")
                print(f"    JA4: {tls_info.get('ja4', 'N/A')}")
                print(f"    TLS Version: {tls_info.get('tls_version_negotiated', 'N/A')}")
                print(f"    Peetprint_hash: {tls_info.get('peetprint_hash', 'N/A')}")
            
            # HTTP/2 information
            if h2_info:
                print(f"  🔗 HTTP/2 Fingerprints:")
                print(f"    Akamai Fingerprint: {h2_info.get('akamai_fingerprint', 'N/A')}")
                print(f"    Akamai Hash: {h2_info.get('akamai_fingerprint_hash', 'N/A')}")
            
            # User Agent
            print(f"  🌐 User Agent: {user_agent}")
            
            return fingerprint_data
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response text: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """
    Main function to run the Edge 137 profile test.
    """
    print("🧪 Noble TLS Custom Profile Test")
    print("Testing Chrome 137 profile with tls.peet.ws API")
    print("=" * 60)
    
    try:
        # Run the async test
        result = asyncio.run(test_chrome_137_profile())
        
        if result:
            print(f"\n✅ Test completed successfully!")
            print(f"📊 Fingerprint data collected: {len(result)} top-level keys")
            
            # Show a summary of the collected data
            if result:
                tls_info = result.get('tls', {})
                print(f"🔍 Summary:")
                print(f"  JA3 Hash: {tls_info.get('ja3_hash', 'N/A')}")
                print(f"  TLS Version: {tls_info.get('tls_version_negotiated', 'N/A')}")
                print(f"  User Agent Match: {result.get('user_agent', 'N/A')}")
                print(f"  Peetprint_hash: {result.get('peetprint_hash', 'N/A')}")
                print(json.dumps(result, indent=2))
        else:
            print(f"\n❌ Test failed - no data collected")
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
