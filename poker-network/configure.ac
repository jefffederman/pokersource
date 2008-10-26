#
# Copyright (C) 2006, 2007, 2008 Loic Dachary <loic@dachary.org>
# Copyright (C) 2008 Bradley M. Kuhn <bkuhn@ebb.org>
# Copyright (C) 2004, 2005, 2006 Mekensleep
#
# Mekensleep
# 24 rue vieille du temple
# 75004 Paris
#       licensing@mekensleep.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.54)
AC_INIT(poker-network, [esyscmd(perl -n -e "print if(s/^version_number = \"(.*)\".*/\1/s)" pokernetwork/__init__.py)])
AC_CONFIG_AUX_DIR(config)
AM_INIT_AUTOMAKE()
AC_CONFIG_SRCDIR([pokernetwork/protocol.py])

AM_MAINTAINER_MODE

# GETTEXT STUFF
AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION(0.13)

POKERNETWORK_AC_PROG_APG(2.2, AC_MSG_ERROR([*** pokernetwork/pokerbotlogic.py requires a working /usr/bin/apg  ***]), , AC_MSG_ERROR([*** apg >= 2.2.0 is not installed - pokernetwork/pokerbotlogic.py needs it. ***]))

AC_PATH_PROG(RSYNC, [rsync])
AC_PATH_PROG(WGET, [wget])
AC_PATH_PROG(TOUCH, [touch])
AC_PATH_PROG(SLEEP, [sleep])
AC_PATH_PROG(MYSQL, [mysql])
AC_SUBST(MYSQL)
AC_PATH_PROG(VALGRIND, [valgrind])
AC_PATH_PROG(XVFB, [Xvfb], ,[$PATH:/usr/bin/X11:/usr/X11R6/bin])
AC_PATH_PROG(PERL, [perl])
AC_PATH_PROGS(WWWBROWSER, [x-www-browser htmlview firefox iceweasel mozilla konqueror epiphany dillo links])

AC_PATH_PROG(PHP, [php])
AC_PATH_PROG(PHPUNIT, [phpunit])
AC_PATH_PROG(POKERCONFIGUPGRADE, [pokerconfigupgrade],,[$PATH:/usr/sbin])
AC_PATH_PROG(BASH, [bash])

if test -z "$POKERCONFIGUPGRADE" ; then AC_MSG_ERROR([pokerconfigupgrade is a mandatory program provided by poker-engine]) ; fi

PHP5_TESTS=/bin/false
if test x$PHP && $PHP --version | grep 'PHP 5' ; then
   if $PHP --define extension=mysql.so --modules | grep mysql ; then
      if test x$PHPUNIT ; then
            PHP5_TESTS=/bin/true
            echo "PHP5_TESTS enabled"
      else
            echo "PHP5_TESTS disabled: http://www.phpunit.de/ not found"
      fi
   else
      echo "PHP5_TESTS disabled: mysql module not found"
   fi
else
   echo "PHP5_TESTS disabled: PHP cli not found or $php --version != PHP 5"
fi

AM_CONDITIONAL([PHP5_TESTS], [$PHP5_TESTS])

pkgsysconfdir=$sysconfdir/$PACKAGE
AC_SUBST(pkgsysconfdir, [$pkgsysconfdir])
pkglibdir=$libexecdir/$PACKAGE
AC_SUBST(pkglibdir, [$pkglibdir])
pkgdatadir=$datadir/$PACKAGE
AC_SUBST(pkgdatadir, [$pkgdatadir])

AC_ARG_ENABLE(poker2d, [  --disable-poker2d do not build a GTK based client], [
    poker2d=false			# for AM_CONDITION

    AM_PATH_PYTHON([2.3])
    AM_CONDITIONAL([PYTHON_2_3], [false])
    AM_CONDITIONAL([PYTHON_2_4], [false])
    AM_CONDITIONAL([PYTHON_2_5], [false])

], [
    # Checks for programs.
    AC_PROG_MAKE_SET
    AC_GNU_SOURCE
    AC_PROG_CPP
    AC_PROG_LIBTOOL

    if test "$GXX" = "yes" -a "$ac_test_CXXFLAGS" != set ; then
      if test "$enable_debug" = "yes" ; then
        CFLAGS="-pipe -g -Wall -W"
        CXXFLAGS="-pipe -g -Wall -Wpointer-arith"
      else
        CFLAGS="-pipe -O3 -Wall -W"
        CXXFLAGS="-pipe -O3 -Wall -Wpointer-arith"
      fi
    fi

    AC_EXEEXT
    AC_OBJEXT
    AC_ISC_POSIX
    AC_HEADER_STDC
    AC_C_INLINE
    
    AC_LANG(C)
    
    test x$prefix = xNONE && prefix="$ac_default_prefix"
    test x$exec_prefix = xNONE && exec_prefix="$prefix"

    ALL_CC_PYTHON
    
    PKG_CHECK_MODULES(GLIB, glib-2.0 >= 2.0, , [AC_MSG_ERROR(glib2 is a mandatory library)])
    PKG_CHECK_MODULES(GLADE, libglade-2.0 >= 2.4.0, , [AC_MSG_ERROR(glade2 is a mandatory library)])

    AC_SUBST(POKER2D_PKGDATADIR, [`eval eval eval echo $pkgdatadir/poker2d`])

    PYTHON_DEPENDENCIES="$PYTHON_DEPENDENCIES gtk"
    PYTHON_DEPENDENCIES="$PYTHON_DEPENDENCIES gtk.glade"

    poker2d=true			# for AM_CONDITION
])

PKG_CHECK_MODULES(POKER_ENGINE, poker-engine >= 1.0.21,, [AC_MSG_ERROR(poker-engine is a mandatory library)])

python_script="
import imp
import sys

path = list()
modules = sys.argv.pop(1)
for module in modules.split('.'):
        (file,  pathname, info) = imp.find_module(module, sys.path + path)
        sys.stdout.write(pathname + ' ')
        path = list(( pathname, ))
"

PYTHON_DEPENDENCIES="$PYTHON_DEPENDENCIES libxml2"
PYTHON_DEPENDENCIES="$PYTHON_DEPENDENCIES twisted"
PYTHON_DEPENDENCIES="$PYTHON_DEPENDENCIES MySQLdb"
AC_ARG_ENABLE(openssl, [  --disable-openssl do not use openssl], [], [
		       PYTHON_DEPENDENCIES="$PYTHON_DEPENDENCIES OpenSSL"
])
AC_ARG_ENABLE(soap, [  --disable-soap do not use soap], [], [
		       PYTHON_DEPENDENCIES="$PYTHON_DEPENDENCIES SOAPpy"
])

AC_SUBST(POKERCONFIGUPGRADE, [$POKERCONFIGUPGRADE])

AC_ARG_ENABLE(debug,
    [  --enable-debug          build in debug mode (the default is to build in optimized mode)],
    [enable_debug=yes])
    
AC_ARG_ENABLE(upgrades,
    [  --enable-upgrades       upgrades are automatically installed from the specified server (default off)],
    [enable_upgrades=yes],
    [enable_upgrades=no])
AC_SUBST(UPGRADES_ENABLE, $enable_upgrades)
AC_SUBST(UPGRADES_SOURCE, $enableval)

for PYTHON in $PYTHONS ; do 
  echo "Check dependencies for $PYTHON"
  found=true
  for module in ${PYTHON_DEPENDENCIES} ; do
    AC_MSG_CHECKING([wether python module $module is available])
    if $PYTHON -c "$python_script" $module ; then
       AC_MSG_RESULT([... yes])
    else
       AC_MSG_RESULT([failed])
       found=false
    fi
  done
  if $found ; then
    break
  else
    echo "Fail to check all dependencies for $PYTHON"
  fi
done
if ! $found ; then
  AC_MSG_ERROR([None of the python found on the system are able to satisfy the dependencies (check the above error messages for more information)])
fi

AM_CONDITIONAL([POKER2D], [test x$poker2d = xtrue])	# For use in Makefile.am

AC_SUBST(POKER_NETWORK_PKGDATADIR, [`eval eval eval echo $pkgdatadir`])
AC_SUBST(POKER_NETWORK_PKGLIBDIR, [`eval eval eval echo $pkglibdir`])
AC_SUBST(POKER_NETWORK_PKGSYSCONFDIR, [`eval eval eval echo $pkgsysconfdir`])
POKER_ENGINE_PKGSYSCONFDIR=`pkg-config --variable=pkgsysconfdir poker-engine` || AC_MSG_ERROR([pkg-config --variable=pkgsysconfdir poker-engine fails])
AC_SUBST(POKER_ENGINE_PKGSYSCONFDIR, [$POKER_ENGINE_PKGSYSCONFDIR])

AC_ARG_WITH(poker-server-host,
[  --with-poker-server-host=<hostname>
                          fully qualified host name of the 
                          default poker server to which the
                          poker client will connect (default localhost). ],
    [ POKER_SERVER_HOST=$with_poker_server_host ],
    [ POKER_SERVER_HOST=localhost ] )
AC_SUBST(POKER_SERVER_HOST)

AC_ARG_WITH(poker-www-host,
[  --with-poker-www-host=<hostname>
                          fully qualified host name of the 
                          default web server to which the
                          poker client will connect (default localhost). ],
    [ POKER_WWW_HOST=$with_poker_www_host ],
    [ POKER_WWW_HOST=localhost ] )
AC_SUBST(POKER_WWW_HOST)

AC_ARG_WITH(wwwbrowser,
[  --with-wwwbrowser=<browser>
                     full path of web browser (default autodetect). ],
    [ WWWBROWSER=$with_wwwbrowser ] )
AC_SUBST(WWWBROWSER)

AC_ARG_WITH(poker-database,
[  --with-poker-database=<name>
                          name of the MySQL database the poker
                          server will use to store information. 
                          (default pokernetwork)],
    [ POKER_DATABASE=$with_poker_database ],
    [ POKER_DATABASE=pokernetwork ] )
AC_SUBST(POKER_DATABASE)

AC_ARG_WITH(poker-dbhost,
[  --with-poker-dbhost=<hostname>
                          hostname of the MySQL server (default localhost). ],
    [ POKER_DBHOST=$with_poker_dbhost ],
    [ POKER_DBHOST=localhost ] )
AC_SUBST(POKER_DBHOST)

AC_ARG_WITH(poker-dbuser,
[  --with-poker-dbuser=<user>
                          user name to connect to the database (default pokernetwork). ],
    [ POKER_DBUSER=$with_poker_dbuser ],
    [ POKER_DBUSER=pokernetwork ] )
AC_SUBST(POKER_DBUSER)

AC_ARG_WITH(poker-dbuser-password,
[  --with-poker-dbuser-password=<password>
                          password for the user used to 
                          connect to the database (default pokernetwork). ],
    [ POKER_DBUSER_PASSWORD=$with_poker_dbuser_password ],
    [ POKER_DBUSER_PASSWORD=pokernetwork ] )
AC_SUBST(POKER_DBUSER_PASSWORD)

AC_ARG_WITH(poker-dbroot,
[  --with-poker-dbroot=<user>
                          root user name to creat database (default root). ],
    [ POKER_DBROOT=$with_poker_dbroot ],
    [ POKER_DBROOT=root ] )
AC_SUBST(POKER_DBROOT)

AC_ARG_WITH(poker-dbroot-password,
[  --with-poker-dbroot-password=<password>
                          password for the mysql root user (default none). ],
    [ POKER_DBROOT_PASSWORD=$with_poker_dbroot_password ],
    [ POKER_DBROOT_PASSWORD= ] )
AC_SUBST(POKER_DBROOT_PASSWORD)

AC_ARG_WITH(test-dbhost,
[  --with-test-dbhost=<hostname>
              hostname for the MySQL server the tests will use (default localhost). ],
    [ MYSQL_TEST_DBHOST=$with_test_dbhost ],
    [ MYSQL_TEST_DBHOST=localhost ] )
AC_SUBST(MYSQL_TEST_DBHOST)

AC_ARG_WITH(test-dbroot,
[  --with-test-dbroot=<user>
                  root user name for MySQL server used during tests (default root). ],
    [ MYSQL_TEST_DBROOT=$with_test_dbroot ],
    [ MYSQL_TEST_DBROOT=root ] )
AC_SUBST(MYSQL_TEST_DBROOT)

AC_ARG_WITH(test-dbroot-password,
[  --with-test-dbroot-password=<password>
                  password for the MySQL root user used during tests (default none). ],
    [ MYSQL_TEST_DBROOT_PASSWORD=$with_test_dbroot_password ],
    [ MYSQL_TEST_DBROOT_PASSWORD= ] )
AC_SUBST(MYSQL_TEST_DBROOT_PASSWORD)

AS_IF([test "x$with_test_dbroot_password" != x],
            [if test `echo $ECHO_N "$with_test_dbroot_password" |  tr ' ' 'G'` != "$with_test_dbroot_password";
            then
                AC_MSG_FAILURE([Tests will not properly work if the you use a --with-test-dbroot-password that has whitespace in it.])
            fi
           ])

AM_UNITTEST

# Generate files
if test x$poker2d = xtrue ; then
        AC_CONFIG_FILES([
        pokerclient2d/Makefile
        pokerclient2d/poker2d.6
        pokerclient2d/poker2d
        pokerclient2d/poker2d.xml
        pokerclient2d/data/Makefile
        pokerclient2d/upgrades/1.0.7-1.0.8.xsl
        ])
fi

AC_CONFIG_FILES([
        database/pokerdatabaseupgrade
        tests/run
        tests/test-clientserver.py
        tests/test-currencyclient.py
        tests/test-pokeravatar.py
        tests/test-attrpack.py
        tests/test-userstats.py
        tests/test-user.py
        tests/test-tourneyattrs.py
        tests/test-pokercashier.py
        tests/test-pokerclient.py
        tests/test-servercrash.py
        tests/test-pokerbotlogic.py
        tests/test-pokerdatabase.py
        tests/test-pokerexplain.py
        tests/test-pokergameclient.py
        tests/test-pokerlock.py
        tests/test-pokernetworkconfig.py
        tests/test-packets.py
        tests/test-actionscript.py
        tests/test-javascript.py
        tests/test-pokerpackets.py
        tests/test-pokerclientpackets.py
        tests/test-pokerservice.py
        tests/test-pokersite.py
        tests/test-pokermemcache.py
        tests/test-pokerauth.py
        tests/test-pokertable.py
        tests/test-proxyfilter.py
        tests/test-countfilter.py
        tests/test-string.py
        tests/test-pokerchildren.py
        tests/test-webservice.py
	tests/test-pokerinteractor.py
	tests/test-pokerrenderer.py
	tests/test-protocol.py
	tests/test-upgrade.py
	tests/test-quit.py
	tests/test-pokerinterface.py
	tests/test-pokerdisplay2d.py
	tests/test-pygame.py
	tests/test-svg2gtk.py
	tests/test-gamewindow.py
	tests/test-poker2d.py
        tests/testcurrency.php
        tests/testpoker.php
        tests/testbirthday.php
	tests/testwebservice.php
        tests/upgrade
], [chmod +x $ac_file])
AC_CONFIG_FILES([
        poker-network.pc
        pokernetwork/pokerserver
        pokernetwork/pokerserver.8
        pokernetwork/pokerbot
        pokernetwork/pokerbot.8
        pokerweb/pages/constants.php.ref
        database/schema.sql
        database/pokerdatabaseupgrade.8
        database/pokerdatabase.5
        conf/poker.bot.xml
        conf/poker.client.xml
        conf/poker.server.xml
        pokerweb/Makefile
        tests/Makefile
        pokernetwork/munin/Makefile
        tests/conf/poker2d.xml
        Makefile
        po/Makefile.in
])
AC_CONFIG_FILES([
        pokerstats/run
        pokerstats/pokerstats
], [chmod +x $ac_file])
AC_CONFIG_FILES([
        pokerstats/pokerstats.1
        pokerstats/poker.stats.xml
        pokerstats/test-stats.py
        pokerstats/Makefile
])
AC_OUTPUT

cat <<!

If this is your first installation, you need to fill the
MySQL root user name and password in ${pkgsysconfdir}/poker.server.xml.
It will be used to create the poker database and user.

If you already have a previous version installed, you must upgrade
your database using:

database/pokerdatabaseupgrade --upgrades=database conf/poker.server.xml

!