
# Project Configuration
[project]
# Enable telemetry (default: true). No personal data is collected.
enable_telemetry = true

# List of environment variables to be provided by each user to use the app.
user_env = []

# Duration (in seconds) during which the session is saved when the connection is lost
session_timeout = 3600

# Enable third-party caching (e.g., LangChain cache)
cache = false

# Allow specific origins for CORS (useful when embedding Chainlit)
allow_origins = ["http://localhost:5500", "http://127.0.0.1:5500"]

# Features Configuration
[features]
# Show the prompt playground
prompt_playground = true

# Authorize users to upload files with messages
multi_modal = true

# Speech-to-text feature configuration
[features.speech_to_text]
enabled = false
# language = "en-US"

# UI Configuration
[UI]
# Name of the app and chatbot
name = "My Chainlit App"

# Show the README while the conversation is empty
show_readme_as_default = true

# Description of the app and chatbot (used for HTML tags)
description = "An AI-powered assistant built with Chainlit."

# Collapse large content blocks by default for a cleaner UI
default_collapse_content = true

# Expand messages by default
default_expand_messages = true

# Hide the chain of thought details from the user in the UI
hide_cot = false

# Link to your GitHub repository (adds a GitHub button in the UI's header)
# github = "https://github.com/your-repo"

# Use full-width layout
layout = "wide"

# Specify a CSS file to customize the user interface
custom_css = "/public/stylesheet.css"

# Specify a JavaScript file to customize the user interface
custom_js = "/public/custom.js"

# Custom login page background image (relative to public directory or external URL)
login_page_image = "/public/custom-background.jpg"

# Custom login page image filter (Tailwind internal filters)
# login_page_image_filter = "brightness-50 grayscale"
# login_page_image_dark_filter = "contrast-200 blur-sm"

# Theme Configuration
[UI.theme.light]
background = "#ffffff"
paper = "#f9f9f9"

[UI.theme.light.primary]
main = "#007BFF"
dark = "#0056b3"
light = "#66bfff"

[UI.theme.dark]
background = "#1e1e1e"
paper = "#2e2e2e"

[UI.theme.dark.primary]
main = "#66bfff"
dark = "#3399ff"
light = "#99ccff"

# Meta Information
[meta]
generated_by = "Chainlit v2.0.0"
