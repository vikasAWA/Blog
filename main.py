from fasthtml.common import*
from monsterui.all import *
import os, yaml
import re
from html import escape


app, rt = fast_app(
    hdrs=(
        Theme.blue.headers(),
        Style("""
        .toc-container {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 1.25rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #e0e0e0;
        }
        .sticky-toc {
            position: sticky;
            top: 2rem;
        }
        .toc-container h4 {
            margin-top: 0;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e0e0e0;
            font-size: 1.1rem;
            color: #333;
        }
        .toc-container ul {
            list-style-type: none;
            padding-left: 0;
            margin-bottom: 0;
        }
        .toc-level-0 { 
            margin-left: 0; 
            font-weight: 600; 
            margin-bottom: 0.6rem;
        }
        .toc-level-1 { 
            margin-left: 1rem; 
            margin-bottom: 0.5rem;
        }
        .toc-level-2 { 
            margin-left: 2rem; 
            font-size: 0.9rem; 
            margin-bottom: 0.4rem;
        }
        .toc-level-3 { 
            margin-left: 2.5rem; 
            font-size: 0.85rem; 
            color: #555; 
            margin-bottom: 0.3rem;
        }
        .toc-level-4, .toc-level-5 { 
            display: none; /* Hide deeper levels for cleaner TOC */
        }
        
        /* Style TOC links */
        .toc-container a {
            text-decoration: none;
            color: #2c5282;
            transition: color 0.2s;
            display: block;
            padding: 2px 0;
        }
        
        .toc-container a:hover {
            color: #1a365d;
            text-decoration: none;
            background-color: #f0f4f8;
            border-radius: 3px;
            padding-left: 5px;
        }
        
        /* Main content styling */
        .content-column {
            padding-right: 2rem;
        }
        """)
    ),
    live=True
)




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
    
def calculate_reading_time(text):
    # Count words in the text
    word_count = len(text.split())
    
    # Average reading speed (words per minute)
    reading_speed = 200
    
    # Calculate reading time in minutes
    minutes = max(1, round(word_count / reading_speed))
    
    return f"{minutes} min read"


def BlogCard(fname):
    with open(f"posts/{fname}") as f: content = f.read()
    meta = content.split('---')[1]
    meta = yaml.safe_load(meta)
    
    # Get the main content (after the second ---)
    main_content = content.split('---')[2]
    
    # Calculate reading time
    reading_time = calculate_reading_time(main_content)
    
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
                P(reading_time, cls=(TextT.muted, TextT.sm, "flex items-center")),
            ),
            DivFullySpaced(
                P(""),  # Empty element for spacing
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

def generate_table_of_contents(markdown_content):
    # Find all headings in the markdown content
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+?)$', re.MULTILINE)
    headings = heading_pattern.findall(markdown_content)
    
    if not headings:
        return []  # No headings found, return empty list
    
    # Create TOC items
    toc_items = []
    
    for heading_level, heading_text in headings:
        # Remove emojis and other special characters
        clean_text = re.sub(r'[^\w\s\-.,:]', '', heading_text)
        clean_text = clean_text.strip()
        
        # Create an ID for the heading (for linking)
        heading_id = clean_text.lower().replace(' ', '-').replace('.', '').replace(',', '')
        heading_id = re.sub(r'[^a-z0-9-]', '', heading_id)
        
        # Determine the indentation level (heading level - 1)
        level = len(heading_level) - 1
        
        # Add to TOC items
        toc_items.append((level, clean_text, heading_id))
    
    return toc_items


@rt   
def blog_post(fname:str):
    with open(f"posts/{fname}") as f: content = f.read()
    meta = content.split('---')[1]
    meta = yaml.safe_load(meta)
    main_content = content.split('---')[2]
    
    # Calculate reading time
    reading_time = calculate_reading_time(main_content)
    
    # Generate TOC
    toc_items = generate_table_of_contents(main_content)
    
    # Modify markdown content to add IDs to headings
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+?)$', re.MULTILINE)
    
    def add_heading_id(match):
        heading_level, heading_text = match.groups()
        # Remove emojis and special characters for the ID
        clean_text = re.sub(r'[^\w\s\-.,:]', '', heading_text)
        clean_text = clean_text.strip()
        
        heading_id = clean_text.lower().replace(' ', '-').replace('.', '').replace(',', '')
        heading_id = re.sub(r'[^a-z0-9-]', '', heading_id)
        
        # Keep original heading text for display
        return f'{heading_level} <a id="{heading_id}"></a>{heading_text}'
    
    modified_content = heading_pattern.sub(add_heading_id, main_content)
    
    return BlogNav(), Container(
        DivFullySpaced(
            H1(meta['title']),
            P(reading_time, cls=(TextT.muted, TextT.sm))
        ),
        # Create a two-column layout with main content and TOC sidebar
        Grid(
            # Main content column
            Div(render_md(modified_content), cls="col-span-3 content-column"),
            
            # TOC sidebar column (only if TOC exists)
            Div(Card(
                Ul(*[Li(A(text, href=f"#{heading_id}"), cls=f"toc-level-{level}") 
                     for level, text, heading_id in toc_items if level < 4]) if toc_items else "",
                header=H4("Contents"),
                cls="toc-container sticky-toc"
            ), cls="col-span-1") if toc_items else "",
            
            cols=4,  # 4 columns total (3 for content, 1 for TOC)
        ),
        cls='p-10'
    )


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
def index(page: str = "1"):
    page = int(page)
    # Get all post filenames
    all_posts = os.listdir('posts')
    
    # Set how many posts per page
    posts_per_page = 5
    
    # Calculate total pages
    total_pages = (len(all_posts) + posts_per_page - 1) // posts_per_page
    
    # Ensure page is valid
    page = max(1, min(page, total_pages))
    
    # Get posts for current page
    start_idx = (page - 1) * posts_per_page
    end_idx = start_idx + posts_per_page
    current_posts = all_posts[start_idx:end_idx]
    
    # Create pagination controls
    pagination = DivFullySpaced(
        A("← Previous", 
        href=index.to(page=page-1) if page > 1 else "#",
        cls=ButtonT.secondary, 
        disabled=page <= 1),
        P(f"Page {page} of {total_pages}", cls=TextT.muted),
        A("Next →", 
        href=index.to(page=page+1) if page < total_pages else "#",
        cls=ButtonT.secondary,
        disabled=page >= total_pages)
    )

    
    return BlogNav(), Container(
        H2("My Blog"),
        Grid(*map(BlogCard, current_posts), cols=1),
        pagination,
        cls='p-10'
    )


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