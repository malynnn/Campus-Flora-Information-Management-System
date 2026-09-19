import os

images_dir = os.path.join("static", "images")
os.makedirs(images_dir, exist_ok=True)

# Generate header_placeholder.svg
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="600" viewBox="0 0 1600 600">
  <defs>
    <linearGradient id="maroonGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4a0000" />
      <stop offset="50%" stop-color="#700000" />
      <stop offset="100%" stop-color="#2b0000" />
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,193,7,0.08)" stroke-width="1"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="1600" height="600" fill="url(#maroonGrad)" />
  <rect width="1600" height="600" fill="url(#grid)" />

  <!-- Decorative Botanical Silhouettes -->
  <g opacity="0.15" fill="#FFC107">
    <path d="M200,600 Q300,300 150,100 Q400,250 500,600 Z" />
    <path d="M1400,600 Q1300,250 1450,50 Q1200,200 1100,600 Z" />
    <circle cx="800" cy="300" r="280" stroke="#FFC107" stroke-width="2" fill="none" opacity="0.3"/>
  </g>

  <!-- Placeholder Border Frame -->
  <rect x="50" y="50" width="1500" height="500" fill="none" stroke="#FFC107" stroke-width="2" stroke-dasharray="10 10" opacity="0.6"/>

  <!-- Icon and Text Placeholder Hint -->
  <g transform="translate(800, 260)" text-anchor="middle">
    <!-- Camera / Image Icon -->
    <path d="M -40 -20 L -25 -40 L 25 -40 L 40 -20 L 60 -20 C 68 -20 75 -13 75 -5 L 75 45 C 75 53 68 60 60 60 L -60 60 C -68 60 -75 53 -75 45 L -75 -5 C -75 -13 -68 -20 -60 -20 Z" fill="none" stroke="#FFC107" stroke-width="4"/>
    <circle cx="0" cy="20" r="22" fill="none" stroke="#FFC107" stroke-width="4"/>
    
    <!-- Text instructions for user -->
    <text y="110" font-family="'Poppins', sans-serif" font-size="28" font-weight="bold" fill="#ffffff" letter-spacing="1">
      [ PLACEHOLDER FOR PUPQC CAMPUS HEADER PHOTO ]
    </text>
    <text y="145" font-family="'Poppins', sans-serif" font-size="18" fill="#FFC107" opacity="0.9">
      Replace this file at: static/images/campus_header.jpg
    </text>
  </g>
</svg>
"""

with open(os.path.join(images_dir, "campus_header_placeholder.svg"), "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Created campus_header_placeholder.svg successfully.")
