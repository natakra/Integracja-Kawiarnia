from starlite import Starlite, get


@get("/")
def hello_world() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"hello": "world"}


app = Starlite(route_handlers=[hello_world])