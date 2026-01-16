"""
ChatKit endpoint for processing chat requests.

This module provides the /chatkit endpoint that handles all ChatKit
protocol requests, including message streaming and widget rendering.

Reference: reference-phase3/backend/routers/chatkit.py
"""

import logging
from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response, StreamingResponse, JSONResponse
from chatkit.server import StreamingResult

from ...auth.dependencies import get_current_user_id
from ...services.chatkit_server import TaskChatKitServer
from ...services.chatkit_store import MemoryStore

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chatkit"])

# Global cache for ChatKit server instances (singleton per user)
# This prevents creating new MCP server subprocesses for each request
_chatkit_servers: dict[str, TaskChatKitServer] = {}


def get_current_user_info(user_id: str = Depends(get_current_user_id)) -> dict:
    """
    Extract user information from JWT token for ChatKit context.

    Args:
        user_id: User ID from JWT verification

    Returns:
        dict: User information (id, name)
    """
    return {
        "id": user_id,
        "name": "there",  # Could be enhanced to get actual user name
    }


async def _get_chatkit_server(user_id: str) -> TaskChatKitServer:
    """Get or create a cached ChatKit server instance for the user.

    This function implements a singleton pattern to ensure the MCP server
    subprocess is created once and reused across requests. This prevents
    timeout issues caused by repeatedly starting/stopping the subprocess.

    Args:
        user_id: User ID for store initialization

    Returns:
        TaskChatKitServer: Cached or newly created server instance
    """
    # Check if we already have a server for this user
    if user_id in _chatkit_servers:
        logger.info(f"Reusing cached ChatKit server for user {user_id}")
        return _chatkit_servers[user_id]

    # Create new server instance
    logger.info(f"Creating new ChatKit server with MemoryStore for user {user_id}")
    store = MemoryStore(user_id=user_id)
    server = TaskChatKitServer(store=store)

    # Cache the server instance
    _chatkit_servers[user_id] = server

    return server


@router.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    user_info: dict = Depends(get_current_user_info),
) -> Response:
    """
    ChatKit endpoint that processes all chat requests.

    This endpoint:
    1. Authenticates the user via JWT
    2. Extracts the request payload
    3. Processes it through the ChatKit server (cached per user)
    4. Returns streaming (SSE) or JSON response

    Args:
        request: FastAPI request object
        user_info: Authenticated user information from JWT

    Returns:
        Response: StreamingResponse for SSE or JSON Response
    """
    user_id = user_info["id"]
    user_name = user_info.get("name", "there")
    logger.info(f"ChatKit request from authenticated user {user_id}")

    try:
        # Read request body
        payload = await request.body()
        logger.info(f"Received payload: {len(payload)} bytes")
        logger.debug(f"Payload content: {payload.decode('utf-8')}")

        # Add user info to context for the ChatKit server
        context = {
            "user_id": user_id,
            "user_name": user_name,
        }

        # Get cached ChatKit server for this user
        chatkit_server = await _get_chatkit_server(user_id)

        # Process through ChatKit server
        result = await chatkit_server.process(payload, context)

        # Return appropriate response type
        if isinstance(result, StreamingResult):
            logger.info(f"Returning streaming response for user {user_id}")
            return StreamingResponse(
                result,
                media_type="text/event-stream",
            )

        # JSON response
        logger.info(f"Returning JSON response for user {user_id}")
        return Response(
            content=result.json,
            media_type="application/json",
        )

    except Exception as e:
        logger.error(f"ChatKit error for user {user_id}: {e}", exc_info=True)
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=500,
        )
