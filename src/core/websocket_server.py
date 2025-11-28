"""
WebSocket servers for communication
- ProfileDataWebSocketServer: Sends profile data
- ConsumingAppsWebSocketServer: Receives messages for consuming apps
- StateTransferWebSocketServer: Handles state transfer to headful browser
"""

import asyncio
import websockets
import json
from typing import Set

class ProfileDataWebSocketServer:
    """WebSocket server for sending profile data"""
    
    def __init__(self, url: str):
        self.url = url
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
    
    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"✅ Profile data client connected. Total: {len(self.clients)}")
    
    async def unregister(self, websocket):
        self.clients.discard(websocket)
        print(f"❌ Profile data client disconnected. Total: {len(self.clients)}")
    
    async def broadcast_profile_data(self, profile_data: dict):
        """Broadcast profile data to all connected clients"""
        if self.clients:
            message = json.dumps(profile_data)
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )
    
    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                # Handle incoming messages if needed
                pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start the WebSocket server"""
        host, port = self.url.replace('ws://', '').split(':')
        self.server = await websockets.serve(self.handler, host, int(port))
        print(f"✅ ProfileDataWebSocketServer started on {self.url}")

class ConsumingAppsWebSocketServer:
    """WebSocket server for consuming applications"""
    
    def __init__(self, url: str):
        self.url = url
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
    
    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"✅ Consuming app client connected. Total: {len(self.clients)}")
    
    async def unregister(self, websocket):
        self.clients.discard(websocket)
        print(f"❌ Consuming app client disconnected. Total: {len(self.clients)}")
    
    async def send_message(self, message_data: dict):
        """Send message data to consuming apps"""
        if self.clients:
            message = json.dumps(message_data)
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )
    
    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                # Handle incoming messages if needed
                pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start the WebSocket server"""
        host, port = self.url.replace('ws://', '').split(':')
        self.server = await websockets.serve(self.handler, host, int(port))
        print(f"✅ ConsumingAppsWebSocketServer started on {self.url}")

class StateTransferWebSocketServer:
    """WebSocket server for state transfer to headful browser"""
    
    def __init__(self, url: str):
        self.url = url
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
    
    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"✅ State transfer client connected. Total: {len(self.clients)}")
    
    async def unregister(self, websocket):
        self.clients.discard(websocket)
        print(f"❌ State transfer client disconnected. Total: {len(self.clients)}")
    
    async def transfer_state(self, state_data: dict):
        """Transfer state to headful browser for obstacle resolution"""
        if self.clients:
            message = json.dumps(state_data)
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )
    
    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                # Handle state transfer requests
                pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start the WebSocket server"""
        host, port = self.url.replace('ws://', '').split(':')
        self.server = await websockets.serve(self.handler, host, int(port))
        print(f"✅ StateTransferWebSocketServer started on {self.url}")

