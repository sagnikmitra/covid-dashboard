mkdir -p ~/.streamlit/
echo "
[general]n
email = "arnab.sen72@gmail.com"n
" > ~/.streamlit/credentials.toml
echo "
[server]n
headless = truen
enableCORS=falsen
port = $PORTn
" > ~/.streamlit/config.toml