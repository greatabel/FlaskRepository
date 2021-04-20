#! /bin/bash

echo "Reload website"
git pull
sudo a2dissite 000-default.conf
sudo a2ensite meomo.conf
sudo service apache2 reload
