FROM fnndsc/python-poetry as bash
WORKDIR /data
EXPOSE 80

# copy 代码
COPY . .

# 设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 设置pip3源头 [global]index-url = https://pypi.tuna.tsinghua.edu.cn/simple
RUN touch /etc/pip.conf && echo '[global]' > /etc/pip.conf && echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> /etc/pip.conf && echo '[install]' >> /etc/pip.conf && echo trusted-host = 'pypi.tuna.tsinghua.edu.cn' >> /etc/pip.conf


# 激活配置
RUN poetry shell

# 生成requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 正式安装依赖
# !!! 注意--trusted-host 的值为tool.poetry.source的域名
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt --trusted-host pypi.tuna.tsinghua.edu.cn


ENTRYPOINT python -m uvicorn main:app --host='0.0.0.0' --port=80 --reload

#  docker build -t test:0.0.1 .
#  docker run --name test -p 8000:80 -d test:0.0.1