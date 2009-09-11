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
import aspoker.com.bubsy.poker.client.communication.JsonStreamProxy;
import aspoker.com.bubsy.poker.client.model.User;

public class PokerClient
{
    public static const VIEW_IS_BOARD:int=1;
    public static const VIEW_IS_TABLE:int=1;
    public static const VIEW_IS_CASHIER:int=1;

    private static var _user:User = null ;;
    private static var _currentState:int = VIEW_IS_BOARD;

    public static const SERVER_HOST:String = "www.aspoker.info";
    public static const SERVER_PORT:int = 19384;
    public static const CARDS_PATH:String = "assets/cards/";
    public static const CARDS_PREFIX:String = "small-";
    public static const IMAGE_PATH:String = CARDS_PATH + CARDS_PREFIX;

    private static var _actionJsonStream:JsonStreamProxy = new JsonStreamProxy();

    public function PokerClient()
    {

    }

    static public function get stream():JsonStreamProxy
    {
        return _actionJsonStream;
    }

    public static function get user():User
    {
       if (_user == null) {
            _user = new User(); 
        }
         
        return _user;
    }
}
}
