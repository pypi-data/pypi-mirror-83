## This is a fico21soft's common libraries...



#### **install**

```
pip install fico21softlibs
```



#### import

```
from fico21softlibs.common import CommonLib as com
```



#### Static methods

```
restart()
```

```
is_internet_connected()
```

```
create_logger(logger_name, logger_level=logging.ERROR, filename="log")
```

```
open_url(url)
```

```
merge_list(list1, list2)
```

```
os()
```

```
db_connect(server, database, username, password)
```

```
get_contacts(filename)
```

```
read_template(filename)
```

```
smtp_login(host, port, user_name, pwd)
```

```
have_punctuation(str)
```

```
punctuation_pos(str)
```

```
remove_punctuation(src_str)
```

```
get_webdriver()
```

```
wd_wait(wd, timeout=10, presence_id='')
```

```
send_keys(keys)
```

```
wd_send_keys(wd, keys)
```

```
get_clipboard_data()
```

```
set_clipboard_data(data)
```



#### Windows only

```
input_keys(data)
```

```
paste_data(data)
```

