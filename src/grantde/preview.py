"""Build and serve the local draft preview on the loopback interface."""

import argparse
import sys
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from jinja2 import TemplateError

from .build import build_site
from .catalogue import CatalogueError


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--project-dir", type=Path, default=Path("."))
    parser.add_argument("--as-of", type=date.fromisoformat, default=None)
    args = parser.parse_args(argv)
    root = args.project_dir.resolve()
    output = root / "build/preview"
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    try:
        metrics = build_site(root, root / "data", output, preview=True, today=args.as_of)
        handler = partial(SimpleHTTPRequestHandler, directory=str(output))
        with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
            print(f"GrantDE local draft preview: {metrics['records']} listings, {metrics['pages']} pages.", flush=True)
            print(f"Open http://127.0.0.1:{args.port}/  (Ctrl+C to stop)", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nPreview stopped.")
    except (CatalogueError, OSError, TemplateError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
