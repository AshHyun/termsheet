mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
[theme]\nbase=\"light\"\nprimaryColor=\"#4169e1\"\
\n\
" > ~/.streamlit/config.toml