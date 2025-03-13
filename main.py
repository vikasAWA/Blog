from fasthtml.common import*
from monsterui.all import *
import os, yaml

app, rt = fast_app(hdrs=Theme.blue.headers(), live=True)

def BlogNav(search_query=""):
    return NavBar(
        A("Home", href=index),
        A("Theme", href=theme),
        A("About Me", href=about_me),
        DivLAligned(
            Form(
                Input(placeholder="Search blog...", name="query", value=search_query),
                Button(UkIcon("search"), type="submit"),
                method="get", action=search.to(), cls="flex"
            ),
            social_media()
        ),
        brand=H3("Vikas Awasthi", cls=TextT.muted)
    )


def BlogCard(fname):
    with open(f"posts/{fname}") as f: content = f.read()
    meta = content.split('---')[1]
    meta = yaml.safe_load(meta)
    return Container(Card(DivHStacked(
        Img(src=meta['image'], style='width:200px'), 
        Div(
            A(H3(meta['title']), href=blog_post.to(fname=fname)), 
            P(meta['description']),
            DivFullySpaced(
                P(meta['author'], cls=TextT.muted), 
                P(meta['date'], cls=TextT.muted)
            ),
            DivFullySpaced(
                DivLAligned(*map(Label, meta['categories'])),
                A("Read More", href=blog_post.to(fname=fname), 
                  cls=("uk-button rounded-md px-2 px-2", ButtonT.primary))),
            
            cls='space-y-3'
        )
    ), cls=[CardT.hover]), cls='p-10')
    
    
def social_media():
    return DivHStacked(
                UkIconLink("linkedin", height=16, href="https://www.linkedin.com/in/vikas-awasthi-583957263/"),
                UkIconLink("github", height=16, href="https://github.com/vikasAWA?tab=repositories"),
                UkIconLink("twitter", height=16, href="https://x.com/Vikas_awa")
)


@rt   
def blog_post(fname:str):
    with open(f"posts/{fname}") as f: content = f.read()
    content = content.split('---')[2]
    return BlogNav(), Container(render_md(content), cls='p-10')

@rt
def about_me():
    with open("aboutme.md", "r") as f: content = f.read()
    return BlogNav(), Card(
        DivLAligned(
            DiceBearAvatar("vawa", h=24, w=24),
            Div(H3("Vikas Awasthi"), Div(render_md(content), cls=TextT.muted))),
        footer=DivFullySpaced(
            DivHStacked(UkIcon("map-pin", height=16), P("remote")),
            social_media()))

@rt
def index():
    return  BlogNav(), Grid(*map(BlogCard, os.listdir('posts')),  cols=1)

@rt
def theme():
    return BlogNav(), ThemePicker()

@rt
def search(query: str = ""):
    results = []
    if query:
        for fname in os.listdir('posts'):
            try:
                with open(f"posts/{fname}") as f:
                    content = f.read()
                if query.lower() in content.lower():
                    results.append(fname)
            except:
                pass  # Skip files with errors
    
    return BlogNav(query), Container(
        H2(f"Search Results for: {query}" if query else "Search"),
        P(f"Found {len(results)} matching posts" if query else "Enter a search term above"),
        Grid(*map(BlogCard, results), cols_sm=1, cols_md=2, cols_lg=3) if results else "",
        cls='p-10'
    )

serve()