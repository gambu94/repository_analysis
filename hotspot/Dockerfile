FROM ubuntu-base
COPY /* /home/
COPY /templates/* /home/templates/
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
EXPOSE 5001/tcp
CMD ["python3","/home/server.py"]