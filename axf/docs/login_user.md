### 登录接口

#### 1、请求地址： /api/user/auth/login/

#### 2、请求方式：POST

#### 3、请求参数：
    
    u_username 登录账号 string 必填
    u_password 登录密码 string 必填
    
#### 4、响应成功

    {
        "code": 200,
        "msg": "请求成功",
        "data": {
            "token": "80f94c545ce646bd9119d43d61d7b7c4"
        }
    }
    
#### 5、响应失败
    {
        'code': 1004, 
        'msg': '登录账号不存在，请更新账号'
    }
    {
        'code': 1005, 
        'msg': '登录密码错误，请重新输入'
    }
    {
        "code": 1006,
        "msg": "登录参数有误",
        "data": {
            "u_username": [
                "登录账号必填"
            ],
            "u_username": [
            "登录账号不能为空"
            ],
            "u_password": [
            "登录密码必填"
            ]
            "u_password": [
                "登录密码不能为空"
            ]
        }
    }
         

#### 响应参数
    
    code 状态码 
    msg 响应信息
    data 响应数据
    token 给用户随机生成一个用户标识符，用来用户认证