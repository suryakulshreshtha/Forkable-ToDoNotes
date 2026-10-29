"""The web layer: Flask routes for the HTML pages and a small JSON API.

Two kinds of routes live here:

* HTML pages (``/``, ``/notes/<id>`` …) that work with plain forms and no
  JavaScript at all. Every form POST answers with a redirect
  (Post/Redirect/Get), so refreshing a page never re-submits a form.
* A JSON API under ``/api`` that the page's JavaScript uses for autosave and
  that the Playwright tests use to seed data quickly.

Routes stay thin: read the request, call the service, render or redirect.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, Response, abort, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

from todonotes import APP_NAME, __version__
from todonotes.config import default_db_path
from todonotes.service import NoteService, NotFoundError, ValidationError
from todonotes.storage import NoteRepository

LOCAL_HOSTNAMES = {"127.0.0.1", "localhost", "::1"}
UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def localtime(iso: str) -> str:
    """Jinja filter: '2026-10-29T07:15:00+00:00' -> '29 Oct 2026, 08:15' in local time."""
    try:
        return datetime.fromisoformat(iso).astimezone().strftime("%d %b %Y, %H:%M")
    except ValueError:
        return iso


def create_app(db_path: Path | str | None = None) -> Flask:
    """Application factory: build a fully configured Flask app.

    Tests call ``create_app(tmp_path / "notes.db")`` to get an isolated app.
    """
    app = Flask(__name__)
    repo = NoteRepository(db_path or default_db_path())
    repo.initialize()
    service = NoteService(repo)
    app.extensions["todonotes"] = service

    app.add_template_filter(localtime)

    @app.context_processor
    def inject_globals() -> dict:
        return {
            "app_name": APP_NAME,
            "version": __version__,
        }

    # ------------------------------------------------------------ safety net
    @app.before_request
    def only_local_and_same_origin() -> None:
        """Cheap checks that matter for an app listening on your machine.

        1. Host check: answer only to 127.0.0.1 / localhost. A web page that
           re-points its own domain name at 127.0.0.1 (DNS rebinding) sends a
           different Host header and is refused.
        2. Fetch Metadata: modern browsers label each request with
           Sec-Fetch-Site. Changes are accepted only from "same-origin" (our
           own pages) or "none" (typed by you), never from another site.
        3. Origin check (fallback for browsers without Fetch Metadata): if an
           Origin header is present and is not this app, refuse the change.
        Together they stop a random website from editing your notes (CSRF).
        """
        hostname = urlsplit(f"//{request.host}").hostname
        if hostname not in LOCAL_HOSTNAMES:
            abort(400, "This app only answers on 127.0.0.1 or localhost.")
        if request.method in UNSAFE_METHODS:
            fetch_site = request.headers.get("Sec-Fetch-Site")
            if fetch_site is not None and fetch_site not in {"same-origin", "none"}:
                abort(403, "Cross-site request refused.")
            origin = request.headers.get("Origin")
            if origin is not None and urlsplit(origin).netloc != request.host:
                abort(403, "Cross-site request refused.")

    # ----------------------------------------------------------- error pages
    def wants_json() -> bool:
        return request.path.startswith("/api/")

    @app.errorhandler(ValidationError)
    def on_validation_error(error: ValidationError):
        if wants_json():
            return {"error": str(error)}, 400
        return render_template("error.html", code=400, message=str(error)), 400

    @app.errorhandler(NotFoundError)
    def on_not_found(error: NotFoundError):
        if wants_json():
            return {"error": str(error)}, 404
        return render_template("error.html", code=404, message=str(error)), 404

    @app.errorhandler(HTTPException)
    def on_http_error(error: HTTPException):
        if wants_json():
            return {"error": error.description}, error.code
        return render_template("error.html", code=error.code, message=error.description), (
            error.code
        )

    # ------------------------------------------------------------ HTML pages
    @app.get("/")
    def index():
        return render_template("index.html", notes=service.list(), q="", hits=None)

    @app.get("/notes/new")
    def new_note():
        return render_template("note.html", note=None, saved=False)

    @app.post("/notes")
    def create_note():
        note = service.create(
            title=request.form.get("title", ""),
            body=request.form.get("body", ""),
            pinned="pinned" in request.form,
        )
        return redirect(url_for("show_note", note_id=note.id, saved=1))

    @app.get("/notes/<int:note_id>")
    def show_note(note_id: int):
        saved = request.args.get("saved") == "1"
        return render_template("note.html", note=service.get(note_id), saved=saved)

    @app.post("/notes/<int:note_id>")
    def update_note(note_id: int):
        service.update(
            note_id,
            title=request.form.get("title", ""),
            body=request.form.get("body", ""),
            pinned="pinned" in request.form,
        )
        return redirect(url_for("show_note", note_id=note_id, saved=1))

    @app.post("/notes/<int:note_id>/pin")
    def toggle_pin(note_id: int):
        service.toggle_pin(note_id)
        return redirect(url_for("index"))

    @app.post("/notes/<int:note_id>/delete")
    def delete_note(note_id: int):
        service.delete(note_id)
        return redirect(url_for("index"))

    @app.post("/notes/<int:note_id>/items")
    def add_item(note_id: int):
        service.add_item(note_id, request.form.get("text", ""))
        return redirect(url_for("show_note", note_id=note_id, _anchor="checklist"))

    @app.post("/items/<int:item_id>/toggle")
    def toggle_item(item_id: int):
        item = service.toggle_item(item_id)
        return redirect(url_for("show_note", note_id=item.note_id, _anchor="checklist"))

    @app.post("/items/<int:item_id>/delete")
    def delete_item(item_id: int):
        note_id = service.remove_item(item_id)
        return redirect(url_for("show_note", note_id=note_id, _anchor="checklist"))

    @app.get("/export.json")
    def export_json():
        body = json.dumps(service.export_data(), indent=2, ensure_ascii=False)
        return _download(body, "application/json", "json")

    @app.get("/export.md")
    def export_markdown():
        return _download(service.export_markdown(), "text/markdown", "md")

    # -------------------------------------------------------------- JSON API
    def json_body() -> dict:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            raise ValidationError("Send a JSON object with Content-Type: application/json.")
        return data

    def optional_bool(data: dict, key: str) -> bool | None:
        value = data.get(key)
        if value is not None and not isinstance(value, bool):
            raise ValidationError(f"'{key}' must be true or false.")
        return value

    def optional_str(data: dict, key: str) -> str | None:
        value = data.get(key)
        if value is not None and not isinstance(value, str):
            raise ValidationError(f"'{key}' must be a string.")
        return value

    @app.get("/api/health")
    def api_health():
        return {
            "status": "ok",
            "app": APP_NAME,
            "version": __version__,
        }

    @app.get("/api/notes")
    def api_list_notes():
        return {"notes": [note.to_dict() for note in service.list()]}

    @app.post("/api/notes")
    def api_create_note():
        data = json_body()
        note = service.create(
            title=optional_str(data, "title") or "",
            body=optional_str(data, "body") or "",
            pinned=bool(optional_bool(data, "pinned")),
        )
        for text in data.get("items") or []:
            service.add_item(note.id, str(text))
        return service.get(note.id).to_dict(), 201

    @app.get("/api/notes/<int:note_id>")
    def api_get_note(note_id: int):
        return service.get(note_id).to_dict()

    @app.patch("/api/notes/<int:note_id>")
    def api_update_note(note_id: int):
        data = json_body()
        note = service.update(
            note_id,
            title=optional_str(data, "title"),
            body=optional_str(data, "body"),
            pinned=optional_bool(data, "pinned"),
        )
        return note.to_dict()

    @app.delete("/api/notes/<int:note_id>")
    def api_delete_note(note_id: int):
        service.delete(note_id)
        return "", 204

    @app.post("/api/notes/<int:note_id>/items")
    def api_add_item(note_id: int):
        item = service.add_item(note_id, optional_str(json_body(), "text") or "")
        return item.to_dict(), 201

    @app.patch("/api/items/<int:item_id>")
    def api_update_item(item_id: int):
        done = optional_bool(json_body(), "done")
        if done is None:
            raise ValidationError('Send {"done": true} or {"done": false}.')
        return service.set_item_done(item_id, done).to_dict()

    @app.delete("/api/items/<int:item_id>")
    def api_delete_item(item_id: int):
        service.remove_item(item_id)
        return "", 204

    return app


def _download(body: str, mimetype: str, extension: str) -> Response:
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"todonotes-export-{stamp}.{extension}"
    return Response(
        body,
        mimetype=mimetype,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
