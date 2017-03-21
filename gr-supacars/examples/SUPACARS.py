#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Supacars
# Generated: Thu Mar  9 18:10:39 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import pyqt
import sip
import supacars
import sys
import time


class SUPACARS(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Supacars")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Supacars")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "SUPACARS")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1 = 'Parser Text Output'
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0 = 'Raw Text Output'
        self.samp_rate = samp_rate = 48000
        self.rx_volume = rx_volume = 100
        self.rx_gain = rx_gain = 26
        self.lo_off = lo_off = 126e3
        self.init_sample_rate = init_sample_rate = 500e3
        self.corr_thres = corr_thres = 0.5
        self.center_freq = center_freq = 131.725e6

        ##################################################
        # Blocks
        ##################################################
        self._rx_volume_range = Range(1, 500, 1, 100, 200)
        self._rx_volume_win = RangeWidget(self._rx_volume_range, self.set_rx_volume, "rx_volume", "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_volume_win, 3,0,1,2)
        self._rx_gain_range = Range(0, 40, 1, 26, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "rx_gain", "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 1,0,1,2)
        self._corr_thres_range = Range(0, 5, 0.01, 0.5, 200)
        self._corr_thres_win = RangeWidget(self._corr_thres_range, self.set_corr_thres, "corr_thres", "counter_slider", float)
        self.top_grid_layout.addWidget(self._corr_thres_win, 0,0,1,2)
        self._variable_qtgui_label_0_1_tool_bar = Qt.QToolBar(self)
        
        if 0:
          self._variable_qtgui_label_0_1_formatter = 0
        else:
          self._variable_qtgui_label_0_1_formatter = lambda x: x
        
        self._variable_qtgui_label_0_1_tool_bar.addWidget(Qt.QLabel('Terminal 2 '+": "))
        self._variable_qtgui_label_0_1_label = Qt.QLabel(str(self._variable_qtgui_label_0_1_formatter(self.variable_qtgui_label_0_1)))
        self._variable_qtgui_label_0_1_tool_bar.addWidget(self._variable_qtgui_label_0_1_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_1_tool_bar, 5,1,1,1)
          
        self._variable_qtgui_label_0_0_tool_bar = Qt.QToolBar(self)
        
        if 0:
          self._variable_qtgui_label_0_0_formatter = 0
        else:
          self._variable_qtgui_label_0_0_formatter = lambda x: x
        
        self._variable_qtgui_label_0_0_tool_bar.addWidget(Qt.QLabel('Terminal 1 '+": "))
        self._variable_qtgui_label_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0)))
        self._variable_qtgui_label_0_0_tool_bar.addWidget(self._variable_qtgui_label_0_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_0_tool_bar, 5,0,1,1)
          
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(init_sample_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(center_freq, lo_off), 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.supacars_acarsparser_0 = supacars.acarsparser(False, '')
        self.supacars_acars_0 = supacars.acars(samp_rate, corr_thres)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	48000, #size
        	samp_rate, #samp_rate
        	"ACARS signal", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 4,0,1,2)
        self.pyqt_text_output_0_0 = pyqt.text_output()
        self._pyqt_text_output_0_0_win = self.pyqt_text_output_0_0;
        self.top_grid_layout.addWidget(self._pyqt_text_output_0_0_win, 6,1,1,1)
        self.pyqt_text_output_0 = pyqt.text_output()
        self._pyqt_text_output_0_win = self.pyqt_text_output_0;
        self.top_grid_layout.addWidget(self._pyqt_text_output_0_win, 6,0,1,1)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_fff(
        	  samp_rate/init_sample_rate,
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        	
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	rx_volume, init_sample_rate, 5e3, 500, firdes.WIN_HAMMING, 6.76))
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.supacars_acars_0, 'raw_output'), (self.pyqt_text_output_0, 'pdus'))    
        self.msg_connect((self.supacars_acars_0, 'parser_output'), (self.supacars_acarsparser_0, 'in'))    
        self.msg_connect((self.supacars_acarsparser_0, 'parsed_out'), (self.pyqt_text_output_0_0, 'pdus'))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.pfb_arb_resampler_xxx_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.supacars_acars_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SUPACARS")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_variable_qtgui_label_0_1(self):
        return self.variable_qtgui_label_0_1

    def set_variable_qtgui_label_0_1(self, variable_qtgui_label_0_1):
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_1_label, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_label_0_1)))

    def get_variable_qtgui_label_0_0(self):
        return self.variable_qtgui_label_0_0

    def set_variable_qtgui_label_0_0(self, variable_qtgui_label_0_0):
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_0_label, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_label_0_0)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(self.samp_rate/self.init_sample_rate)

    def get_rx_volume(self):
        return self.rx_volume

    def set_rx_volume(self, rx_volume):
        self.rx_volume = rx_volume
        self.low_pass_filter_0.set_taps(firdes.low_pass(self.rx_volume, self.init_sample_rate, 5e3, 500, firdes.WIN_HAMMING, 6.76))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
        	

    def get_lo_off(self):
        return self.lo_off

    def set_lo_off(self, lo_off):
        self.lo_off = lo_off
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.center_freq, self.lo_off), 0)

    def get_init_sample_rate(self):
        return self.init_sample_rate

    def set_init_sample_rate(self, init_sample_rate):
        self.init_sample_rate = init_sample_rate
        self.uhd_usrp_source_0.set_samp_rate(self.init_sample_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(self.samp_rate/self.init_sample_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(self.rx_volume, self.init_sample_rate, 5e3, 500, firdes.WIN_HAMMING, 6.76))

    def get_corr_thres(self):
        return self.corr_thres

    def set_corr_thres(self, corr_thres):
        self.corr_thres = corr_thres
        self.supacars_acars_0.set_corr_thres(self.corr_thres)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.center_freq, self.lo_off), 0)


def main(top_block_cls=SUPACARS, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
