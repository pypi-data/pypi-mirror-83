from alembic import op

def getSchemas():
    try:
      conn = op.get_bind()
      schemas = conn.execute("SELECT schema_name FROM system_manager.license").fetchall()
      return [ str(x[0]) for x in schemas ]
    except:
      return []

def perSchema(schemas=getSchemas(), schemas_ignore=[]):
  def externalWrapper(func):
    def wrapper(*args, **kwargs):
      for s in schemas:
        if s not in schemas_ignore:
          print(f"Executing on schema {s}")
          try:
            op.execute(f"CREATE SCHEMA IF NOT EXISTS {s}")
            op.execute(f"SET search_path TO {s}")
            func(*args, **kwargs)
            op.execute("SET search_path TO default")
          except Exception as e:
            op.execute("SET search_path TO default")
            raise e
    return wrapper
  return externalWrapper
