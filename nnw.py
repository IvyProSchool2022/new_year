import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Predefined image path (You can replace it with your own image path)
PREDEFINED_IMAGE_PATH = "RD.jpg"
DATA_TYPE_PATH = "Montserrat-Regular.ttf"

def add_name_to_image(image_path, first_name, middle_name, last_name):
    # Convert all name parts to Title Case
    first_name = first_name.title()
    middle_name = middle_name.title()
    last_name = last_name.title()

    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Define the font
    font = ImageFont.truetype(DATA_TYPE_PATH, 60)

    # Concatenate the full name
    full_name = " ".join([first_name, middle_name, last_name]).strip()

    # Get the size of the image
    image_width, image_height = image.size

    # Calculate the bounding box of the text
    text_bbox = draw.textbbox((0, 0), full_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Position above "Data & AI Enthusiast"
    enthusiast_y = int(image_height * 0.77)  # Reference position for that text
    text_x = (image_width - text_width) // 2
    text_y = enthusiast_y - text_height - 10  # 10px gap

    # Draw outline for visibility
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for offset in offsets:
        draw.text((text_x + offset[0], text_y + offset[1]),
                  full_name, fill="#0465B5", font=font)

    # Draw main white text
    draw.text((text_x, text_y), full_name, fill="#0465B5", font=font)

    return image


# Streamlit App
st.title("Generate Personalized Republic Day Greeting")

# Collect user input for the name
st.subheader("Enter Your Name")
first_name = st.text_input("First Name", placeholder="Enter your first name")
middle_name = st.text_input("Middle Name", placeholder="Enter your middle name")
last_name = st.text_input("Last Name", placeholder="Enter your last name")

if st.button("Generate Image"):
    if first_name and last_name:  # Ensure at least first and last name are provided
        # Generate the personalized image
        personalized_image = add_name_to_image(
            PREDEFINED_IMAGE_PATH, first_name, middle_name, last_name
        )

        # Display the image
        st.image(personalized_image, caption="Your Personalized Image")

        # Convert image to bytes for download
        img_byte_arr = io.BytesIO()
        personalized_image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # Provide a download link
        st.download_button(
            label="Download Image",
            data=img_byte_arr,
            file_name="personalized_image.png",
            mime="image/png",
        )
    else:
        st.error("Please enter at least your first and last name.")

# Footer section
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; font-size: 14px;">
        <p><i>Powered by Ivy Professional School</i></p>
    </div>
    """,
    unsafe_allow_html=True
)


