#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql.cursors
import os
import configparser
import cryptography


class Config(object):
    def __init__(self, route):
        self.route = route

    def __create_config(self):
        config = configparser.ConfigParser()
        config.add_section("Database")
        config.add_section("Selenium")
        config.add_section("SQL")
        config.set("SQL", "Use SQL", "False")
        config.set("Selenium", "WebDriver", "resources"+"\\"+"\\"+"chromedriver.exe")
        config.set("Selenium", "Chromium", "/usr/bin/google-chrome")
        config.set("Database", "database_user", "root")
        config.set("Database", "database_pass", "pass")
        config.set("Database", "database_name", "bankrupt")
        config.set("Database", "database_table", "bankrupts")
        config.set("Database", "database_temp_table", "bankrupts_temp")
        with open(self.route, "w") as cfg:
            config.write(cfg)

    def get_config(self):
        if not os.path.exists(self.route):
            self.__create_config()
        config = configparser.ConfigParser()
        config.read(self.route)
        return {
            "SQL": config.get("SQL", "Use SQL"),
            "chrome": config.get("Selenium", "Chromium"),
            "webdriver": config.get("Selenium", "Webdriver"),
            "database_user": config.get("Database", "database_user"),
            "database_pass": config.get("Database", "database_pass"),
            "database_name": config.get("Database", "database_name"),
            "database_table": config.get("Database", "database_table"),
            "database_temp_table": config.get("Database", "database_temp_table")
        }


class SQL(object):
    """Get SQL connection, save table"""

    def __init__(self, route):
        cfg = Config(route)
        self.info = cfg.get_config()
        self.con = pymysql.connect(
            user=self.info['database_user'],
            password=self.info['database_pass'],
            db=self.info['database_name'],
        )

    def mysql_save(self, people):
        with self.con.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS `{self.info['database_temp_table']}`;")
            cursor.execute(f"CREATE TABLE `{self.info['database_temp_table']}` (`ID` INT unsigned NOT NULL AUTO_INCREMENT,`BidID` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL UNIQUE,`BidDate` DATETIME NOT NULL,`DeployDate` DATETIME NOT NULL,`AgencyURL` VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,`Obligor` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,`BidType` VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,`Status` INT(1) unsigned NOT NULL DEFAULT '0' COMMENT '0 = Bidding announced; 1 = Applications are open',`AppType` INT(1) unsigned NOT NULL DEFAULT '0' COMMENT '0 = Public; 1 = Private',PRIMARY KEY (`ID`, `BidID`)) ENGINE=InnoDB;")
            for person in people:
                sql = f"INSERT IGNORE INTO `{self.info['database_temp_table']}` (`BidID`, `BidDate`, `DeployDate`, `AgencyURL`, `Obligor`, `BidType`, `Status`, `AppType`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (person['BidID'],
                                     person['BidDate'],
                                     person['DeployDate'],
                                     person['AgencyURL'],
                                     person['Obligor'],
                                     person['BidType'],
                                     person['Status'],
                                     person['AppType']
                                     )
                               )
            cursor.execute(f"DELETE LOW_PRIORITY FROM `{self.info['database_table']}`;")
            cursor.execute(f"INSERT INTO {self.info['database_name']}.{self.info['database_table']} SELECT * FROM {self.info['database_name']}.{self.info['database_temp_table']};")
            cursor.execute(f"DROP TABLE IF EXISTS `{self.info['database_temp_table']}`;")
        self.con.commit()