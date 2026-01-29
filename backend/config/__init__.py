# TeamTrack config package
# Use PyMySQL as MySQLdb when using MySQL backend
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
