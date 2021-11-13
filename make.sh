sudo rm /etc/systemd/system/web.service
sudo cp /var/app/current/web.service /etc/systemd/system/
sudo rm /etc/nginx/nginx.conf
sudo cp /var/app/current/nginx.conf /etc/nginx/
sudo cp -r /var/app/current/taiga-front-dist/ /home/ec2-user/
sudo systemctl restart nginx
sudo systemctl daemon-reload
sudo systemctl restart web

