#FROM python:3.6.10
#COPY /* /home/
#ENV PATH /usr/local/bin:$PATH
#ENV LANG C.UTF-8
#EXPOSE 23232
#CMD ["python","/home/server.py"]
FROM change-coupling_2
COPY /* /home/
COPY /templates/* /home/templates/
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
EXPOSE 5000/tcp
CMD ["python","/home/server.py"]