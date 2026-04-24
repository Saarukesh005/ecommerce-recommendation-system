import streamlit as st
from model.recommender import Recommender

# Path
DATA_PATH = r"C:\ecommerce-recommendation\data\products.xlsx"

# Load model
recommender = Recommender(DATA_PATH)

# Page config
st.set_page_config(page_title="E-commerce Recommender", layout="wide")

# Title
st.title("🛒 Smart E-commerce Recommendation System")
st.write("This system recommends similar products using Machine Learning (TF-IDF + Cosine Similarity).")

# Sidebar
st.sidebar.header("🔍 Search & Filter")

search = st.sidebar.text_input("Search Product")

categories = ["All"] + sorted(recommender.df['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Filter dataset
filtered_df = recommender.df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df['name'].str.contains(search.lower())
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df['category'] == selected_category
    ]

# Product selection
product_list = filtered_df['name'].tolist()

if not product_list:
    st.warning("No products found!")
    st.stop()

selected_product = st.selectbox("Select a product:", product_list)

# Button
if st.button("🔍 Show Recommendations"):

    recommendations = recommender.recommend(selected_product, top_n=10)

    if recommendations.empty:
        st.error("No recommendations found")
    else:
        st.subheader("✨ Recommended Products")

        # Grid layout (3 columns)
        cols = st.columns(3)

        for i, row in recommendations.iterrows():
            with cols[i % 3]:
                st.markdown(f"### {row['name'].title()}")
                st.write(f"📂 Category: {row['category']}")
                st.caption(row['description'][:100] + "...")
                st.markdown("---")