# -*- coding: utf-8 -*-
"""
A subclass of bpy.types.Operator to create an instance of a PySide2 QApplication and run a PySide2 frame/dialog/widget within Blender 2.8.
This code is based on code and information provided by the YouTube channel, "VFX Pipeline" in this video:
	https://youtu.be/QYgHyi7jd9c
"""


import sys

from PySide2.QtCore import QEventLoop, QFile, QTextStream
from PySide2.QtWidgets import QApplication

import bpy


class QWindowEventLoop( bpy.types.Operator ):
	"""
	An instance of a QApplication and an event loop to process events on PySide2 based tools running within Blender.

	Arguments:
		 widget {PySide2.QWidgets} -- [description]
		 args {list} -- [description]
		 kwargs {dict} -- [description]

	Returns:
		 [type] -- [description]
	"""

	bl_idname = 'blender.pyside2_event_loop'
	bl_label = 'PySide2 Event Loop'

	def __init__( self, widget, *args, **kwargs ):
		self._args = args
		self._kwargs = kwargs

		self._app = None
		self._event_loop = None
		self._timer = None
		self._widget_base = widget
		self._widget = None


	def model( self, context, _e ):
		"""
		Processes Qt events for self._widget. If self._widget is not visible (e.g. the user closed it) then the event loop servicing timer is removed.

		Arguments:
			 context {bpy.context} -- A Blender context manager.
			 _e {QEvent} -- A PySide 2 event. - UNUSED

		Returns:
			 set -- A set with a single string providing Blender with a result code for this function.
		"""

		wm = context.window_manager

		if not self._widget.isVisible( ):
			wm.event_timer.remove( self._timer )
			return { 'FINISHED' }

		self.event_loop.processEvents( )
		self.app.sendPostedEvents( None, 0 )

		return { 'PASS_THROUGH' }


	def execute( self, context ):
		"""
		The main execution method for this class. If no QApplication exists one is created. An event loop is created, the provided widget
		is instantiated and a servicing timer is created.

		Arguments:
			 context {bpy.context} -- A Blender context manager.

		Returns:
			 set -- A set with a single string providing Blender with a result code for this function.
		"""

		self._app = QApplication.instance( )

		if not self._app:
			self._app = QApplication( sys.argv )

		stylesheet_filepath = self._kwargs.get( 'stylesheet', None)
		self.set_stylesheet( stylesheet_filepath )

		self._event_loop = QEventLoop( )
		self._widget = self._widget_base( *self._args, **self._kwargs )

		# Run Modal
		wm = context.window_manager
		self._timer = wm.event_timer_add( 1 / 120, window = context.window )
		context.window_manager.modal_handler_add( self )

		return { 'RUNNING_MODEL' }


	def set_stylesheet( self, filepath ):
		"""
		If a stylesheet was specified this function loads it and applies the styling to self._widget.

		Arguments:
			 filepath {str} -- An absolute filepath to a PySide2 QSS stylesheet.
		"""

		file_qss = QFile( filepath )
		if file_qss.exists( ):
			file_qss.open( QFile.ReadOnly )
			stylesheet = QTextStrem( file_qss ).readAll( )
			self._app.setStyleSheet( stylesheet )
			file_qss.close( )
