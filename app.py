import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io

st.set_page_config(page_title="Fridge-to-Feast Chef", page_icon="🍳")

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3-flash-preview')

st.title("🍳 Fridge-to-Feast Chef")
st.write("Upload photos of your fridge, pantry, and freezer!")

img_files = st.file_uploader("Upload photos...", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if img_files:
    processed_images = []
    
    # Show progress to avoid "Freezing" feel
    with st.status("👨‍🍳 Preparing your kitchen photos...", expanded=True) as status:
        for img_file in img_files:
            st.write(f"Resizing {img_file.name}...")
            
            # Open the image
            img = Image.open(img_file)
            
            # --- THE FIX: RESIZE TO MAX 1000px ---
            # This keeps quality high enough for AI but reduces file size by 80%
            img.thumbnail((1000, 1000)) 
            
            # Convert back to bytes for Gemini
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            processed_images.append({
                "mime_type": "image/jpeg",
                "data": img_byte_arr.getvalue()
            })
        
        status.update(label="✅ Photos ready for the Chef!", state="complete")

    if st.button("What's for Dinner?", type="primary"):
        with st.spinner("Chef is analyzing all items..."):
            try:
                prompt = "Identify all ingredients across these photos and suggest 3 recipes with instructions. Format with Markdown."
                
                # We send the resized data instead of the raw huge files
                content = [prompt] + processed_images
                response = model.generate_content(content)
                
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
