import requests
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner
from rich import box
import time

BASE_URL = "http://127.0.0.1:8000/api"
console = Console()

session = {
    "token": None,
    "username": None,
}

LOGO = r"""
░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓██████████████▓▒░  
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░  ░▒▓████████▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                                  
                                                                                                  
                                                                                                  
"""

DIFFICULTY_COLORS = {
    "beginner":    "green",
    "intermediate": "yellow",
    "advanced":     "red",
}

DIFFICULTY_ICONS = {
    "beginner":    "○○○",
    "intermediate": "●●○",
    "advanced":     "●●●",
}

def difficulty_badge(level: str) -> Text:
    color = DIFFICULTY_COLORS.get(level, "white")
    icon = DIFFICULTY_ICONS.get(level, "?")
    t = Text()
    t.append(f" {icon} {level.upper()} ", style=f"bold {color} on grey19")
    return t

def auth_headers() -> dict:
    return {"Authorization": f"Token {session['token']}"}

def api(method: str, path: str, **kwargs):
    url = f"{BASE_URL}{path}"
    if session["token"]:
        kwargs.setdefault("headers", {}).update(auth_headers())
    try:
        r = getattr(requests, method)(url, **kwargs)
        return r
    except requests.ConnectionError:
        console.print("\n[bold red]Error[/] Cannot reach the server.\n")
        sys.exit(1)

def loading(msg: str = "Loading..."):
    return Live(Spinner("dots", text = f"[dim]{msg}[/]"), console = console, transient=True)



def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_logo():
    clear()
    console.print(Text(LOGO, style="bold bright_blue"), justify="center")
    console.print(
        Align.center(Text("the guitar tab app for terminal-heads", style="italic dim"))
    )
    console.print()

def show_banner():
    t = Text()
    t.append("TabTerm", style="bold bright_blue")
    if session["username"]:
        t.append(f"  ·  logged in as ", style="dim")
        t.append(session["username"], style="bold cyan")
    console.print(Rule(t, style="bright_blue"))
    console.print()



def screen_login():
    show_logo()
    console.print(Panel("[bold]Log in to your account[/]", border_style="bright_blue", width=44))
    username = Prompt.ask("[cyan]Username[/]")
    password = Prompt.ask("[cyan]Password[/]", password=True)

    with loading("Authenticating..."):
        r = api("post", "/auth/login/", json={"username": username, "password": password})

    if r.status_code == 200:
        data = r.json()
        session["token"] = data["token"]
        session["username"] = data["username"]
        console.print(f"\n[bold green]Success[/] Welcome back, [bold cyan]{session['username']}[/]!\n")
        time.sleep(1)
        screen_main_menu()
    else:
        console.print("\n[bold red]Error: Invalid creditensials.[/]\n")
        time.sleep(1)
        screen_auth_menu()

def screen_register():
    show_logo()
    console.print(Panel("[bold]Create an account[/]", border_style="bright_blue", width=44))
    username = Prompt.ask("[cyan]Username[/]")
    email = Prompt.ask("[cyan]Email[/]")
    password = Prompt.ask("[cyan]Password[/]", password=True)

    with loading("Creating account..."):
        r = api("post", "/auth/register/", json={
            "username": username, "email": email, "password": password
        })

    if r.status_code == 200:
        data = r.json()
        session["token"] = data["token"]
        session["username"] = data["username"]
        console.print(f"\n[bold green]Success[/] Account created! Welcome, [bold cyan]{session['username']}[/]!\n")
        time.sleep(1)
        screen_main_menu()
    else:
        errors = r.json()
        console.print(f"\n[bold red]Error: [/]{errors}\n")
        time.sleep(1.5)
        screen_auth_menu()

def screen_auth_menu():
    show_logo()
    console.print(Align.center(
        Panel(
            "[1] Login\n[2] Register\n[3] Browse tabs\n[Q] Quit",
            title="[bold bright_blue]Menu[/]",
            border_style="bright_blue",
            width=36,
        )
    ))
    console.print()
    choice = Prompt.ask("[bold]>[/]", choices=["1","2","3","q","Q"], default="1")
    if choice == "1": screen_login()
    elif choice == "2": screen_register()
    elif choice == "3": screen_browse_tabs()
    else: goodbye()

def screen_main_menu():
    show_logo()
    show_banner()
    console.print(Align.center(
        Panel(
            "[1] Browse tabs\n"
            "[2] Search tabs\n"
            "[3] View a tab\n"
            "[4] Create a tab\n"
            "[5] My favorites\n"
            "[6] My profile\n"
            "[Q] Logout",
            title="[bold bright_blue]Main Menu[/]",
            border_style="bright_blue",
            width=36,
        )
    ))
    console.print()
    choice = Prompt.ask("[bold]>[/]", choices=["1","2","3","4","5","6","q","Q"], default="1")
    if choice == "1": screen_browse_tabs()
    elif choice == "2": screen_search_tabs()
    elif choice == "3": screen_view_tab_by_id()
    elif choice == "4": screen_create_tab()
    elif choice == "5": screen_favorites()
    elif choice == "6": screen_profile()
    else:
        session["token"] = None
        session["username"] = None
        screen_auth_menu()


def render_tabs_table(tabs: list, title: str = "TabTerm"):
    if not tabs:
        console.print("[dim]No tabs found.[/]\n")
        return
    
    table = Table(
        title=f"[bold bright_blue]{title}[/]",
        box=box.SIMPLE_HEAD,
        border_style="grey30",
        header_style="bold bright_blue",
        show_lines=False,
        expand=True,
    )
    table.add_column("#", style = "dim", width=4, justify="right")
    table.add_column("Title", style = "bold white", ratio=3)
    table.add_column("Artist", style = "cyan", ratio=2)
    table.add_column("Tuning", style = "dim", ratio=2)
    table.add_column("Level", ratio=2)
    table.add_column("Author", style="dim magenta", ratio=2)
    table.add_column("<3", style="bold red", width=5, justify="center")

    for tab in tabs:
        table.add_row(
            str(tab["id"]),
            tab["title"],
            tab["artist"],
            tab["tuning"],
            difficulty_badge(tab["difficulty"]),
            tab["author"],
            str(tab["favorite_count"]),
        )
    
    console.print(table)

def screen_browse_tabs(params: dict = None):
    clear()
    show_banner()
    with loading("Fetching tabs..."):
        r = api("get", "/tabs/", params=params or {})
    tabs = r.json()
    render_tabs_table(tabs, title="All Tabs")
    _tab_list_actions()

def screen_search_tabs():
    clear()
    show_banner()
    console.print("[bold]Search tabs[/]\n")
    query = Prompt.ask("[cyan]Search[/] (artist, song, title)")
    difficulty = Prompt.ask(
        "[cyan]Difficulty[/]",
        choises=["", "beginner","intermediate","advanced"],
        default="",
        show_default=False,
        show_choices=True,
    )
    params = {}
    if query: params["search"] = query
    if difficulty: params["difficulty"] = difficulty

    with loading("Searching..."):
        r = api("get", "/tabs/", params=params)
    tabs = r.json()
    render_tabs_table(tabs, title=f'Results for "{query}"')
    _tab_list_actions()

def _tab_list_actions():
    console.print()
    console.print("[dim][V] View a a tab   [B] Back to menu[/]")
    choice = Prompt.ask("[bold]>[/]", choices=["v","V","b","B"], default="b")
    if choice.lower() == "v":
        screen_view_tab_by_id()
    else:
        _back_to_menu()



def screen_view_tab_by_id():
    clear()
    show_banner()
    tab_id = Prompt.ask("[cyan]Enter Tab ID[/]")
    with loading("Loading tab..."):
        r = api("get", f"/tabs/{tab_id}/")
    if r.status_code == 404:
        console.print("[red]Tab not found.[/]\n")
        time.sleep(1)
        _back_to_menu()
        return
    screen_view_tab(r.json())

def screen_view_tab(tab: dict):
    clear()
    show_banner()

    info = Table.grid(padding=(0,2))
    info.add_column(style="dim", justify="right")
    info.add_column(style="white")
    info.add_row("Artist", f"[bold cyan]{tab['artist']}[/]")
    info.add_row("Song", tab["song"])
    info.add_row("Tuning", f"[yellow]{tab['tuning']}[/]")
    info.add_row("Level", difficulty_badge(tab["difficulty"]))
    info.add_row("Author", f"[magenta]{tab['author']}[/]")
    info.add_row("Favorites", f"[red]<3 {tab['favorite_count']}[/]")

    console.print(Panel(
        info,
        title=f"[bold bright_blue]{tab['title']}[/]",
        border_style="bright_blue",
        subtitle=f"[dim]id:{tab['id']}[/]",
    ))

    if tab.get("description"):
        console.print(f"\n[italic dim]{tab['description']}[/]\n")

    
    console.print(Panel(
        Text(tab["content"], style="bold green on grey7"),
        title="[bold]Tab[/]",
        border_style="grey30",
        padding=(1, 2),
    ))

    
    comments = tab.get("comments", [])
    if comments:
        console.print(f"\n[bold bright_blue]Comments[/] [dim]({len(comments)})[/]\n")
        for c in comments:
            console.print(
                f"  [magenta]{c['author']}[/] [dim]{c['created_at'][:10]}[/]"
            )
            console.print(f"  {c['content']}\n")
    else:
        console.print("\n[dim]No comments yet. Be the first![/]\n")

    
    actions = ["[B] Back"]
    if session["token"]:
        actions += ["[C] Comment", "[F] Toggle favorite"]
        if tab["author"] == session["username"]:
            actions += ["[E] Edit", "[D] Delete"]

    console.print("[dim]" + "   ".join(actions) + "[/]")
    valid = ["b","B"]
    if session["token"]:
        valid += ["c","C","f","F"]
        if tab["author"] == session["username"]:
            valid += ["e","E","d","D"]

    choice = Prompt.ask("[bold]>[/]", choices=valid, default="b")
    c = choice.lower()
    if   c == "c": screen_add_comment(tab)
    elif c == "f": action_toggle_favorite(tab)
    elif c == "e": screen_edit_tab(tab)
    elif c == "d": action_delete_tab(tab)
    else: _back_to_menu()



def screen_create_tab():
    clear()
    show_banner()
    console.print(Panel("[bold]Create a new tab[/]", border_style="bright_blue", width=44))
    console.print("[dim]Fill in the details below. For the tab content, use standard ASCII tab notation.[/]\n")

    title       = Prompt.ask("[cyan]Title[/]")
    artist      = Prompt.ask("[cyan]Artist[/]")
    song        = Prompt.ask("[cyan]Song[/]")
    tuning      = Prompt.ask("[cyan]Tuning[/]", default="Standard (EADGBe)")
    difficulty  = Prompt.ask(
        "[cyan]Difficulty[/]",
        choices=["beginner","intermediate","advanced"],
        default="beginner",
    )
    description = Prompt.ask("[cyan]Description[/] [dim](optional)[/]", default="")

    console.print("\n[bold cyan]Tab content[/] [dim](paste your tab, then type END on a new line)[/]\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    content = "\n".join(lines)

    payload = {
        "title": title, "artist": artist, "song": song,
        "tuning": tuning, "difficulty": difficulty,
        "description": description, "content": content,
    }

    with loading("Saving tab…"):
        r = api("post", "/tabs/", json=payload)

    if r.status_code == 201:
        tab = r.json()
        console.print(f"\n[bold green]✓[/] Tab created! ID: [bold]{tab['id']}[/]\n")
        time.sleep(1)
        screen_view_tab(tab)
    else:
        console.print(f"\n[red]✗ Error:[/] {r.json()}\n")
        time.sleep(1.5)
        screen_main_menu()

def screen_edit_tab(tab: dict):
    clear()
    show_banner()
    console.print(Panel(f"[bold]Editing:[/] {tab['title']}", border_style="bright_blue", width=50))
    console.print("[dim]Leave blank to keep existing value.[/]\n")

    title      = Prompt.ask("[cyan]Title[/]",      default=tab["title"])
    artist     = Prompt.ask("[cyan]Artist[/]",     default=tab["artist"])
    song       = Prompt.ask("[cyan]Song[/]",       default=tab["song"])
    tuning     = Prompt.ask("[cyan]Tuning[/]",     default=tab["tuning"])
    difficulty = Prompt.ask(
        "[cyan]Difficulty[/]",
        choices=["beginner","intermediate","advanced"],
        default=tab["difficulty"],
    )
    description = Prompt.ask("[cyan]Description[/]", default=tab.get("description",""))

    console.print("\n[dim]Tab content (type END to finish, leave just END to keep existing):[/]\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    content = "\n".join(lines) if lines else tab["content"]

    payload = {
        "title": title, "artist": artist, "song": song,
        "tuning": tuning, "difficulty": difficulty,
        "description": description, "content": content,
    }

    with loading("Saving…"):
        r = api("put", f"/tabs/{tab['id']}/", json=payload)

    if r.status_code == 200:
        console.print("\n[bold green]✓[/] Tab updated!\n")
        time.sleep(1)
        screen_view_tab(r.json())
    else:
        console.print(f"\n[red]✗ Error:[/] {r.json()}\n")
        time.sleep(1.5)
        screen_main_menu()

def action_delete_tab(tab: dict):
    confirmed = Confirm.ask(f"[red]Delete[/] '{tab['title']}'? This cannot be undone")
    if not confirmed:
        screen_view_tab(tab)
        return
    with loading("Deleting…"):
        r = api("delete", f"/tabs/{tab['id']}/")
    if r.status_code == 204:
        console.print("\n[bold green]✓[/] Tab deleted.\n")
    else:
        console.print(f"\n[red]✗[/] {r.json()}\n")
    time.sleep(1)
    screen_browse_tabs()



def screen_add_comment(tab: dict):
    clear()
    show_banner()
    console.print(f"[bold]Add comment on:[/] [bright_blue]{tab['title']}[/]\n")
    content = Prompt.ask("[cyan]Your comment[/]")

    with loading("Posting…"):
        r = api("post", f"/tabs/{tab['id']}/comments/", json={"content": content})

    if r.status_code == 201:
        console.print("\n[bold green]✓[/] Comment posted!\n")
    else:
        console.print(f"\n[red]✗[/] {r.json()}\n")
    time.sleep(1)

    # Reload tab to show new comment
    r2 = api("get", f"/tabs/{tab['id']}/")
    screen_view_tab(r2.json())



def action_toggle_favorite(tab: dict):
    with loading("Updating…"):
        r = api("post", f"/tabs/{tab['id']}/favorite/")
    status = r.json().get("status", "")
    icon   = "♥" if status == "favorited" else "♡"
    console.print(f"\n[bold green]✓[/] {icon} {status.capitalize()}\n")
    time.sleep(1)
    r2 = api("get", f"/tabs/{tab['id']}/")
    screen_view_tab(r2.json())

def screen_favorites():
    clear()
    show_banner()
    with loading("Loading favorites…"):
        r = api("get", "/favorites/")
    data = r.json()
    tabs = [f["tab"] for f in data]
    render_tabs_table(tabs, title="♥ My Favorites")
    _tab_list_actions()



def screen_profile():
    clear()
    show_banner()
    with loading("Loading profile…"):
        r  = api("get", "/auth/profile/")
        r2 = api("get", "/tabs/", params={})

    user = r.json()
    all_tabs = r2.json()
    my_tabs  = [t for t in all_tabs if t["author"] == session["username"]]

    grid = Table.grid(padding=(0, 3))
    grid.add_column(style="dim", justify="right")
    grid.add_column(style="white")
    grid.add_row("Username",  f"[bold cyan]{user['username']}[/]")
    grid.add_row("Email",     user.get("email","—"))
    grid.add_row("Joined",    user["date_joined"][:10])
    grid.add_row("Tabs",      f"[bright_blue]{len(my_tabs)}[/]")

    console.print(Panel(grid, title="[bold bright_blue]My Profile[/]", border_style="bright_blue", width=50))

    if my_tabs:
        console.print()
        render_tabs_table(my_tabs, title="My Tabs")

    console.print()
    console.print("[dim][B] Back to menu[/]")
    Prompt.ask("[bold]>[/]", choices=["b","B"], default="b")
    screen_main_menu()



def _back_to_menu():
    if session["token"]:
        screen_main_menu()
    else:
        screen_auth_menu()

def goodbye():
    clear()
    console.print(Align.center(
        Text("\n  Keep strumming  \n", style="bold bright_blue")
    ))
    sys.exit(0)



if __name__ == "__main__":
    try:
        screen_auth_menu()
    except KeyboardInterrupt:
        goodbye()