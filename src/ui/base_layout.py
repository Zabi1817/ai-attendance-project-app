import streamlit as st



import streamlit as st


def style_background_home():
    st.html("""
        <style>
                .stApp, [data-testid="stAppViewContainer"] {
                    background: #5865F2 !important;
                }

                div[data-testid="column"], div[data-testid="stColumn"] {
                    background-color: #E0E3FF !important;
                    padding: 2.5rem !important;
                    border-radius: 5rem !important;
                }

                div[data-testid="column"] [data-testid="stVerticalBlock"], 
                div[data-testid="stColumn"] [data-testid="stVerticalBlock"] {
                    display: flex !important;
                    flex-direction: column !important;
                    align-items: center !important;
                    justify-content: center !important;
                    text-align: center !important;
                }

                div[data-testid="column"] [data-testid="stButton"], 
                div[data-testid="stColumn"] [data-testid="stButton"] {
                    text-align: center !important;
                    display: flex !important;
                    justify-content: center !important;
                }
                
                /* Center the image element inside the column container */
                div[data-testid="column"] img, div[data-testid="stColumn"] img {
                    margin: 0 auto !important;
                    display: block !important;
                }
        </style>  
    """)


def style_background_dashboard():
    st.html("""
        <style>
                .stApp, [data-testid="stAppViewContainer"] {
                    background: #E0E3FF !important;
                }
        </style>  
    """)


def style_base_layout():
    st.html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

         /* Hide Top Bar and Footer of streamlit */
            #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stFooter"] {
                visibility: hidden !important;
                height: 0px !important;
                padding: 0 !important;
            }
                
            .block-container {
                padding-top: 1.5rem !important;    
            }

            /* Set global fonts */
            body, input, select, textarea, label, button, 
            [data-testid="stMarkdownContainer"] p, 
            .stWidgetLabel, [data-testid="stWidgetLabel"] {
                font-family: 'Outfit', sans-serif !important;
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
            }

            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important;
            }
                
            h3, h4, p {
                font-family: 'Outfit', sans-serif !important;    
            }

            /* Premium Button Styling */
            div[data-testid="stButton"] button, button {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 24px !important;
                border: none !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
                transition: all 0.25s ease-in-out !important;
            }

            div[data-testid="stButton"] button[kind="secondary"], button[kind="secondary"] {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 24px !important;
                border: none !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
                transition: all 0.25s ease-in-out !important;
            }

            div[data-testid="stButton"] button[kind="tertiary"], button[kind="tertiary"] {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 24px !important;
                border: none !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
                transition: all 0.25s ease-in-out !important;
            }

            div[data-testid="stButton"] button:hover, button:hover {
                transform: scale(1.05) !important;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
            }
        </style>  
    """)