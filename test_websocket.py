"""
Quick test script to verify WebSocket servers are running
Run this after starting the main application
"""

import asyncio
import websockets
import json

async def test_websocket(uri, name):
    """Test a WebSocket connection"""
    try:
        print(f"Testing {name} at {uri}...")
        async with websockets.connect(uri) as websocket:
            print(f"✅ {name} - Connected successfully!")
            
            # Send a test message
            test_message = {"test": "connection", "server": name}
            await websocket.send(json.dumps(test_message))
            print(f"✅ {name} - Message sent")
            
            # Wait for response (with timeout)
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                print(f"✅ {name} - Received: {response}")
            except asyncio.TimeoutError:
                print(f"⚠️  {name} - No response (this is OK for one-way servers)")
            
            return True
    except ConnectionRefusedError:
        print(f"❌ {name} - Connection refused. Is the server running?")
        return False
    except Exception as e:
        print(f"❌ {name} - Error: {e}")
        return False

async def main():
    """Test all WebSocket servers"""
    print("🧪 Testing WebSocket Servers...\n")
    
    servers = [
        ("ws://localhost:8001", "Profile Data WebSocket"),
        ("ws://localhost:8002", "Consuming Apps WebSocket"),
        ("ws://localhost:8003", "State Transfer WebSocket"),
    ]
    
    results = []
    for uri, name in servers:
        result = await test_websocket(uri, name)
        results.append(result)
        print()
    
    # Summary
    print("=" * 50)
    if all(results):
        print("✅ All WebSocket servers are running correctly!")
    else:
        print("⚠️  Some servers are not responding.")
        print("Make sure to run: python src/main.py")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

