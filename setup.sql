CREATE TABLE IF NOT EXISTS customers(
  cid INT NOT NULL AUTO_INCREMENT,
  firstname VARCHAR(45) NOT NULL,
  lastname VARCHAR(45) NOT NULL,
  password BLOB(256) NOT NULL,
  phone VARCHAR(12) NULL,
  email VARCHAR(45) NOT NULL,
  PRIMARY KEY(cid)
);

CREATE TABLE IF NOT EXISTS clothes (
  clid INT NOT NULL,
  clname VARCHAR(200) NULL,
  color VARCHAR(45) NULL,
  size VARCHAR(6) NULL,
  category VARCHAR(60) NULL,
  price DECIMAL(15,1) NULL,
  qty_in_stock INT NULL,
  PRIMARY KEY (clid)
  );

  CREATE TABLE IF NOT EXISTS transaction (
  cid INT NOT NULL,
  clid INT NOT NULL,
  date DATE NOT NULL,
  cardNum INT NOT NULL,
  qty INT NOT NULL,
  INDEX cid_idx (cid ASC) VISIBLE,
  INDEX clid_idx (clid ASC) VISIBLE,
  CONSTRAINT cid
    FOREIGN KEY (cid)
    REFERENCES customers (cid)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT clid
    FOREIGN KEY (clid)
    REFERENCES clothes (clid)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    );