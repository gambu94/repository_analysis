FROM ubuntu-base
ADD ./skill_analysis/frontend/* /home/
ADD ./skill_analysis/templates/* /home/templates/
ADD ./utils /home/utils
VOLUME [ "/home/utils" ]
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
EXPOSE 5003/tcp
CMD ["python","/home/server.py"]