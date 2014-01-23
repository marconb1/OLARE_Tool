-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tempo de Geração: 23/01/2014 às 11h27min
-- Versão do Servidor: 5.5.34
-- Versão do PHP: 5.3.10-1ubuntu3.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Banco de Dados: `Name_DB`
--
CREATE DATABASE `Name_DB` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `Name_DB`;

--
-- Estrutura da tabela `TabelaSubst`
--

CREATE TABLE IF NOT EXISTS `TabelaSubst` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Palavra` varchar(500) DEFAULT NULL,
  `Exemplo` varchar(5000) DEFAULT NULL,
  `Frequencia` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13919 ;

--
--Estrutura da tabela `TabelaVAdjAdvSubst`
--

CREATE TABLE IF NOT EXISTS `TabelaVAdjAdvSubst` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Pontuacao` varchar(1) DEFAULT NULL,
  `NovaPolaridade` varchar(40) DEFAULT NULL,
  `Categoria` varchar(500) DEFAULT NULL,
  `Palavra` varchar(500) DEFAULT NULL,
  `ColunaQC` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4227 ;

--
-- Estrutura da tabela `TabelaV`
--

CREATE TABLE IF NOT EXISTS `TabelaV` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Palavra` varchar(500) DEFAULT NULL,
  `Exemplo` varchar(5000) DEFAULT NULL,
  `Frequencia` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11401 ;

--
-- Estrutura da tabela `TabelaAdj`
--

CREATE TABLE IF NOT EXISTS `TabelaAdj` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Palavra` varchar(500) DEFAULT NULL,
  `Exemplo` varchar(5000) DEFAULT NULL,
  `Frequencia` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9852 ;

--
-- Estrutura da tabela `TabelaAdv`
--

CREATE TABLE IF NOT EXISTS `TabelaAdv` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Palavra` varchar(500) DEFAULT NULL,
  `Exemplo` varchar(5000) DEFAULT NULL,
  `Frequencia` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1883 ;

--
