'''Senior level — p2_t04_config_builder.py
Write a function build_config that:

Takes a required app_name
Has defaults: version="1.0", debug=False
Accepts any number of plugin names via *args
Accepts any number of settings via **kwargs
Returns a fully built config dict

pyth'''


def build_config(AppName,version='1.0',Debug=False,*args,**kwargs):
    config={}
    config['AppName']=AppName
    config['version']=version
    config['debig']=Debug
    config['plugins']=args
    config['settings']=kwargs
    return config
config1=build_config("MyApp",
    "2.0",
    True,
    "auth", "logging", "cache",
    db_host="localhost",
    db_port=5432,
    max_connections=100)
print(config1)



