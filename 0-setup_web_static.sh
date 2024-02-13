#!/usr/bin/env bash
# Configures a new Ubuntu machine by installing
# Nginx where it would be listening on port 80
# Adds a custom header "X-Served-By" in the response indicating the hostname 
# Serve a page that would return a Hello World string
# Redirect you with a 301 status when the location is /redirect_me
# Serves a custom error message when asked for a page that doesn't exist

Update package list
sudo apt-get update

# Install Nginx
sudo apt-get install -y nginx

# Allow traffic on port 80
sudo ufw allow 'Nginx HTTP'

# Change ownership and permissions
sudo chown -R "$USER":"$USER" /var/www/html
sudo chmod -R 755 /var/www

# Create the necessary project directories if they don't exist
# sudo mkdir -p /data/web_static/
# sudo mkdir -p /data/web_static/shared/
# sudo mkdir -p /data/web_static/releases/
# sudo mkdir -p /data/web_static/releases/test/
# Or simply
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create aa fake index file to test
echo -e "AirBnb Clone is coming soon .." | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link to the current release and delete the previous if any
if [ -L "/data/web_static/current" ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Change ownership and permissions
sudo chown -R ubuntu:ubuntu /data/
sudo chmod -R 755 /data

# Create index file with "Hello World!"
echo -e "Hello World!" | sudo tee /var/www/html/index.html > /dev/null

# Create the configuration file
echo -e "server {
    listen 80;
    server_name localhost;

    error_page 404 /custom_error;

    add_header X-Served-By \$hostname;

    location / {
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
    }

    location /redirect_me {
        return 301 https://github.com/ZEYAD-8/;
    }

    location = /custom_error {
        internal;
        return 200 \"Ceci n'est pas une page\";
    }

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }
}" | sudo tee /etc/nginx/sites-available/my_custom_configuration > /dev/null

# Create symbolic link to enable the configuration
sudo ln -sf /etc/nginx/sites-available/my_custom_configuration /etc/nginx/sites-enabled/

# Remove default configuration symlink
sudo rm /etc/nginx/sites-enabled/default

# Restart Nginx
sudo service nginx restart

# Exit with a 0 status (Succes)
exit 0
