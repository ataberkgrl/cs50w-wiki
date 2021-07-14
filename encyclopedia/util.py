import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def search(query):
    _, filenames = default_storage.listdir("entries")
    search_results = []
    print("query: " + query)
    for filename in filenames:
        if filename.lower() == query.lower() + ".md":
            return re.sub(r"\.md$", "", filename)
        elif query.lower() in filename.lower(): 
            search_results.append((re.sub(r"\.md$", "", filename)))
    return sorted(search_results)

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    try:
        f = default_storage.open(f"entries/{title}.md", "wb")
        f.write(content.encode("utf-8"))
        f.close()
    except FileNotFoundError:
        return None


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md", "rb")
        content = f.read().decode("utf-8")
        f.close()
        return content
    except FileNotFoundError:
        return None

# #-###### TEXT --- Heading
# **TEXT** or __TEXT__ --- Bold
# - TEXT --- Unordered List
# [TEXT](URL) --- Link
# You can create a new paragraph by leaving a blank line between lines of text. --- Paragraph

def trans_links_to_html(content):
    return re.sub(r"\[(?P<link_text>[\S ][^\]]+[^\]])\]\((?P<url>\S+)\)", r"<a href='\g<url>'>\g<link_text></a>", content)

def trans_headings_to_html(content):
    heading_regex = re.compile(r"(?P<heading_size>^\#{1,5})[\t ]*(?P<heading_text>\S+)(\r\n?|\n|$)", flags=re.MULTILINE)
    slider = 0
    old_content_length = len(content)
    for match in heading_regex.finditer(content):
        heading_size = len(match.group("heading_size"))
        content = content[:match.span()[0] + slider] + f"<h{heading_size}>{match.group('heading_text')}</h{heading_size}>"  + match.group(3) + content[match.span()[1] + slider:]
        slider = len(content) - old_content_length
        old_content_length = len(content)
    return content

def trans_paragraphs_to_html(content):
    return re.sub(r"(^[^\#\r\n\-\*][^\#\r\n]+)((\r|\n|\r\n)[^\r\n]+)*", r"<p>\g<1></p>", content, flags=re.MULTILINE)

def trans_bolds_to_html(content):
    return re.sub(r"\*\*(?P<bold_text_a>[\S\t ][^*]*)\*\*", r"<b>\g<bold_text_a></b>", content)
    return re.sub(r"__(?P<bold_text_u>[\S\t ][^*]*)__", r"<b>\g<bold_text_u></b>", content)

def trans_lists_to_html(content):
    list_regex = re.compile(r"(^(\*|-)[\S ]*(\r\n?|\n|$))+", flags=re.MULTILINE)
    slider = 0
    old_content_length = len(content)
    for match in list_regex.finditer(content):
        li_string = ""
        for item in match.group().splitlines():
            li_string += f"\t<li>{item[1:].strip()}</li>\n"
        content = content[:match.span()[0] + slider] + f"<ul>\n{li_string}</ul>"  + match.group(3) + content[match.span()[1] + slider:]
        slider = len(content) - old_content_length
        old_content_length = len(content)
    return content

def MarkdownToHTML(content):
    content = trans_bolds_to_html(content)
    content = trans_links_to_html(content)
    print(content)
    content = trans_paragraphs_to_html(content)
    content = trans_headings_to_html(content)
    content = trans_lists_to_html(content)
    return content

# print(MarkdownToHTML("HTML"))
# print("-----------------------------------")
# print(MarkdownToHTML("CSS"))
# print("-----------------------------------")
# print(MarkdownToHTML("Django"))
# print("-----------------------------------")
# print(MarkdownToHTML("Git"))
# print("-----------------------------------")
# print(MarkdownToHTML("Python"))

# \[(?P<link_text>\S+)\]\((?P<url>\S+)\) REGEX FOR LINKS
# (?P<heading_size>\#{1,5})[\t ]*(?P<heading_text>\S+)(\n|$) REGEX FOR HEADING
# [^\r\n]+((\r|\n|\r\n)[^\r\n]+)* REGEX FOR PARAGRAPH
# \*\*(?P<bold_text_a>[\S\t ][^*]*)\*\*|__(?P<bold_text_u>[\S\t ][^*]*)__ REGEX FOR BOLD 
# ((\*|-)[\S ]*(\n|$))+ REGEX FOR LIST ITEM

