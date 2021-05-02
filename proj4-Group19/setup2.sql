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