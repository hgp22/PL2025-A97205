import sys
import re
     
#    for i in range(6, 0, -1):
#        markdown_text = re.sub(r'^' + '#' * i + r' (.*)',
#                               r'<h{0}>\1</h{0}>'.format(i),
#                               markdown_text,
#                               flags=re.MULTILINE)

def markdown_to_html(markdown_text):
    html_text = markdown_text
    
    # Cabecalhos
    html_text = re.sub(r'^# (.+)$',
                       r'<h1>\1</h1>',
                       html_text, flags=re.MULTILINE)
    html_text = re.sub(r'^## (.+)$',
                       r'<h2>\1</h2>',
                       html_text, flags=re.MULTILINE)
    html_text = re.sub(r'^### (.+)$',
                       r'<h3>\1</h3>',
                       html_text, flags=re.MULTILINE)
    
    # Negrito
    html_text = re.sub(r'\*\*(.+?)\*\*',
                       r'<b>\1</b>',
                       html_text)
    
    # Italico
    html_text = re.sub(r'\*(.+?)\*',
                       r'<i>\1</i>',
                       html_text)
    
    # Imagens
    html_text = re.sub(r'!\[(.*?)\]\((.*?)\)',
                       r'<img src="\2" alt="\1"/>',
                       html_text)
    html_text = re.sub(r'\[(.+?)\]\((.+?)\)',
                       r'<a href="\2">\1</a>',
                       html_text)
    
    # Listas
    numbered_items = re.findall(r'^(\d+\. .+)$',
                                html_text, re.MULTILINE)
    
    # Blockquote
    blockquote_pattern = r'(?:^> .+$\n?)+'
    blockquotes = re.finditer(blockquote_pattern,
                              html_text, re.MULTILINE)

    offset = 0

    for match in blockquotes:
            original_blockquote = match.group(0)
            start_pos = match.start() + offset
            end_pos = match.end() + offset

            # Extract blockquote content
            content_lines = re.findall(r'^> (.+)$', original_blockquote, re.MULTILINE)
            html_blockquote = "<blockquote>" + "<br>".join(content_lines) + "</blockquote>"

            # Replace in the text
            html_text = html_text[:start_pos] + html_blockquote + html_text[end_pos:]

            # Update offset
            offset += len(html_blockquote) - len(original_blockquote)
    

    if numbered_items:
        list_groups = []
        current_group = [numbered_items[0]]
    
        item_positions = []
        for match in re.finditer(r'^(\d+\. .+)$', 
                                 html_text, re.MULTILINE):
            item_positions.append((match.start(),
                                   match.end()))
        
        for i in range(1, len(numbered_items)):
            if item_positions[i][0] - item_positions[i-1][1] <= 1:
                current_group.append(numbered_items[i])
            else:
                list_groups.append(current_group)
                current_group = [numbered_items[i]]
        
        if current_group:
            list_groups.append(current_group)
        
        for group in list_groups:
            group_pattern = r'\n?'.join([re.escape(item)
                                         for item in group])
            
            list_content = []
            for item in group:
                content = re.match(r'\d+\. (.+)$', item)
                if content:
                    list_content.append(content.group(1))
            
            html_list = "<ol>" + "".join([f"<li>{item}</li>"
                                          for item in list_content])+"</ol>"
            
            html_text = re.sub(group_pattern,
                               html_list, html_text,
                               flags=re.MULTILINE)
    
    unordered_items = re.findall(r'^([*-] .+)$',
                                 html_text, re.MULTILINE)
    
    if unordered_items:
        list_groups = []
        current_group = [unordered_items[0]]
        
        item_positions = []
        for match in re.finditer(r'^([*-] .+)$',
                                 html_text, re.MULTILINE):
            item_positions.append((match.start(),
                                   match.end()))
        
        for i in range(1, len(unordered_items)):
            if item_positions[i][0] - item_positions[i-1][1] <= 1:
                current_group.append(unordered_items[i])
            else:
                list_groups.append(current_group)
                current_group = [unordered_items[i]]
        
        if current_group:
            list_groups.append(current_group)
        
        for group in list_groups:
            group_pattern = r'\n?'.join([re.escape(item)
                                         for item in group])
            
            list_content = []
            for item in group:
                content = re.match(r'[*-] (.+)$', item)
                if content:
                    list_content.append(content.group(1))
            
            # Create HTML list
            html_list = "<ul>" + "".join([f"<li>{item}</li>"
                                          for item in list_content])+"</ul>"
            
            # Replace in the text
            html_text = re.sub(group_pattern,
                               html_list,
                               html_text, flags=re.MULTILINE)
    
    return html_text

if __name__ == "__main__":
    markdown_text = sys.stdin.read()
    html_output = markdown_to_html(markdown_text)

    final_html = f"""
    <html lang="pt-PT">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport"
                content="width=device-width" />
            <title>TPC3</title>
        </head>
        <body style="display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    padding: 0;">
            <div style="width: 100%;
                        max-width: 800px;
                        padding: 20px;">
                {html_output}
            <div>
            <footer>
                <hr>
                TPC3 Conversor Markdown Html -
                Henrique Pereira - A97205
            </footer
        </body>
    </html>    
    """

    print(final_html)