ALTER TABLE `mainsa_next_db`.`auto_request_tbl` 
DROP COLUMN `time_fld`,
ADD COLUMN `schedule_fld` TINYINT UNSIGNED NOT NULL AFTER `status_changed_fld`;

CREATE TABLE `mainsa_next_db`.`auto_request_sched_tbl` (
  `auto_request_id` MEDIUMINT UNSIGNED NOT NULL,
  `weekday_fld` TINYINT UNSIGNED NOT NULL,
  `from_fld` TIME NOT NULL,
  `to_fld` TIME NOT NULL,
  `modified_fld` DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`auto_request_id`, `weekday_fld`),
  CONSTRAINT `fk_auto_request_sched_tbl_1`
    FOREIGN KEY (`auto_request_id`)
    REFERENCES `mainsa_next_db`.`auto_request_tbl` (`auto_request_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Таблица расписания доступа к автозаявкам по дням недели';

CREATE TABLE `visitor_request_sched_tbl` (
  `visitor_request_id` mediumint(8) unsigned NOT NULL,
  `weekday_fld` tinyint(3) unsigned NOT NULL,
  `from_fld` time NOT NULL,
  `to_fld` time NOT NULL,
  `modified_fld` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`visitor_request_id`,`weekday_fld`),
  CONSTRAINT `fk_visitor_request_sched_tbl_1` FOREIGN KEY (`visitor_request_id`) REFERENCES `visitor_request_tbl` (`visitor_request_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Таблица расписания доступа к заявкам на посетителей по дням недели';

ALTER TABLE `mainsa_db`.`visitor_request_tbl` 
ADD COLUMN `schedule_fld` TINYINT UNSIGNED NOT NULL AFTER `status_changed_fld`;


