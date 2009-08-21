#
# Copyright (C) 2007, 2009 Loic Dachary <loic@dachary.org>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
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
ulimit -n 10240
server=$1
shift
for i in $@ ; do
    perl -pi -e "s|<servers>.*</servers>|<servers>$server</servers>|" poker.bot${i}00.xml
    nohup python -u /usr/sbin/pokerbot poker.bot${i}00.xml > bot-$i.out 2>&1 &
done
tail -f bot-?.out
