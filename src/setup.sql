CREATE TABLE IF NOT EXISTS customers(
  cid INT NOT NULL AUTO_INCREMENT,
  firstname VARCHAR(45) NOT NULL,
  lastname VARCHAR(45) NOT NULL,
  password BLOB(256) NOT NULL,
  phone VARCHAR(12) NULL,
  email VARCHAR(45) NOT NULL,
  PRIMARY KEY(cid)
);

CREEATE TABLE IF NOT EXISTS clothes(
  clid INT NOT NULL AUTO_INCREMENT,
  category VARCHAR(60),
  size VARCHAR(6),
  price REAL,
  qty_in_stock INT
);
