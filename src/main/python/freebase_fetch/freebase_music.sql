
DROP DATABASE freebase_music;

CREATE DATABASE freebase_music;
USE freebase_music;

CREATE TABLE `resources` (
    `key` INT NOT NULL AUTO_INCREMENT,
    `id` VARCHAR(511) NOT NULL,
    `creator` INT,        # may be null for now
    `timestamp` DATETIME, # may be null for now
    UNIQUE (`id`),
    PRIMARY KEY (`key`),
    FOREIGN KEY(`creator`) REFERENCES `resources`(`key`) ON DELETE CASCADE);

CREATE TABLE `type_domain` (
    `type` INT NOT NULL,
    `domain` INT NOT NULL,
    PRIMARY KEY (`type`, `domain`),
    FOREIGN KEY(`type`) REFERENCES `resources`(`key`) ON DELETE CASCADE,
    FOREIGN KEY(`domain`) REFERENCES `resources`(`key`) ON DELETE CASCADE);

CREATE TABLE `property_schema` (
    `property` INT NOT NULL,
    `schema` INT NOT NULL,
    PRIMARY KEY (`property`),
    FOREIGN KEY(`property`) REFERENCES `resources`(`key`) ON DELETE CASCADE,
    FOREIGN KEY(`schema`) REFERENCES `resources`(`key`) ON DELETE CASCADE);

CREATE TABLE `link_property_source_target` (
    `link` INT NOT NULL,
    `master_property` INT NOT NULL,
    `source` INT,  # apparently can be null
    `target` INT,  # null if it's a literal-valued link
    PRIMARY KEY(`link`),
    UNIQUE(`link`),
    FOREIGN KEY(`link`) REFERENCES `resources`(`key`) ON DELETE CASCADE,
    FOREIGN KEY(`master_property`) REFERENCES `resources`(`key`) ON DELETE CASCADE,
    FOREIGN KEY(`source`) REFERENCES `resources`(`key`) ON DELETE CASCADE,
    FOREIGN KEY(`target`) REFERENCES `resources`(`key`) ON DELETE CASCADE);

CREATE TABLE `resource_type` (
    `resource` INT NOT NULL,
    `type` INT NOT NULL,
    PRIMARY KEY(`resource`, `type`),
    FOREIGN KEY(`resource`) REFERENCES `resources`(`key`) ON DELETE CASCADE,
    FOREIGN KEY(`type`) REFERENCES `resources`(`key`) ON DELETE CASCADE);

