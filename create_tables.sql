mysql> CREATE DATABASE securities_master;
mysql> USE securities_master;


mysql> CREATE USER 'sec_user'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON securities_master.* TO 'sec_user'@'localhost';
mysql> FLUSH PRIVILEGES;


CREATE TABLE 'symbol' (
  'id' int NOT NULL AUTO_INCREMENT,
  'exchange_id' int NULL,
  'ticker' varchar(32) NOT NULL,
  'instrument' varchar(64) NOT NULL,
  'name' varchar(255) NULL,
  'sector' varchar(255) NULL,
  'currency' varchar(32) NULL,
  'created_date' datetime NOT NULL,
  'last_updated_date' datetime NOT NULL,
  PRIMARY KEY ('id'),
  KEY 'index_exchange_id' ('exchange_id')
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE 'daily_price' (
  'id' int NOT NULL AUTO_INCREMENT,
  'symbol_id' int NOT NULL,
  'price_date' date NOT NULL,
  'created_date' datetime NOT NULL,
  'last_updated_date' datetime NOT NULL,
  'open_price' decimal(19,4) NULL,
  'high_price' decimal(19,4) NULL,
  'low_price' decimal(19,4) NULL,
  'close_price' decimal(19,4) NULL,
  'adj_close_price' decimal(19,4) NULL,
  'volume' bigint NULL,
  PRIMARY KEY ('id'),
  KEY 'index_synbol_id' ('symbol_id')
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
