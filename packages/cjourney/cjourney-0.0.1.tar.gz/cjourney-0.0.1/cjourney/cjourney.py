import pandas as pd
import colorsys
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

class Cjourney(object):

    def __init__(self):
        self.df = None
        self.color_index = None 
        self.sequences = None 
        self.sequences_padded = None 

    def __generate_colorbar(self, num):
        def get_n_hls_colors(num):
            hls_colors = []
            i = 0
            step = 360.0 / num
            while i < 360:
                h = i
                s = 90 + random.random() * 10
                l = 50 + random.random() * 10
                _hlsc = [h / 360.0, l / 100.0, s / 100.0]
                hls_colors.append(_hlsc)
                i += step

            return hls_colors

        def ncolors(num):
            rgb_colors = []
            if num < 1:
                return rgb_colors
            hls_colors = get_n_hls_colors(num)
            for hlsc in hls_colors:
                _r, _g, _b = colorsys.hls_to_rgb(hlsc[0], hlsc[1], hlsc[2])
                r, g, b = [int(x * 255.0) for x in (_r, _g, _b)]
                rgb_colors.append([r, g, b])

            return rgb_colors
        
        return ncolors(num)
    
    def fit_on_actions(self, df, event):
        self.df = df
        unique_events = list(self.df[event].unique())
        color_list = self.__generate_colorbar(len(unique_events))
        self.color_index = dict(zip(unique_events, color_list))
    
    def actions_to_sequences(self, cusid, timestamp, event, max_duration=None):
        # cusid: customer unique id or session id
        # timestamp: event trigger time
        # max_duration: max duration of a session
        self.df.sort_values(by=[cusid, timestamp], inplace=True)
        if not max_duration:
            pg = self.df.groupby([cusid])[event].apply(lambda x: list(np.array(x))).tolist()
        else:
            self.df[timestamp] = self.df[timestamp].astype('datetime64[ns]')
            diff = self.df.groupby(cusid)[timestamp].diff(1).to_frame()
            diff[timestamp] = diff[timestamp].dt.seconds
            diff = diff[(diff[timestamp].isna()) | (diff[timestamp]>max_duration)]
            pg = []
            index = diff.index.tolist()
            index_len = len(index)
            for i in range(index_len):
                if i < index_len-1:
                    temp = self.df[index[i]:index[i+1]]
                else:
                    temp = self.df[index[i]:]
                pg_part = temp.groupby([cusid])[event].apply(lambda x: list(np.array(x))).tolist()
                pg = pg + pg_part
       
        self.sequences = pg

    def __plt_sequences(self, maxlen, num_samples, repeat):
       
        fig = plt.figure(figsize=(24, 13))
        gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1]) 
        
        a0 = fig.add_subplot(gs[0])
        a0.imshow(self.sequences_padded, interpolation='nearest')
        a0.set_aspect(0.5)
        a0_xticks_ori = range(0, int(0.5*num_samples), repeat)
        plt.xticks(a0_xticks_ori, range(maxlen))

        ks = []
        vs = None
        color_x_size = 3
        color_y_size = 3
        for k, v in self.color_index.items():
            ks.append(k)
            vtemp = np.array([v])
            vtemp = vtemp.repeat(color_x_size, axis=0).reshape(1, -1, 3)
            vtemp = vtemp.repeat(color_y_size, axis=0).reshape(color_y_size, -1, 3)
            if len(ks) == 1:
                vs = vtemp
            else:
                vs = np.vstack((vs, vtemp))
        a1 = fig.add_subplot(gs[1])
        a1.imshow(vs, interpolation='nearest')
        ori = list(range(0, len(ks)*color_y_size, color_y_size)) + [len(ks)*color_y_size-1]
        plt.yticks(ori, ks + [None])
        plt.xticks([])
        
        plt.show()
                                
    def padding(self, maxlen=None, sampsize=10000, ifplt=True):

        if sampsize == -1:
            sampsize = len(self.sequences)
        
        sequences = self.sequences
        np.random.shuffle(sequences)
        sequences = sequences[:sampsize]
        sequences.sort()
        num_samples = len(sequences)
        lengths = []
        for s in sequences:
            lengths.append(len(s))
        if maxlen is None:
            maxlen = np.max(lengths)
        
        x = np.full((num_samples, maxlen, 3), [255, 255, 255])
        for idx, s in enumerate(sequences):
            trunc = [self.color_index[i] for i in s[:maxlen]]
            x[idx, :len(trunc)] = trunc
      
        if num_samples > 3*maxlen:
            repeat = int(0.5*num_samples/maxlen)
        else:
            repeat = 1
        
        output = x[:, 0].repeat(repeat, axis=0).reshape(num_samples, -1, 3)
        for cdx in range(1, maxlen):
            temp = x[:, cdx].repeat(repeat, axis=0).reshape(num_samples, -1, 3)
            output = np.hstack((output, temp))
        
        self.sequences_padded = output
    
        if ifplt:
            self.__plt_sequences(maxlen, num_samples, repeat)
