#!/bin/bash

# show database
echo "listing current databases.............."
mysql -u root -ppassword -e "show databases"

# sample test data from https://github.com/tadatakuho/mysql-docker
# create database
mysql -uroot -ppassword -e "create database sakila"
mysql -uroot -ppassword -e "create database sakila_small"

# DDLでテーブルを作成する
mysql -u root -ppassword sakila < "/docker-entrypoint-initdb.d/sakila/sakila-schema.sql"
# データを流し込む
mysql -u root -ppassword sakila < "/docker-entrypoint-initdb.d/sakila/sakila-data.sql"
# small data for testing fast
mysql -u root -ppassword sakila_small < "/docker-entrypoint-initdb.d/sakila/sakila-small.sql"

# show database
echo "listing current databases.............."
mysql -u root -ppassword -e "show databases"
