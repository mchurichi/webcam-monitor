#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Webcam viewer.
# Copyright (C) 2010  Gonzalo Exequiel Pedone
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email   : hipersayan DOT x AT gmail DOT com
# Web-Site: http://hipersayanx.blogspot.com/

import sys

# Cargamos los modulos de Qt necesarios para el programa.
from PyQt4 import uic, QtGui, QtCore

# Cargamos el modulo de OpenCV.
import cv


class Webcam:
    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi('webcam.ui')

        # Tomamos el dispositivo de captura a partir de la webcam.
        self.webcam = cv.CreateCameraCapture(1)

        # Creamos un temporizador para que cuando se cumpla el tiempo limite
        # tome una captura desde la webcam.
        self.timer = QtCore.QTimer(self.MainWindow)

        # Conectamos la señal timeout() que emite nuestro temporizador con la
        # funcion show_frame().
        self.MainWindow.connect(self.timer, QtCore.SIGNAL('timeout()'), \
            self.show_frame)

        # Tomamos una captura cada 1 mili-segundo.
        self.timer.start(1)

    """
    show_frame() -> None

    Esta funcion toma una captura desde la webcam y la muestra en una QLabel.
    """
    def show_frame(self):
        # Tomamos una captura desde la webcam.
        ipl_image = cv.QueryFrame(self.webcam)

        # Leemos los pixeles de la imagen
        #(numero_de_bytes_por_pixels * ancho * alto).
        data = ipl_image.tostring()

        # Creamos una imagen a partir de los datos.
        #
        # QImage
        # (
        #   Los pixeles que conforman la imagen,
        #   Ancho de de la imagen,
        #   Alto de de la imagen,
        #   Numero de bytes que conforman una linea
        #   numero_de_bytes_por_pixels * ancho),
        #   Formato de la imagen
        # )
        image = QtGui.QImage(data, ipl_image.width, ipl_image.height, \
            ipl_image.channels * ipl_image.width, QtGui.QImage.Format_RGB888)

        '''
        Creamos un pixmap a partir de la imagen.
        OpenCV entraga los pixeles de la imagen en formato BGR en lugar del
        tradicional RGB, por lo tanto tenemos que usar el metodo rgbSwapped()
        para que nos entregue una imagen con los bytes Rojo y Azul
        intercambiados, y asi poder mostrar la imagen de forma correcta.
        '''
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())

        # Mostramos el QPixmap en la QLabel.
        self.MainWindow.lblWebcam.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    webcam = Webcam()
    webcam.MainWindow.show()
    app.exec_()
