import os

def generate_animated_svg(slide_dir, output_file, duration=5):
    files = sorted([f for f in os.listdir(slide_dir) if f.endswith('.svg')])
    if not files:
        print("No SVG files found.")
        return

    # Basic CSS animation wrapper
    total_duration = len(files) * duration
    
    # Read all SVG contents
    slides_content = []
    for f in files:
        with open(os.path.join(slide_dir, f), 'r') as svg_file:
            content = svg_file.read()
            # Extract inner content (remove outer svg tags if possible, or simple embedding)
            # For simplicity, we will use image tags or foreignObject.
            # actually, best way for GitHub markdown is detailed CSS keyframes on opacity
            slides_content.append(f)

    # We will generate an SVG that embeds the others as images or groups
    # Since we can't easily embed arbitrary SVGs without parsing, 
    # we will use <image> href assuming they are hosted, OR simpler:
    # We construct a single SVG with multiple groups and animate opacity.
    
    # Simpler approach: Create an SVG that actually contains the text of the others
    # But since we wrote the SVGs ourselves, we can just merge them.
    
    combined_svg = f'''<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <style>
    .slide {{ opacity: 0; animation: fade {total_duration}s infinite; }}
'''
    
    # Generate keyframes
    step = 100 / len(files)
    for i in range(len(files)):
        start_pct = i * step
        end_pct = (i + 1) * step
        # Overlap slightly
        combined_svg += f'''
    #slide{i+1} {{ animation-delay: {i * duration}s; }}
'''

    # Keyframes definition
    combined_svg += f'''
    @keyframes fade {{
      0% {{ opacity: 0; }}
      5% {{ opacity: 1; }}
      {100/len(files) - 5}% {{ opacity: 1; }}
      {100/len(files)}% {{ opacity: 0; }}
      100% {{ opacity: 0; }}
    }}
  </style>
'''

    for i, filename in enumerate(files):
        with open(os.path.join(slide_dir, filename), 'r') as f:
            c = f.read()
            # Strip xml header and svg tag to extract content
            body = c.split('>', 1)[1].rsplit('<', 1)[0]
            combined_svg += f'<g id="slide{i+1}" class="slide">{body}</g>\n'

    combined_svg += '</svg>'

    with open(output_file, 'w') as f:
        f.write(combined_svg)
    print(f"Generated {output_file}")

if __name__ == "__main__":
    generate_animated_svg('slides', 'slideshow.svg')
