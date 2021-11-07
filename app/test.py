
# reference: https://blog.csdn.net/qq_38226778/article/details/115250861
# connect to localhost to get familiar with sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, inspect, create_engine

engine = create_engine(
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="root",
        database="todo_list",
        host="localhost"
    )
)

# inspector
insp = inspect(engine)
print("tables in this db: ", insp.get_table_names())

# check out sqlalchemy
session = sessionmaker(bind=engine)()

# refect the table out
metadata = MetaData(bind=engine)
metadata.reflect(bind=engine)
Base = automap_base(metadata=metadata)
Base.prepare()

task_table = getattr(Base.classes, "tasks")

primary_key = inspect(task_table).primary_key

print("the primary key of tasks: ", primary_key)

# print(primary_key[0].name) 

print("columns keys: ", inspect(task_table).c.keys())

columns = list(inspect(task_table).columns)
print("columns info: ", columns)


# 以上便是每一个字段的属性组成的列表，每一个元素都是<class ‘sqlalchemy.sql.schema.Column’>类型
# 那么我们便可以拿到相应的属性
print()
print("name\tkey\tdtype\tnullable\tcomment")
for col_attr in columns:
    print(col_attr.name,"\t",col_attr.primary_key,"\t",str(col_attr.type),"\t",col_attr.nullable, "\t", col_attr.comment)
