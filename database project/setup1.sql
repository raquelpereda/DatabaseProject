CREATE TABLE IF NOT EXISTS clothes (
  clid INT NOT NULL,
  clname VARCHAR(200) NULL,
  color VARCHAR(45) NULL,
  size VARCHAR(45) NULL,
  category VARCHAR(60) NULL,
  price DECIMAL(15,1) NULL,
  qty_in_stock INT NULL,
  PRIMARY KEY (clid)
  );