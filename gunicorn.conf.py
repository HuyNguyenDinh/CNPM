import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
log_file = "/tmp/gunicorn.log"
raw_env = ["DB_HOST=localhost", "DB_PORT=3306", "DB_NAME=clinicapp", "DB_USER=clinicapp", "DB_PASSWORD=clinicapp"]
