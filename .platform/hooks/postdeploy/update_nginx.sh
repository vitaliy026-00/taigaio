#!/usr/bin/bash
sudo mv /home/ec2-user/nginx.conf /etc/nginx/
sudo mv /home/ec2-user/web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl restart web
