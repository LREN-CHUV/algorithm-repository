FROM hbpmip/python-mip:6fb0698

COPY atsne_cmd /atsne_cmd
COPY libflann_cpp.so.1.8 /libflann_cpp.so.1.8
COPY libQt5Gui.so.5 /libQt5Gui.so.5
COPY libQt5Widgets.so.5 /libQt5Widgets.so.5

CMD python -m SimpleHTTPServer 8000
