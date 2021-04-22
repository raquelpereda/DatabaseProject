DROP DATABASE mydb;

CREATE database IF NOT EXISTS mydb;
CREATE TABLE IF NOT EXISTS `mydb`.`clothes` (
  `clid` INT NOT NULL,
  `clname` VARCHAR(200) NULL,
  `color` VARCHAR(45) NULL,
  `size` VARCHAR(6) NULL,
  `category` VARCHAR(60) NULL,
  `price` DECIMAL(15,1) NULL,
  `qty_in_stock` INT NULL,
  PRIMARY KEY (`clid`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `mydb`.`customers` (
  `cid` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(30) NOT NULL,
  `lastname` VARCHAR(30) NOT NULL,
  `email` VARCHAR(30) NULL,
  `password` VARCHAR(16) NULL,
  `phone` VARCHAR(12) NULL,
  `admin` TINYINT NULL,
  PRIMARY KEY (`cid`),
  UNIQUE INDEX `cid_UNIQUE` (`cid` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `mydb`.`transaction` (
  `cid` INT NOT NULL,
  `clid` INT NOT NULL,
  `date` DATE NOT NULL,
  `cardNum` INT NOT NULL,
  `qty` INT NOT NULL,
  INDEX `cid_idx` (`cid` ASC) VISIBLE,
  INDEX `clid_idx` (`clid` ASC) VISIBLE,
  CONSTRAINT `cid`
    FOREIGN KEY (`cid`)
    REFERENCES `mydb`.`customers` (`cid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `clid`
    FOREIGN KEY (`clid`)
    REFERENCES `mydb`.`clothes` (`clid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE mydb;
SELECT * FROM customers;
SELECT * FROM clothes;