mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your_heroku@email_id.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
primaryColor=\"#004F45\"
backgroundColor=\"#fff\"
secondaryBackgroundColor=\"#97B1AB\"
textColor=\"#000\"
port = $PORT\n\
" > ~/.streamlit/config.toml