import urllib.parse
import requests
from bs4 import BeautifulSoup
import re


# --- Lyrics Fetching ---
def get_lyrics(song: str, artist: str) -> str:
    try:
        response = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{song}")
        return response.json().get("lyrics", "Lyrics not found.")
    except:
        return "Could not fetch lyrics."


def create_genius_url(artist: str, song: str) -> str:
    """
    Creates a Genius.com lyrics URL from artist and song names
    
    Args:
        artist: Artist name (e.g. "Gino Paoli")
        song: Song title (e.g. "Il Cielo in una Stanza")
    
    Returns:
        str: Formatted Genius URL
    """
    # Convert to lowercase and replace spaces with dashes
    artist_slug = artist.lower().replace(" ", "-")
    song_slug = song.lower().replace(" ", "-")
    
    # Remove special characters (keeping hyphens)
    artist_slug = ''.join(c for c in artist_slug if c.isalnum() or c == '-')
    song_slug = ''.join(c for c in song_slug if c.isalnum() or c == '-')
    
    # Remove any leading/trailing hyphens
    artist_slug = artist_slug.strip('-')
    song_slug = song_slug.strip('-')
    
    # URL encode any remaining special cases
    artist_slug = urllib.parse.quote(artist_slug)
    song_slug = urllib.parse.quote(song_slug)
    
    return f"https://genius.com/{artist_slug}-{song_slug}-lyrics"


def scrape_genius_lyrics(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "Referer": "https://genius.com/",
        "DNT": "1"
    }
    
    try:
        # Add a small delay to be polite
        import time
        time.sleep(1)

        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # STRICT selection - only the lyrics containers
        lyrics_containers = soup.select('div[data-lyrics-container="true"]')
        
        if not lyrics_containers:
            return "Error: No lyrics containers found"
        
        clean_lyrics = []
        for container in lyrics_containers:
            # Remove ALL non-lyric elements including spans, buttons, etc.
            for element in container.find_all(['button', 'svg',]):
                element.decompose()
            
            # Get text while preserving line breaks
            container_text = container.get_text('\n', strip=True)
            
            # Only keep lines that look like actual lyrics
            for line in container_text.split('\n'):
                if line and not any(x in line for x in ['Contributors', 'Lyrics', 'Read More']):
                    clean_lyrics.append(line)
        
        lyrics = '\n'.join(clean_lyrics)
        lyrics = re.sub(r'\n{3,}', '\n\n', lyrics.strip())
        
        return lyrics

    except Exception as e:
        return f"Error: {str(e)}"

    
def erase_before_bracket(text):
    """
    Removes all text before the first occurrence of '[' character.
    
    Args:
        text (str): Input text to process
    
    Returns:
        str: Text with everything before first '[' removed, or original text if '[' not found
    """
    bracket_index = text.find('[')
    return text[bracket_index:] if bracket_index != -1 else text


def remove_text_inside_brackets(text):
    """
    Removes text inside brackets, including cases where brackets are on separate lines.

    Returns:
        str: Text with bracket content removed, including multiline cases
    """
    bracket_pairs = { '[]': (r'\[', r'\]')}
    
    open_b, close_b = bracket_pairs["[]"]
    # Pattern matches brackets with any content (including newlines) between them
    pattern = f'{open_b}[\\s\\S]*?{close_b}'
    return re.sub(pattern, '', text)


def adjust_lowercase_starts(text):
    """
    Adjusts lines where the first word starts with lowercase, moving it to the previous line.
    
    Args:
        text (str): Input text to process
        
    Returns:
        str: Processed text with lowercase-start lines merged with previous lines
    """
    lines = text.split('\n')
    adjusted_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            adjusted_lines.append(line)
            continue
            
        # Check if first character is lowercase
        if line and line[0].islower():
            if adjusted_lines:  # If there's a previous line to append to
                adjusted_lines[-1] = adjusted_lines[-1] + ' ' + line
            else:
                adjusted_lines.append(line)  # First line starts with lowercase
        else:
            adjusted_lines.append(line)
    
    return '\n'.join(adjusted_lines)


def extract_parenthetical_blocks(text):
    """
    Processes text to extract parenthetical content spanning multiple lines,
    and moves each complete block to the line above where it started,
    while preserving original spacing between lines.
    
    Args:
        text (str): Input text with possible multi-line parentheses
        
    Returns:
        str: Processed text with parenthetical blocks moved up
    """
    lines = text.split('\n')
    output = []
    i = 0
    n = len(lines)
    
    while i < n:
        line = lines[i]
        
        # Check if line contains an opening parenthesis
        if '(' in line:
            open_idx = line.index('(')
            content = []
            content_start_line = i
            balance = 1
            current = line[open_idx + 1:]
            found_close = False
            
            # Search for matching closing parenthesis
            while i < n and balance > 0:
                for j, char in enumerate(current):
                    if char == '(':
                        balance += 1
                    elif char == ')':
                        balance -= 1
                        if balance == 0:
                            content.append(current[:j])
                            found_close = True
                            break
                
                if not found_close:
                    content.append(current)
                    i += 1
                    if i < n:
                        current = lines[i]
                    else:
                        break
            
            if found_close:
                # Reconstruct the parenthetical block
                parenthetical = '(' + ''.join(content) + ')'
                
                # Preserve the original line before parenthetical
                lines[content_start_line] = lines[content_start_line][:open_idx].rstrip()
                
                # Clear only the parenthetical content from subsequent lines (preserve empty lines)
                for k in range(content_start_line + 1, i + 1):
                    if lines[k].strip() == current.strip():  # Only clear if this line was part of the parenthetical
                        lines[k] = '' if not lines[k].strip() else lines[k]  # Preserve empty lines
                
                # Insert the parenthetical on the line above
                if content_start_line > 0:
                    lines[content_start_line - 1] += ' ' + parenthetical
                else:
                    lines.insert(0, parenthetical)
                    i += 1
            else:
                i += 1
        else:
            i += 1
    
    # Rebuild the text while preserving original empty lines
    result = []
    for line in lines:
        if line.strip():  # If line has content
            result.append(line.rstrip())
        else:  # Preserve empty lines
            result.append('')
    
    return '\n'.join(result)


def merge_comma_lines(text, space_before_comma=False, keep_original_spacing=False):
    """
    Enhanced version with more control over comma merging.
    
    Args:
        text (str): Input text
        space_before_comma (bool): Whether to add space before comma when merging
        keep_original_spacing (bool): Whether to preserve original line spacing
        
    Returns:
        str: Processed text
    """
    lines = text.split('\n')
    merged_lines = []
    
    for line in lines:
        stripped_line = line.strip()
        
        if not merged_lines:
            merged_lines.append(line if keep_original_spacing else stripped_line)
            continue
            
        if stripped_line.startswith(','):
            # Handle comma merging
            separator = ' ' if space_before_comma else ''
            merged_lines[-1] = merged_lines[-1].rstrip() + separator + stripped_line
        else:
            # Add new line
            new_line = line if keep_original_spacing else stripped_line
            merged_lines.append(new_line)
    
    return '\n'.join(merged_lines)


