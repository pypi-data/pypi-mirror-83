import os
import socket
import logging
from time import time, sleep
from select import select
from traceback import format_exc
from .gamestate import GameState


##########################################
# rcssserver3d server communication utility
##########################################

logger = logging.getLogger()


class Server(object):

    def __init__(self, pid=0, host='*', port=None, agent_port=None , select_wait=0.2):
        self.pid = pid
        self.host = host
        self.port = port
        self.agent_port = agent_port

        # agents connected to this server
        self.connected_agents = []

        # game state. game time, score left, score right, ...
        self.game_state = GameState()

        self.sock = None
        self.select_wait = select_wait
        self.__send_timeouts_acc = 0
        self.__get_timeouts_acc = 0


    def __del__(self):
        self.close_connection()


    def __repr__(self):
        return '<RC_Server monitor-port={}, agent-port={}>'.format(self.port, self.agent_port)


    def create_connection(self, timeout=0.5):
        if self.port == None:
            raise RuntimeError('set monitor port before creating connection!')

        if self.sock == None:
            try:
                self.sock = socket.create_connection(('localhost', self.port), timeout=timeout)
                self.sock.setblocking(False)
                self.__send_timeouts_acc = 0
                self.__get_timeouts_acc = 0
            except:
                logger.debug(format_exc())


    def refresh_connection(self):
        self.close_connection()
        self.create_connection()


    def close_connection(self):
        if self.sock != None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except:
                pass
            self.sock = None


    def is_connected(self):
        return self.sock != None  and  select([self.sock], [self.sock], [], select_wait) != ([], [], [])


    def error_accumulates(self, tolerance=2):
        if self.is_connected():
            if self.__get_timeouts_acc > tolerance or self.__send_timeouts_acc > tolerance:
                return True
        return False


    def send_message(self, msg :str, wait=0.2):
        if self.sock == None:
            return

        buf = int.to_bytes(len(msg), 4, byteorder='big') + msg.encode('ascii')

        if not select([], [self.sock.fileno()], [], wait)[1]:
            self.__send_timeouts_acc += 1
            raise TimeoutError('timeout waiting for socket to be writeable on server ' + str(self))
        self.sock.send(buf)

        self.__send_timeouts_acc = 0

    def get_message(self, wait=0.2):
        if self.sock == None:
            raise RuntimeError('sock not created on server ' + str(self))

        self.sock.settimeout(wait)

        # logger.debug('starting to wait for select sock, timestamp ' + repr(time()))
        try:
            if not select([self.sock], [], [], wait)[0]:
                raise TimeoutError('timeout waiting for socket to be readable on server ' + str(self))

            start = time()

            len_bytes = self.sock.recv(4)
            while(len(len_bytes) < 4):
                len_bytes += self.sock.recv(1)
                # sleep(0.005)
                if (time() - start > wait and len(len_bytes) < 4):
                    raise TimeoutError('timeout reading message header on server ' + str(self))

            msg_len = int.from_bytes(len_bytes, byteorder='big')

            buf = b''
            while len(buf) < msg_len:
                if not select([self.sock], [], [], wait)[0]:
                    raise TimeoutError('read operation not complete on server ' + str(self))
                buf += self.sock.recv(msg_len)
                # sleep(0.005)
        except:
            self.__get_timeouts_acc += 1
            raise
        else:
            self.__get_timeouts_acc = 0

        #logToFile('util - ' + msg)
        return buf.decode('ascii')

    def send_init(self):
        self.send_message("(init)")


    def send_reset_game_time(self):
        self.send_message('(time 0)')


    def send_kickOff(self, left :bool):
        self.send_message("(kickOff Left)" "(kickOff Right)")


    def send_dropBall(self):
        self.send_message("(dropBall)")


    def send_move_ball(self, x, y, z, vx=0, vy=0, vz=0):
        self.send_message("(ball (pos %.2f %.2f %.2f) (vel %.2f %.2f %.2f))" % (x, y, z, vx, vy, vz))


    def send_playMode(self, mode :str):
        self.send_message("(playMode %s)" % (mode))


    def send_freeKick(self, left :bool):
        self.send_playMode("free_kick_left" if left else  "free_kick_right")


    def send_directFreeKick(self, left :bool):
        self.send_playMode("direct_free_kick_left" if left else  "direct_free_kick_right")


    def send_kill_erver(self):
        self.send_message("(killsim)")


    def send_move_agent(self, x, y, z, left :bool, agentID :int):
        # - (agent (team [Right,Left])(unum <n>)(pos <x y z>)):
        # Set the position and velocity of the given player on the field.
        # Example: (agent (team Left)(unum 1)(pos -52.0 0.0 0.3))
        self.send_message("(agent (team %s)(unum %d)(pos %.2f %.2f %.2f))".format("Left" if left else "Right", agentID, x, y, z))


    def send_request_full_state(self):
        self.send_message("(reqfullstate)")
    

    def sync_game_state(self, retry=2) -> bool:
        
        if not self.is_connected():
            return
            
        #msg = getFullStateMessage(mon['sock'], timeout=0.5)
        try:
            self.send_request_full_state() # always request for full game states
        except:
            logger.debug('error on sending request of full state.')
            return

        msg = ''
        while msg[2:7] != 'Field': # full state message starts with "((FieldLength ..."
            try:
                msg = self.get_message(wait=0.01 )
            except:
                retry -= 1
                logger.debug(format_exc())
                logger.debug('Server communication error, retrying...' + repr(retry))

            if retry <= 0:
                break

            sleep(0.001)

        if msg:
            try:
                self.game_state.parse_state(msg)
            except:
                logger.warning('Error on parsing game state string:')
                logger.debug(msg)
