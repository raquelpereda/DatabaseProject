CREATE TABLE IF NOT EXISTS customers(
  cid INT NOT NULL AUTO_INCREMENT,
  firstname VARCHAR(45) NOT NULL,
  lastname VARCHAR(45) NOT NULL,
  password BLOB(256) NOT NULL,
  phone VARCHAR(12) NULL,
  email VARCHAR(45) NOT NULL,
  administrator TINYINT NULL,
  PRIMARY KEY(cid)
);



