////////////////////////////////////////////////////////////////////////////////
//
//     Copyright (C) 2008 Bruno Garnier <bruno.garnier@gmail.com>
//
//     This program is free software: you can redistribute it and/or modify
//     it under the terms of the GNU General Public License as published by
//     the Free Software Foundation, either version 3 of the License, or
//     (at your option) any later version.
//
//     This program is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU General Public License for more details.
//
//     You should have received a copy of the GNU General Public License
//     along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
////////////////////////////////////////////////////////////////////////////////

package aspoker.com.bubsy.poker.client
{
    import aspoker.com.bubsy.poker.client.model.User;

    public class PokerClient
    {
        public static const VIEW_IS_BOARD:int=1;
        public static const VIEW_IS_TABLE:int=1;
        public static const VIEW_IS_CASHIER:int=1;

        private static var _user:User = new User();
        private static var _currentState:int = VIEW_IS_BOARD;

        public function PokerClient()
        {

        }

        public static function get user():User
        {
            return _user;
        }
    }
}