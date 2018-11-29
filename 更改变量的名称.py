>>> var = "This is a string"  
>>> b = "var"                 #设置一个新的字符串
>>> s = locals()[b]           #把b字符串空间的值， 变相的给s变量
>>> s                         #打印s变量 
'This is a string'            #这样就成功实现，用一个值，去充当变量名     这个b可以随意取拼接
