
CREATE TABLE `articles_urlalias` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `for_update` smallint UNSIGNED NOT NULL,
    `active` bool NOT NULL,
    `urlname` varchar(50) NOT NULL UNIQUE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `articles_article_aliases` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `urlalias_id` integer NOT NULL,
    UNIQUE (`article_id`, `urlalias_id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE `articles_article_aliases` ADD CONSTRAINT article_id_refs_id_3218bf4a FOREIGN KEY (`article_id`) REFERENCES `articles_article` (`id`);
ALTER TABLE `articles_article_aliases` ADD CONSTRAINT urlalias_id_refs_id_3bf67034 FOREIGN KEY (`urlalias_id`) REFERENCES `articles_urlalias` (`id`);


CREATE TABLE `services_urlalias` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `for_update` smallint UNSIGNED NOT NULL,
    `active` bool NOT NULL,
    `urlname` varchar(50) NOT NULL UNIQUE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `services_service_aliases` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `service_id` integer NOT NULL,
    `urlalias_id` integer NOT NULL,
    UNIQUE (`service_id`, `urlalias_id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE `services_service_aliases` ADD CONSTRAINT service_id_refs_id_dc0185e FOREIGN KEY (`service_id`) REFERENCES `services_service` (`id`);
ALTER TABLE `services_service_aliases` ADD CONSTRAINT urlalias_id_refs_id_71eede59 FOREIGN KEY (`urlalias_id`) REFERENCES `services_urlalias` (`id`);
