import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Fridge-to-Feast Chef", page_icon="🍳")

# 2. API Setup
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3-flash-preview')

st.title("🍳 Fridge-to-Feast Chef")
st.write("Snap a photo of your fridge or pantry, and I'll create Michelin-star recipes for you!")

# 3. File Uploader
img_file = st.file_uploader("Upload a photo of your ingredients...", type=['jpg', 'jpeg', 'png'])

if img_file:
    # Display the uploaded image nicely
    image = Image.open(img_file)
    st.image(image, caption="Current Kitchen Inventory", use_container_width=True)
    
    if st.button("What's for Dinner?", type="primary"):
        with st.spinner("Chef Gemini is inspecting the shelves..."):
            try:
                # The "Chef" Prompt
                prompt = """
                Act as a professional chef. Analyze this image and:
                1. List every ingredient you can identify.
                2. Suggest 3 creative recipes I can make using these items.
                3. For each recipe, provide:
                   - Name & Prep Time
                   - A 'Chef's Secret' tip to make it better
                   - Step-by-step instructions
                
                Format the response with beautiful Markdown, using bold headers and bullet points.
                """
                
                # Process the image
                response = model.generate_content([prompt, image])
                
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"The chef had a mishap: {e}")

st.info("Tip: Make sure the lighting is good so I can see the labels on jars!")
