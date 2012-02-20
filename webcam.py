#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import uic, QtGui, QtCore
from hacks import clickable
import cv
import time


class Webcam:

    def __init__(self):
        self.MainWindow = uic.loadUi('webcam.ui')
        self.MainWindow.lblCamZoom.full_size = True
        self.MainWindow.lblCamZoom.show_name = True
        self.MainWindow.lblCamZoom.show_date = True
        self.MainWindow.lblCam1.show_name = True
        self.MainWindow.lblCam2.show_name = True
        self.MainWindow.lblCam3.show_name = True
        self.webcams = {
            0: {
                'containers': [self.MainWindow.lblCam1, self.MainWindow.lblCam2,
                    self.MainWindow.lblCam3]
            }
        }
        self.initialize_webcams()
        self.timer = QtCore.QTimer(self.MainWindow)
        self.MainWindow.connect(self.timer, QtCore.SIGNAL('timeout()'), \
            self.show_frame)
        for i, wc in self.webcams.items():
            for ct in wc['containers']:
                clickable(ct).connect(lambda cam=i: self.set_zoom_cam(cam))
        self.timer.start(1)

    def initialize_webcams(self):
        for i, wc in self.webcams.items():
            wc['webcam'] = cv.CreateCameraCapture(i)
            wc['pixmap'] = None

    def set_zoom_cam(self, cam=None):
        cz = self.MainWindow.lblCamZoom
        for i, wc in self.webcams.items():
            if cz in wc['containers'] and i != cam:
                wc['containers'].remove(cz)
        if not cz in self.webcams[cam]['containers']:
            self.webcams[cam]['containers'].append(cz)

    def put_extra_info(self, pixmap, name=None, date=False):
        qp = QtGui.QPainter()
        c_pixmap = pixmap
        qp.begin(c_pixmap)
        qp.setPen(QtGui.QColor("white"))
        if name:
            qp.drawText(5, 15, QtCore.QString(str(name)))
        if date:
            fecha_hora = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            qp.drawText(200, 280, QtCore.QString(fecha_hora))
        qp.end()
        return c_pixmap

    def show_frame(self):
        max_height = self.MainWindow.height() / 3 - 20
        for i, wc in self.webcams.items():
            ipl_image = cv.QueryFrame(wc['webcam'])
            data = ipl_image.tostring()
            image = QtGui.QImage(data, ipl_image.width, ipl_image.height, \
                ipl_image.channels * ipl_image.width, \
                QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image.rgbSwapped())
            wc['pixmap'] = pixmap

            for c in wc['containers']:
                c_pixmap = pixmap
                if not hasattr(c, 'full_size'):
                    c_pixmap = c_pixmap.scaledToHeight(max_height)
                show_name = c.show_name if hasattr(c, 'show_name') else False
                show_date = c.show_date if hasattr(c, 'show_date') else False
                if show_name or show_date:
                    c_pixmap = self.put_extra_info(c_pixmap, \
                        'Camara %i' % (i + 1), show_date)
                c.setPixmap(c_pixmap)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    webcam = Webcam()
    webcam.MainWindow.showMaximized()
    app.exec_()
