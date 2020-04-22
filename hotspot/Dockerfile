FROM ubuntu-base
ADD ./hotspot/* /home/
ADD ./hotspot/templates/* /home/templates/
ADD ./utils /home/utils
VOLUME [ "/home/utils" ]
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
EXPOSE 5001/tcp
CMD ["python3","/home/server.py"]