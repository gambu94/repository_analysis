FROM ubuntu-base
ADD ./frontend/* /home/
ADD ./frontend/templates/* /home/templates/
ADD ./utils /home/utils
VOLUME [ "/home/utils" ]
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
EXPOSE 5000/tcp
CMD ["python","/home/server.py"]