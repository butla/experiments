uwsgi --module falcon_app.app:app --http-socket :9090 --threads 8 --disable-logging --add-header "connection: close"
