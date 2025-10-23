from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

from aido.agent import root_agent
from aido.callbacks import DEFAULT_CALLBACKS
from aido.db import session_service

APP_NAME = "aido"
DEFAULT_USER_ID = "local-user"
UI_DIST_PATH = Path(__file__).resolve().parent / "ui" / "dist"
UI_INDEX_FILE = UI_DIST_PATH / "index.html"


def create_app() -> FastAPI:
    app = FastAPI(title="AIDO Control Center", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    agui_agent = ADKAgent(
        adk_agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        use_in_memory_services=False,
    )

    add_adk_fastapi_endpoint(app, agui_agent, path="/api/copilotkit")

    if UI_INDEX_FILE.exists():
        assets_path = UI_DIST_PATH / "assets"
        if assets_path.exists():
            app.mount(
                "/assets",
                StaticFiles(directory=assets_path),
                name="aido-ui-assets",
            )

        @app.get("/", include_in_schema=False)
        async def serve_index() -> FileResponse:
            return FileResponse(UI_INDEX_FILE)

        @app.get("/favicon.ico", include_in_schema=False)
        async def serve_favicon() -> FileResponse:
            favicon = UI_DIST_PATH / "favicon.ico"
            if favicon.exists():
                return FileResponse(favicon)
            raise HTTPException(status_code=404, detail="Favicon not found")

    @app.get("/api/healthz", tags=["diagnostics"])
    async def healthcheck() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/sessions", tags=["sessions"])
    async def list_sessions(
        user_id: str = Query(DEFAULT_USER_ID, description="Identificador do usuário.")
    ) -> Dict[str, List[Dict[str, Any]]]:
        try:
            response = await session_service.list_sessions(
                app_name=APP_NAME, user_id=user_id
            )
        except Exception as exc:  # pragma: no cover - defensivo
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        sessions_payload: List[Dict[str, Any]] = []
        for session in response.sessions:
            state = session.state or {}
            sessions_payload.append(
                {
                    "id": session.id,
                    "user_id": session.user_id,
                    "created_at": session.create_time,
                    "updated_at": session.last_update_time,
                    "status": state.get("status", "unknown"),
                    "video_path": state.get("video_path"),
                    "generated_docx_path": state.get("generated_docx_path"),
                    "structured_title": (
                        (state.get("structured_data") or {}).get("titulo")
                        if isinstance(state.get("structured_data"), dict)
                        else None
                    ),
                }
            )

        return {"sessions": sessions_payload}

    return app


app = create_app()


__all__ = ["app", "create_app"]
