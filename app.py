import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

st.set_page_config(page_title="Fridge-to-Feast Chef", page_icon="🍳")

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3-flash-preview')

st.title("🍳 Fridge-to-Feast Chef")
st.write("Snap photos of your fridge, pantry, and freezer, and I'll create Michelin-star recipes for you!")

# --- THE UPDATE: accept_multiple_files=True ---
img_files = st.file_uploader("Upload photos of your kitchen inventory...", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if img_files:
    st.write(f"✅ {len(img_files)} photos uploaded.")
    
    # Display the images in a grid so they don't take up too much vertical space
    cols = st.columns(len(img_files))
    images_to_process = []
    for idx, img_file in enumerate(img_files):
        image = Image.open(img_file)
        images_to_process.append(image)
        with cols[idx]:
            st.image(image, use_container_width=True)
    
    if st.button("What's for Dinner?", type="primary"):
        with st.spinner("Chef Gemini is inspecting all the shelves..."):
            try:
                # Prompt updated to recognize multiple images
                prompt = """
                Act as a professional chef. Analyze these images from my fridge, pantry, and freezer. 
                1. Identify all ingredients you see across ALL the photos.
                2. Suggest 3 creative recipes using these items.
                3. For each recipe, provide:
                   - Name & Prep Time
                   - A 'Chef's Secret' tip to make it better
                   - Step-by-step instructions
                Format the response with beautiful Markdown.
                """
                
                # Send the whole list of images + prompt in one go
                content = [prompt] + images_to_process
                response = model.generate_content(content)
                
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"The chef had a mishap: {e}")
