FROM python:3.7-slim

ENV TASK_API_HOST api
ENV TASK_API_PORT 8080
ENV FLASK_APP app.py

# Copy local code to the container image.
WORKDIR /app
COPY src ./

# Install dependencies.
RUN pip install  -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

EXPOSE 8081

CMD ["flask", "run", "--host=0.0.0.0", "--port=8081"]