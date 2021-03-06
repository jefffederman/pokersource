#
# Copyright (C) 2006-2010        Loic Dachary <loic@dachary.org>
# Copyright (C) 2008, 2009       Bradley M. Kuhn <bkuhn@ebb.org>
# Copyright (C) 2004, 2005, 2006 Mekensleep <licensing@mekensleep.com>
#                                24 rue vieille du temple, 75004 Paris
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version of the AGPL.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.54)
AC_INIT(poker-network, [esyscmd(perl -n -e "print if(s/^version_number = \"(.*)\".*/\1/s)" pokernetwork/__init__.py)])
AC_CONFIG_AUX_DIR(config)
AM_INIT_AUTOMAKE()
AC_CONFIG_SRCDIR([pokernetwork/protocol.py])

AM_MAINTAINER_MODE

POKERNETWORK_AC_PROG_APG(2.2, AC_MSG_ERROR([*** pokernetwork/pokerbotlogic.py requires a working /usr/bin/apg  ***]), , AC_MSG_ERROR([*** apg >= 2.2.0 is not installed - pokernetwork/pokerbotlogic.py needs it. ***]))

AC_PATH_PROG(RSYNC, [rsync])
AC_PATH_PROG(WGET, [wget])
AC_PATH_PROG(TOUCH, [touch])
AC_PATH_PROG(SLEEP, [sleep])
AC_PATH_PROG(MYSQL, [mysql])
AC_SUBST(MYSQL)
AC_PATH_PROG(PERL, [perl])

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

AC_PROG_MAKE_SET
AC_GNU_SOURCE
AM_PATH_PYTHON([2.4])

PKG_CHECK_MODULES(POKER_ENGINE, poker-engine >= 1.3.4,, [AC_MSG_ERROR(poker-engine is a mandatory library)])

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

AC_SUBST(POKER_NETWORK_PKGDATADIR, [`eval eval eval echo $pkgdatadir`])
AC_SUBST(POKER_NETWORK_PKGLIBDIR, [`eval eval eval echo $pkglibdir`])
AC_SUBST(POKER_NETWORK_PKGSYSCONFDIR, [`eval eval eval echo $pkgsysconfdir`])

POKER_ENGINE_PKGSYSCONFDIR=`pkg-config --variable=pkgsysconfdir poker-engine`
AC_SUBST(POKER_ENGINE_PKGSYSCONFDIR, [$POKER_ENGINE_PKGSYSCONFDIR])

POKER_ENGINE_PKGDATADIR=`pkg-config --variable=pkgdatadir poker-engine`
if test -z "$POKER_ENGINE_PKGDATADIR" ; then
   POKER_ENGINE_PKGDATADIR=/usr/share/poker-engine
fi
AC_SUBST(POKER_ENGINE_PKGDATADIR, [$POKER_ENGINE_PKGDATADIR])

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

AC_CONFIG_FILES([
        database/pokerdatabaseupgrade
        tests/run
        tests/test-clientserver.py
        tests/test-currencyclient.py
        tests/test-pokeravatar.py
        tests/test-user.py
        tests/test-pokercashier.py
        tests/test-pokerclient.py
        tests/test-servercrash.py
        tests/test-pokerbothandeval.py
        tests/test-pokerbotlogic.py
        tests/test-pokerbot.py
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
        tests/test-pokerservice-load.py
        tests/test-tourneytablebalance.py
        tests/test-pokersite.py
        tests/test-pokermemcache.py
        tests/test-pokerauth.py
        tests/test-pokersql.py
        tests/test-pokertable.py
        tests/test-proxy.py
        tests/test-proxyfilter.py
        tests/test-sessionproxyfilter.py
        tests/test-nullfilter.py
        tests/test-webservice.py
	tests/test-protocol.py
	tests/test-leak.py
	tests/test-leak-no-trial.py
	tests/test-leak-reference.py
	tests/test-leak-exarkun.py
	tests/test-pokerserver.py
	tests/test-pokerserver-run-load.py
	tests/test-pokerrestclient.py
        tests/testcurrency.php
        tests/testpoker.php
        tests/testbirthday.php
	tests/testwebservice.php
        tests/upgrade
], [chmod +x $ac_file])
AC_CONFIG_FILES([
        poker-network.pc
        pokernetwork/pokersql
        pokernetwork/pokerserver
        pokernetwork/pokerserver.8
        pokernetwork/pokerbot
        pokernetwork/pokerbot.8
        pokerweb/pages/constants.php.ref
        database/schema.sql
        database/pokerdatabaseupgrade.8
        database/pokerdatabase.5
        conf/poker.bot.xml
        conf/poker.server.xml
        pokerweb/Makefile
        tests/Makefile
        pokernetwork/munin/Makefile
        Makefile
])
AC_CONFIG_FILES([
        pokerstats/run
        pokerstats/pokerstats
	examples/merged-translation-import.plx
], [chmod +x $ac_file])
AC_CONFIG_FILES([
        pokerstats/pokerstats.1
        pokerstats/poker.stats.xml
        pokerstats/test-stats.py
        pokerstats/Makefile
])
AC_CONFIG_FILES([
        pokerprizes/run
], [chmod +x $ac_file])
AC_CONFIG_FILES([
        pokerprizes/poker.prizes.xml
        pokerprizes/test-prizes.py
        pokerprizes/schema.sql
        pokerprizes/Makefile
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
