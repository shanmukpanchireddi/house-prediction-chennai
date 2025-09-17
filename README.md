# Chennai House Price Predictor

A simple Streamlit web application to predict house prices in Chennai based on locality, area, and property features.

## Features

- **25 Chennai Localities**: Includes popular areas like Anna Nagar, Adyar, T Nagar, Velachery, etc.
- **Interactive Input**: Select locality, enter area, property type, BHK, age, and amenities
- **Real-time Prediction**: Instant price calculation with adjustments for property features
- **Price Factors**: Shows how different factors affect the final price
- **Similar Areas**: Suggests localities with similar price ranges
- **Data Export**: Download the complete Chennai locality price data as CSV

## Installation & Setup

1. **Clone or Download** the files to your local machine

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run chennai_house_predictor.py
   ```

4. **Access the App**:
   - Open your browser and go to `http://localhost:8501`

## How to Use

1. **Select Locality**: Choose from 25 popular Chennai localities in the sidebar
2. **Enter Area**: Input the built-up area in square feet
3. **Property Details**: Select property type, BHK, age, parking, and amenities
4. **View Results**: See the estimated price per sq ft and total property value
5. **Explore Data**: Browse the complete locality price data in the table below

## Price Calculation Logic

The app uses the following factors to calculate property prices:

- **Base Price**: Average price per sq ft for the selected locality
- **Property Type**: 
  - Apartment: Base price
  - Independent House: +10%
  - Villa: +20%
- **Age Factor**:
  - 0-10 years: No adjustment
  - 11-20 years: -10%
  - 21+ years: -20%
- **Amenities**: +2% per amenity
- **Parking**: +5% if available

## Data Sources

Price data is based on recent market trends from:
- MagicBricks.com
- Housing.com
- 99acres.com
- Real estate market reports (2025)

## Localities Covered

The app includes data for these Chennai localities:

**Central Chennai**: Anna Nagar, T Nagar, Kilpauk, Kodambakkam, Mylapore, Egmore, Nungambakkam, Guindy

**South Chennai**: Adyar, Velachery, Sholinganallur, Thiruvanmiyur, OMR, Pallikaranai, Chromepet, Besant Nagar, Tambaram, Medavakkam

**West Chennai**: Porur, Ambattur, Avadi, Saligramam, Vadapalani

**North Chennai**: Perambur, Madavaram

## Screenshots

The app provides:
- Clean, intuitive interface
- Real-time price updates
- Detailed price breakdowns
- Locality comparison features
- Data export capabilities

## Limitations

- Prices are estimates based on market averages
- Actual prices may vary based on specific property conditions
- Consult real estate professionals for accurate valuations
- Data is indicative and for educational purposes

## Future Enhancements

- Add more localities and sub-areas
- Include transportation connectivity scores
- Add school/hospital proximity factors
- Implement machine learning models for better predictions
- Add historical price trends

## Support

For questions or suggestions, please create an issue or contact the developer.

---

**Disclaimer**: This tool provides estimated prices based on market trends. Always consult with real estate professionals for actual property valuations.