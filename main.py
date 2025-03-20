from fasthtml.common import*
from monsterui.all import *
import os, yaml
import re
import json
from pathlib import Path
from html import escape


# Update your app initialization with the complete CSS
app, rt = fast_app(
    hdrs=(
        Theme.blue.headers(),
        Style("""
        /* Blog content wrapper layout */
        .blog-content-wrapper {
            display: flex;
            flex-direction: column;
        }
        
        .blog-main-content {
            width: 100%;
            order: 1;
        }
        
        .blog-toc {
            width: 100%;
            order: 2;
            margin-top: 2rem;
        }
        
        /* Desktop TOC styling */
        .desktop-toc {
            display: none; /* Hidden by default on mobile */
        }
        
        /* Mobile TOC styling */
        .mobile-toc {
            display: block; /* Visible by default on mobile */
            margin-bottom: 2rem;
        }
        
        /* Responsive adjustments */
        @media (min-width: 768px) {
            .blog-content-wrapper {
                flex-direction: row;
                gap: 2rem;
            }
            
            .blog-main-content {
                width: 70%;
                order: 1;
            }
            
            .blog-toc {
                width: 30%;
                order: 2;
                margin-top: 0;
            }
            
            .mobile-toc {
                display: none; /* Hide on larger screens */
            }
            
            .desktop-toc {
                display: block; /* Show on larger screens */
            }
        }
        
        /* TOC container with theme-aware colors */
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
        
        /* Dark theme adjustments */
        [data-theme="dark"] .toc-container {
            background-color: #2d3748;
            border-color: #4a5568;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        /* TOC header styling */
        .toc-container h4 {
            margin-top: 0;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e0e0e0;
            font-size: 1.1rem;
            color: #333;
        }
        
        [data-theme="dark"] .toc-container h4 {
            color: #e2e8f0;
            border-bottom-color: #4a5568;
        }
        
        /* TOC links styling with theme awareness */
        .toc-container a {
            text-decoration: none;
            color: #2c5282;
            transition: color 0.2s, background-color 0.2s;
            display: block;
            padding: 2px 5px;
            border-radius: 3px;
        }
        
        [data-theme="dark"] .toc-container a {
            color: #90cdf4;
        }
        
        .toc-container a:hover {
            color: #1a365d;
            background-color: #f0f4f8;
        }
        
        [data-theme="dark"] .toc-container a:hover {
            color: #bee3f8;
            background-color: #2d3748;
        }
        
        /* TOC list styling */
        .toc-container ul {
            list-style-type: none;
            padding-left: 0;
            margin-bottom: 0;
        }
        
        /* Level styling with theme awareness */
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
        
        [data-theme="dark"] .toc-level-3 {
            color: #cbd5e0;
        }
        
        .toc-level-4, .toc-level-5 { 
            display: none;
        }
        
        /* Also make blog cards responsive */
        @media (max-width: 768px) {
            .blog-card-container {
                flex-direction: column;
            }
            .blog-card-image {
                width: 100% !important;
                max-height: 200px;
                object-fit: cover;
            }
        }
        /* Social sharing buttons */
        .social-share-buttons {
            display: flex;
            gap: 10px;
        }

        .social-share-buttons a {
            transition: transform 0.2s;
        }

        .social-share-buttons a:hover {
            transform: translateY(-3px);
        }

        /* Comments styling */
        .comments-section {
            border-top: 1px solid #e0e0e0;
            padding-top: 2rem;
        }

        [data-theme="dark"] .comments-section {
            border-top-color: #4a5568;
        }

        """)
    ),
    live=True
)


# Function to update view count
def update_view_count(post_id):
    view_file = Path('views.json')
    
    # Create file if it doesn't exist
    if not view_file.exists():
        with open(view_file, 'w') as f:
            json.dump({}, f)
    
    # Read current views
    with open(view_file, 'r') as f:
        views = json.load(f)
    
    # Update views for this post
    views[post_id] = views.get(post_id, 0) + 1
    
    # Save updated views
    with open(view_file, 'w') as f:
        json.dump(views, f)
    
    return views[post_id]

# Function to get view count
def get_view_count(post_id):
    view_file = Path('views.json')
    
    # Return 0 if file doesn't exist
    if not view_file.exists():
        return 0
    
    # Read current views
    with open(view_file, 'r') as f:
        views = json.load(f)
    
    return views.get(post_id, 0)

def SocialShareButtons(url, title):
    # URL encode the title and full URL
    encoded_url = escape(url)
    encoded_title = escape(title)
    
    return Div(
        A(UkIcon("facebook", height=20), 
          href=f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}",
          target="_blank", rel="noopener", 
          cls="uk-icon-button uk-margin-small-right"),
        A(UkIcon("twitter", height=20), 
          href=f"https://twitter.com/intent/tweet?text={encoded_title}&url={encoded_url}",
          target="_blank", rel="noopener", 
          cls="uk-icon-button uk-margin-small-right"),
        A(UkIcon("linkedin", height=20), 
          href=f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}",
          target="_blank", rel="noopener", 
          cls="uk-icon-button uk-margin-small-right"),
        A(UkIcon("mail", height=20), 
          href=f"mailto:?subject={encoded_title}&body={encoded_url}",
          cls="uk-icon-button"),
        cls="social-share-buttons uk-margin-medium-top"
    )

from datetime import datetime

# Function to save a new comment
def save_comment(post_id, name, email, comment):
    comments_file = Path(f'comments/{post_id}.json')
    comments_dir = Path('comments')
    
    # Create directory if it doesn't exist
    if not comments_dir.exists():
        comments_dir.mkdir()
    
    # Create file if it doesn't exist
    if not comments_file.exists():
        with open(comments_file, 'w') as f:
            json.dump([], f)
    
    # Read current comments
    with open(comments_file, 'r') as f:
        comments = json.load(f)
    
    # Add new comment
    comments.append({
        'name': name,
        'email': email,
        'comment': comment,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Save updated comments
    with open(comments_file, 'w') as f:
        json.dump(comments, f)
    
    return len(comments)

# Function to get comments
def get_comments(post_id):
    comments_file = Path(f'comments/{post_id}.json')
    
    # Return empty list if file doesn't exist
    if not comments_file.exists():
        return []
    
    # Read current comments
    with open(comments_file, 'r') as f:
        comments = json.load(f)
    
    return comments

# Component to display a single comment
def CommentItem(comment):
    return Card(
        Div(
            DivLAligned(
                DiceBearAvatar(comment['name'], h=10, w=10),
                Div(
                    H4(comment['name'], cls=TextT.bold),
                    P(comment['date'], cls=TextT.muted)
                )
            ),
            P(comment['comment'], cls="uk-margin-top")
        ),
        cls="uk-margin-medium-bottom"
    )

# Component to display comment form
def CommentForm(post_id):
    return Form(
        H3("Leave a Comment", cls="uk-margin-medium-top"),
        Grid(
            LabelInput("Name", id="comment_name", required=True),
            LabelInput("Email", id="comment_email", type="email", required=True),
            cols=2
        ),
        LabelTextArea("Comment", id="comment_content", required=True),
        Input(type="hidden", name="post_id", value=post_id),
        Button("Submit Comment", type="submit", cls=ButtonT.primary),
        method="post", action=save_comment_route.to()
    )

# Component to display comments section
def CommentsSection(post_id):
    comments = get_comments(post_id)
    
    return Div(
        H3(f"Comments ({len(comments)})", cls="uk-margin-large-top"),
        Div(*[CommentItem(comment) for comment in comments]) if comments else P("No comments yet. Be the first to comment!"),
        CommentForm(post_id),
        cls="comments-section uk-margin-large-top"
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
        Img(src=meta['image'], style='width:200px', cls="blog-card-image"), 
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
            
            cls='space-y-3 p-5'
        ),
        cls="blog-card-container"
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
def blog_post(fname: str):
    # Update view count
    views = update_view_count(fname)
    
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
        clean_text = re.sub(r'[^\w\s\-.,:]', '', heading_text)
        clean_text = clean_text.strip()
        
        heading_id = clean_text.lower().replace(' ', '-').replace('.', '').replace(',', '')
        heading_id = re.sub(r'[^a-z0-9-]', '', heading_id)
        
        return f'{heading_level} <a id="{heading_id}"></a>{heading_text}'
    
    modified_content = heading_pattern.sub(add_heading_id, main_content)
    
    # TOC component
    toc_component = Card(
        Ul(*[Li(A(text, href=f"#{heading_id}"), cls=f"toc-level-{level}") 
             for level, text, heading_id in toc_items if level < 4]) if toc_items else "",
        header=H4("Contents"),
        cls="toc-container sticky-toc"
    ) if toc_items else ""
    
    # Get current URL for sharing
    current_url = f"{escape(os.environ.get('BASE_URL', 'https://yourblog.com'))}{blog_post.to(fname=fname)}"
    
    # Post metadata with view count
    post_meta = DivFullySpaced(
        DivLAligned(
            P(meta['date'], cls=TextT.muted),
            P("•", cls=TextT.muted),
            P(reading_time, cls=TextT.muted),
            P("•", cls=TextT.muted),
            P(f"{views} views", cls=TextT.muted),
            cls="uk-flex uk-flex-middle gap-2"
        ),
        DivLAligned(*map(Label, meta['categories']))
    )
    
    return BlogNav(), Container(
        # Post header
        Div(
            H1(meta['title']),
            post_meta,
            cls="uk-margin-medium-bottom space-y-2"
        ),
        
        # Mobile TOC (visible only on small screens)
        Div(toc_component, cls="mobile-toc"),
        
        # Desktop layout with explicit order of columns
        Div(cls="blog-content-wrapper")(
            # Main content column
            Div(
                # Main content
                render_md(modified_content),
                
                # Social sharing
                SocialShareButtons(current_url, meta['title']),
                
                # Comments section
                CommentsSection(fname),
                
                cls="blog-main-content"
            ),
            
            # TOC sidebar column (only if TOC exists and on larger screens)
            Div(toc_component, cls="blog-toc desktop-toc") if toc_items else ""
        ),
        cls='p-10'
    )

@rt
def save_comment_route(post_id: str, comment_name: str, comment_email: str, comment_content: str):
    # Save the comment
    save_comment(post_id, comment_name, comment_email, comment_content)
    
    # Redirect back to the blog post
    return RedirectResponse(url=blog_post.to(fname=post_id))


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
    
    # Sort posts by date (newest first)
    sorted_posts = []
    for fname in all_posts:
        try:
            with open(f"posts/{fname}") as f:
                content = f.read()
            meta = content.split('---')[1]
            meta = yaml.safe_load(meta)
            # Add filename and date to the list for sorting
            sorted_posts.append((fname, meta.get('date')))
        except:
            # Skip files with errors
            pass
    
    # Sort by date in descending order (newest first)
    sorted_posts.sort(key=lambda x: x[1], reverse=True)
    
    # Extract just the filenames after sorting
    all_posts = [post[0] for post in sorted_posts]
    
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