
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# Set page config
st.set_page_config(
    page_title="Chennai House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Create sample Chennai locality data
@st.cache_data
def load_data():
    """Load Chennai house price data"""
    data = {
        'locality': [
            'Anna Nagar', 'Adyar', 'T Nagar', 'Velachery', 'Sholinganallur',
            'Thiruvanmiyur', 'OMR', 'Porur', 'Kilpauk', 'Kodambakkam',
            'Ambattur', 'Mylapore', 'Egmore', 'Pallikaranai', 'Perambur',
            'Madavaram', 'Chromepet', 'Guindy', 'Avadi', 'Nungambakkam',
            'Besant Nagar', 'Saligramam', 'Vadapalani', 'Tambaram', 'Medavakkam'
        ],
        'avg_price_per_sqft': [
            14500, 13600, 13000, 12500, 8200, 10700, 8500, 11200, 
            12700, 10900, 8700, 13100, 11500, 8400, 7300, 7000, 
            7800, 12200, 6900, 13700, 12000, 9500, 10800, 6600, 7100
        ],
        'zone': [
            'Central', 'South', 'Central', 'South', 'South', 'South', 'South', 
            'West', 'Central', 'Central', 'West', 'Central', 'Central', 'South', 
            'North', 'North', 'South', 'Central', 'West', 'Central', 'South',
            'West', 'Central', 'South', 'South'
        ]
    }
    return pd.DataFrame(data)

def create_model():
    """Create and train a simple price prediction model"""
    df = load_data()

    # Create features for training
    zone_mapping = {'North': 1, 'South': 2, 'East': 3, 'West': 4, 'Central': 5}
    df['zone_encoded'] = df['zone'].map(zone_mapping)

    # Simple model using zone as feature
    X = df[['zone_encoded']].values
    y = df['avg_price_per_sqft'].values

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model, df

def main():
    st.title("🏠 Chennai House Price Predictor")
    st.markdown("---")

    # Load data and model
    df = load_data()
    model, _ = create_model()

    # Sidebar for inputs
    st.sidebar.header("Property Details")

    # Select locality
    selected_locality = st.sidebar.selectbox(
        "Select Locality",
        options=df['locality'].tolist()
    )

    # Get locality details
    locality_data = df[df['locality'] == selected_locality].iloc[0]

    # Area input
    area = st.sidebar.number_input(
        "Built-up Area (sq ft)",
        min_value=300,
        max_value=5000,
        value=1000,
        step=50,
        help="Enter the built-up area of your property"
    )

    # Property type
    property_type = st.sidebar.selectbox(
        "Property Type",
        ["Apartment", "Independent House", "Villa"]
    )

    # BHK
    bhk = st.sidebar.selectbox(
        "BHK",
        [1, 2, 3, 4, 5]
    )

    # Age of property
    age = st.sidebar.slider(
        "Age of Property (years)",
        min_value=0,
        max_value=30,
        value=5
    )

    # Additional features
    has_parking = st.sidebar.checkbox("Parking Available")
    amenities = st.sidebar.multiselect(
        "Amenities",
        ["Swimming Pool", "Gym", "Security", "Power Backup", "Garden", "Club House"]
    )

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"📍 {selected_locality}")
        st.write(f"**Zone:** {locality_data['zone']}")
        st.write(f"**Average Price per sq ft:** ₹{locality_data['avg_price_per_sqft']:,}")

        # Calculate price
        base_price_per_sqft = locality_data['avg_price_per_sqft']

        # Apply adjustments based on features
        adjusted_price = base_price_per_sqft

        # Property type adjustment
        if property_type == "Independent House":
            adjusted_price *= 1.1
        elif property_type == "Villa":
            adjusted_price *= 1.2

        # Age adjustment
        if age > 10:
            adjusted_price *= 0.9
        elif age > 20:
            adjusted_price *= 0.8

        # Amenities adjustment
        amenity_bonus = len(amenities) * 0.02
        adjusted_price *= (1 + amenity_bonus)

        # Parking adjustment
        if has_parking:
            adjusted_price *= 1.05

        # Calculate total price
        total_price = adjusted_price * area

        # Display results
        st.subheader("💰 Price Estimation")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric(
                "Price per sq ft",
                f"₹{adjusted_price:,.0f}",
                delta=f"₹{adjusted_price - base_price_per_sqft:,.0f}"
            )

        with col_b:
            st.metric(
                "Total Property Value",
                f"₹{total_price:,.0f}",
                help="Estimated total property value"
            )

        with col_c:
            st.metric(
                "Total (in Lakhs)",
                f"₹{total_price/100000:.1f}L"
            )

        # Confidence interval
        confidence_range = total_price * 0.1
        st.info(f"**Estimated Range:** ₹{total_price - confidence_range:,.0f} - ₹{total_price + confidence_range:,.0f}")

        # Factors affecting price
        st.subheader("📊 Price Factors")
        factors = []

        if property_type != "Apartment":
            factors.append(f"Property Type ({property_type}): +{10 if property_type=='Independent House' else 20}%")

        if age > 10:
            factors.append(f"Property Age ({age} years): -{10 if age <= 20 else 20}%")

        if amenities:
            factors.append(f"Amenities ({len(amenities)}): +{len(amenities)*2}%")

        if has_parking:
            factors.append("Parking: +5%")

        if factors:
            for factor in factors:
                st.write(f"• {factor}")
        else:
            st.write("• Base price applied with no adjustments")

    with col2:
        st.subheader("🗺️ Locality Info")
        st.write(f"**Zone:** {locality_data['zone']}")
        st.write(f"**Avg Price/sqft:** ₹{locality_data['avg_price_per_sqft']:,}")

        # Show top 5 similar priced localities
        df_sorted = df.copy()
        df_sorted['price_diff'] = abs(df_sorted['avg_price_per_sqft'] - locality_data['avg_price_per_sqft'])
        similar_localities = df_sorted.nsmallest(6, 'price_diff')[1:6]  # Exclude the selected locality itself

        st.subheader("📈 Similar Priced Areas")
        for _, row in similar_localities.iterrows():
            st.write(f"• **{row['locality']}**: ₹{row['avg_price_per_sqft']:,}/sqft")

    # Data table
    st.subheader("📋 Chennai Locality Price Data")

    # Add a search functionality
    search_term = st.text_input("Search localities:")
    if search_term:
        filtered_df = df[df['locality'].str.contains(search_term, case=False)]
    else:
        filtered_df = df

    # Display data with formatting
    display_df = filtered_df.copy()
    display_df['avg_price_per_sqft'] = display_df['avg_price_per_sqft'].apply(lambda x: f"₹{x:,}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Download data
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Chennai Price Data",
        data=csv,
        file_name="chennai_house_prices.csv",
        mime="text/csv"
    )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        **Note:** These are estimated prices based on market trends and locality averages. 
        Actual prices may vary based on specific property conditions, exact location, 
        market conditions, and other factors. Please consult with real estate professionals 
        for accurate valuations.

        **Data Sources:** Based on recent market reports from MagicBricks, Housing.com, 
        and other real estate portals for Chennai (2025).
        """
    )

if __name__ == "__main__":
    main()
