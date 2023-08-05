#!/usr/bin/env python
'''
dash_board
Created by Seria at 29/12/2018 3:29 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
from ..toolkit.utility import curve2str
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import pandas as pd
import os
import termios
import sys
from pynput import keyboard



class HotKey(keyboard.HotKey):
    def __init__(self, keys, on_activate):
        super(HotKey, self).__init__(keys, on_activate)

    def press(self, key):
        """Updates the hotkey state for a pressed key.

        If the key is not currently pressed, but is the last key for the full
        combination, the activation callback will be invoked.

        Please note that the callback will only be invoked once.

        :param key: The key being pressed.
        :type key: Key or KeyCode
        """
        if key in self._keys and key not in self._state:
            self._state.add(key)
            if self._state == self._keys:
                ret = self._on_activate()
                return ret



def switch_mode():
    return 0
def show_curve_1():
    return 1
def show_curve_2():
    return 2
def show_curve_3():
    return 3
def show_curve_4():
    return 4
def show_curve_5():
    return 5
def show_curve_6():
    return 6
def show_curve_7():
    return 7

def on_quit():
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    return False

class CtrlPanel(keyboard.Listener):
    """A keyboard listener supporting a number of global hotkeys.

    This is a convenience wrapper to simplify registering a number of global
    hotkeys.

    :param dict hotkeys: A mapping from hotkey description to hotkey action.
        Keys are strings passed to :meth:`HotKey.parse`.

    :raises ValueError: if any hotkey description is invalid
    """
    def __init__(self, dashboard):
        self.rank = dashboard.param['rank']
        self.db = dashboard
        self.kc = keyboard.Controller()
        if self.rank>0:
            hotkeys = {}
        else:
            hotkeys = {'<ctrl>+0': switch_mode,
                       '<ctrl>+1': show_curve_1,
                       '<ctrl>+2': show_curve_2,
                       '<ctrl>+3': show_curve_3,
                       '<ctrl>+4': show_curve_4,
                       '<ctrl>+5': show_curve_5,
                       '<ctrl>+6': show_curve_6,
                       '<ctrl>+7': show_curve_7,
                       '<backspace>': on_quit}
        self._hotkeys = [
            HotKey(HotKey.parse(key), value)
            for key, value in hotkeys.items()]
        super(CtrlPanel, self).__init__(
            on_press=self._on_press,
            on_release=self._on_release,)

    def actuate(self):
        if self.rank > 0:
            return
        fd = sys.stdin
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, new)
            self.kc.press(keyboard.Key.backspace)
            self.kc.release(keyboard.Key.backspace)
            self.join()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def refresh(self):
        self.kc.press(keyboard.Key.ctrl)
        self.kc.press('0')
        self.kc.release(keyboard.Key.ctrl)
        self.kc.release('0')

        self.kc.press(keyboard.Key.ctrl)
        self.kc.press('0')
        self.kc.release(keyboard.Key.ctrl)
        self.kc.release('0')

    def _on_press(self, key):
        """The press callback.

        This is automatically registered upon creation.

        :param key: The key provided by the base class.
        """
        for hotkey in self._hotkeys:
            ret = hotkey.press(self.canonical(key))
            if ret is False:
                return ret
            elif isinstance(ret, int):
                if ret>0:
                    self.db.panel = ret-1
                else:
                    self.db.is_global = not self.db.is_global

    def _on_release(self, key):
        """The release callback.

        This is automatically registered upon creation.

        :param key: The key provided by the base class.
        """
        for hotkey in self._hotkeys:
            _ = hotkey.release(self.canonical(key))



class DashBoard(object):
    palette = ['#F08080', '#00BFFF', '#FFFF00', '#2E8B57', '#6A5ACD', '#FFD700', '#808080']
    linestyle = ['-', '--', '-.', ':']
    def __init__(self, config=None, log_path='./aerolog', window=1, divisor=10, span=30, format=None, rank=-1):
        '''
        :param config:
        :param window: the window length of moving average
        :param format: a list of which the element is format and mode, e.g. ['3f', 'raw']
        '''
        if config is None:
            self.param = {'log_path': log_path, 'window': window, 'divisor': divisor,
                          'span': span, 'format': format, 'rank': rank}
        else:
            config['window'] = config.get('window', window)
            config['divisor'] = config.get('divisor', divisor)
            config['span'] = config.get('span', span)
            config['rank'] = config.get('rank', rank)
            self.param = config
        assert len(self.param['format'])<8, 'NEBULAE ERROR ⨷ there are at most 7 panels to monitor.'
        if not os.path.exists(self.param['log_path']):
            os.mkdir(self.param['log_path'])
        self.max_epoch = 0
        self.first_call = True # if it is the first call for self.gauge()
        self.win_mile = {}
        self.gauge_mile = {}
        self.gauge_epoch = {}
        self.trail_mile = {}
        self.trail_epoch = {}
        self.tailor = None
        self.is_global = True
        self.panel = 0
        self.kctrl = keyboard.Controller()

    def _getOridinal(self, number):
        remainder = number % 10
        if remainder == 1:
            ordinal = 'st'
        elif remainder == 2:
            ordinal = 'nd'
        elif remainder == 3:
            ordinal = 'rd'
        else:
            ordinal = 'th'
        return ordinal

    def _formatAsStr(self, stage, abbr, value, global_mile=-1):
        format, mode = self.param['format'][abbr]
        format = '%-' + format
        if mode == 'raw':
            return (' %%s ➠ \033[1;36m%s\033[0m |' % format) % (abbr, value)
        elif mode == 'percent':
            return (' %%s ➠ \033[1;36m%s%%%%\033[0m |' % format) % (abbr, value*100)
        elif mode == 'image':
            if global_mile >= 0:
                cv2.imwrite(os.path.join(self.param['log_path'], '%s/%s_%d.jpg'%(stage, abbr, global_mile)), value)
            return ''
        elif mode == 'tailor':
            string = self.tailor(abbr, value)
            return ' %s ➠ \033[1;36m%s\033[0m |' % (abbr, string)
        else:
            raise KeyError('%s is an illegal format option.' % mode)

    def gauge(self, entry, mile, epoch, mpe, stage, interval=1, duration=None):
        if self.param['rank']>0:
            return
        epoch += 1
        string_mile = ''
        flag_display = False
        flag_epoch_end = False
        if mile % interval == 0:
            flag_display = True
        if (mile+1) % mpe == 0:
            flag_epoch_end = True
            if epoch > self.max_epoch:
                self.max_epoch = epoch
            string_epoch = ''
            cnt = 0
        if self.first_call:
            self.time = time.time()
            self.first_call = False
        items = []
        for abbr, value in entry.items():
            # read gauge every mile
            global_mile = ((epoch-1)*mpe+mile)
            name = stage + ":" + abbr
            items.append(name)
            if flag_display:
                string_mile += self._formatAsStr(stage, abbr, value, global_mile)
            if self.param['format'][abbr][1] == 'tailor': ################### ??? ##################
                continue
            if name not in self.win_mile.keys():
                self.win_mile[name] = np.zeros((self.param['window'],))
                self.gauge_mile[name] = []
                self.gauge_epoch[name] = [0]
                self.trail_mile[name] = []
                self.trail_epoch[name] = []
            self.win_mile[name][global_mile % self.param['window']] = value
            if mile == 0:
                self.gauge_epoch[name][-1] = value
            else:
                self.gauge_epoch[name][-1] += value
            if global_mile < self.param['window']:
                gauge = np.array(self.win_mile[name][:global_mile+1]).mean()
            else:
                gauge = np.array(self.win_mile[name]).mean()
            self.gauge_mile[name].append(gauge)
            self.trail_mile[name].append(global_mile)
            if flag_epoch_end:
                # read gauge every epoch
                self.gauge_epoch[name][-1] /= mpe
                self.trail_epoch[name].append(epoch)
                indicator = self._formatAsStr(stage, abbr, self.gauge_epoch[name][-1])
                string_epoch += indicator
                if indicator != '':
                    cnt += 1
                self.gauge_epoch[name].append(0)
        if flag_display:
            data = np.array(self.gauge_mile[items[self.panel]])
            curve = curve2str(data, self.param['divisor'], self.param['span'],
                              self.is_global, x_title='step', y_title=items[self.panel] + 10*' ')
            print(curve)
            ordinal = self._getOridinal(epoch)
            progress = int(mile / mpe * 20 + 0.4)
            yellow_bar = progress * ' '
            space_bar = (20 - progress) * ' '
            if duration is None:
                duration = '--:--'
            else:
                duration = '%.3f'%duration
            print('| %d%s Epoch ✇ %d Miles ⊰⟦\033[43m%s\033[0m%s⟧⊱︎ ⧲ %ss/mile | %s |%s     '
                  % (epoch, ordinal, mile, yellow_bar, space_bar, duration, stage, string_mile), end='\n')
            print(f'\033[{self.param["divisor"]+7}A')
        if flag_epoch_end:
            w = os.get_terminal_size().columns-1
            for _ in range(self.param["divisor"]+6):
                print(w*' ')
            print(f'\033[{self.param["divisor"]+7}A')
            ordinal = self._getOridinal(epoch)
            mileage = str(epoch * mpe)
            display = '| %d%s Epoch ✇ %s Miles ︎⧲ %.2fs/epoch | %s |%s' \
                      % (epoch, ordinal, mileage, time.time() - self.time, stage, string_epoch)
            print('+' + (len(display) - 3 - cnt * 11) * '-' + '+' + 30 * ' ')
            print(display)
            print('+' + (len(display) - 3 - cnt * 11) * '-' + '+' + 30 * ' ')
            self.time = time.time()

    def read(self, entry, stage, epoch=-1):
        if self.param['rank']>0:
            return
        assert epoch!=0, 'NEBULAE ERROR ⨷ epoch starts from 1.'
        return self.gauge_epoch[stage + ':' + entry][epoch-1]

    def record(self, entry, stage, value):
        if self.param['rank']>0:
            return
        name = stage + ':' + entry
        if name in self.gauge_epoch.keys():
            raise KeyError('NEBULAE ERROR ⨷ %s has been taken in dashboard.'%name)
        else:
            self.gauge_epoch[name] = value

    def log(self, gauge=True, tachograph=True, record=None):
        if self.param['rank']>0:
            return
        if gauge:
            boards = {}
            # clustering
            for k in self.param['format'].keys():
                boards[k] = []
            for k in self.gauge_mile.keys():
                boards[k.split(':')[-1]].append(k)
            # plot
            for k in boards.keys():
                for i, b in enumerate(boards[k]):
                    stage = b.split(':')[0]
                    plt.plot(self.trail_mile[b], self.gauge_mile[b], c=self.palette[i % 7], label=b)
                    plt.legend()
                    plt.grid(True)
                    plt.savefig(os.path.join(self.param['log_path'], '%s_%s_%.3g_mile_%d.jpg'
                                          % (k.replace('/', '-'), stage, self.gauge_mile[b][-1], self.trail_mile[b][-1])))
                    plt.close()

                for i, b in enumerate(boards[k]):
                    plt.plot(self.trail_epoch[b], self.gauge_epoch[b][:-1], marker='o',
                             c=self.palette[i % 7], linestyle=self.linestyle[i % 4], label=b)
                if self.max_epoch > 0:
                    plt.legend()
                    plt.grid(True)
                    plt.savefig(os.path.join(self.param['log_path'], '%s_epoch_%d.jpg' % (k.replace('/', '-'), self.max_epoch)))
                    plt.close()
        if tachograph:
            for k in self.gauge_mile.keys():
                stage, metric = k.split(':')
                df = pd.DataFrame(data={'A': self.trail_mile[k], 'B': self.gauge_mile[k]})
                df.to_csv(os.path.join(self.param['log_path'], '%s_%s_mile.csv'%(metric.replace('/', '-'), stage)),
                          header=None, index=None)
                df = pd.DataFrame(data={'A': self.trail_epoch[k], 'B': self.gauge_epoch[k][:-1]})
                df.to_csv(os.path.join(self.param['log_path'], '%s_%s_epoch.csv' % (metric.replace('/', '-'), stage)),
                          header=None, index=None)