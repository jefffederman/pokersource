-- -*-sql-*- 
--
-- Copyright (C) 2009 Loic Dachary <loic@dachary.org>
--
-- This software's license gives you freedom; you can copy, convey,
-- propagate, redistribute and/or modify this program under the terms of
-- the GNU Affero General Public License (AGPL) as published by the Free
-- Software Foundation, either version 3 of the License, or (at your
-- option) any later version of the AGPL.
--
-- This program is distributed in the hope that it will be useful, but
-- WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
-- General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program in a file in the toplevel directory called
-- "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
--
DROP TABLE IF EXISTS `tourneys_schedule2prizes`;
CREATE TABLE `tourneys_schedule2prizes` (

  /* Foreign key to tourneys_schedule table */
  `tourneys_schedule_serial` int(11) default NULL,

  /* Foreign key to prizes table */
  `prize_serial` int(11) default NULL,

) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `prizes`;
CREATE TABLE `prizes` (
  `serial` int(11) NOT NULL auto_increment,

  /* Short name of the prize */
  `name` varchar(255) default NULL,

  /* HTML description of the prize */
  `description` varchar(255) default NULL,

  /* URL to the image to be displayed */
  `image_url` text,

  /* points needed for this reward */
  `points` int(10) NOT NULL,

  /* URL to the image to be displayed */
  `link_url` text,
  PRIMARY KEY  (`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
