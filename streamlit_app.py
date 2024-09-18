import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Investment dashboard',
    page_icon=':earth_europe:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_inv_data():
    """Grab investment data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/inv_data.csv'
    raw_inv_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 2010
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    inv_df = raw_inv_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'INV',
    )

    # Convert years from string to integers
    inv_df['Year'] = pd.to_numeric(inv_df['Year'])

    return inv_df

inv_df = get_inv_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Text.
'''

# Add some spacing
''
''

min_value = inv_df['Year'].min()
max_value = inv_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = inv_df['Country Code'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['Fra', 'Ger'])

''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (inv_df['Country Code'].isin(selected_countries))
    & (inv_df['Year'] <= to_year)
    & (from_year <= inv_df['Year'])
]

st.header('INV over time', divider='gray')

''

st.line_chart(
    filtered_inv_df,
    x='Year',
    y='Investment',
    color='Country Code',
)

''
''


first_year = inv_df[gdp_df['Year'] == from_year]
last_year = inv_df[gdp_df['Year'] == to_year]

st.header(f'INV in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_inv = first_year[first_year['Country Code'] == country]['INV'].iat[0] / 1000000000
        last_inv = last_year[last_year['Country Code'] == country]['INV'].iat[0] / 1000000000

        if math.isnan(first_inv):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_inv / first_inv:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=f'{last_inv:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )
