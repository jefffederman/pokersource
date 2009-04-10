;; Copyright (C) 2005, 2006, 2007, 2008, 2009 Thomas Cort <tcort@tomcort.com>
;;
;; This file is part of TinyPoker.
;;
;; This program is free software: you can redistribute it and/or modify
;; it under the terms of the GNU Affero General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.
;;
;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU Affero General Public License for more details.
;;
;; You should have received a copy of the GNU Affero General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

;;
;; CONFIGURATION
;;
(define hostname "localhost")
(define port 9898)
(define player "BAGELBOT")
(define buyin 500)

;;
;; PROGRAM CODE
;;

(define main
	(lambda ()
		(display (ipp-handshake hostname port player buyin))
		(newline)
	)
)

(main)
