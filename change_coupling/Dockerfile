FROM ubuntu-base
ADD ./change_coupling/* /home/
ADD ./change_coupling/templates/* /home/templates/
ADD ./utils /home/utils
VOLUME [ "/home/utils" ]
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
EXPOSE 5002/tcp
CMD ["python3","/home/server.py"]