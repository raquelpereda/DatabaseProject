CREATE TABLE IF NOT EXISTS customers(
  cid INT NOT NULL,
  firstname VARCHAR(45) NOT NULL,
  lastname VARCHAR(45) NOT NULL,
  password BLOB(256) NOT NULL,
  --address VARCHAR(200) NOT NULL,
  phone VARCHAR(12) NULL,
  PRIMARY KEY(cid)
);


