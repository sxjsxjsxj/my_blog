### 登录接口

#### 1、请求地址： /api/user/auth/register/

#### 2、请求方式：POST

#### 3、请求参数：
    
    u_username 登录账号 string 必填
    u_password 登录密码 string 必填
    u_password2 确认密码 string 必填
    u_email 邮箱 string 必填 
    
#### 4、响应成功

    {
        "code": 200,
        "msg": "请求成功",
        "data": {
            "user_id": 10
        }
    }
    
#### 5、响应失败
    {
    "code": 1001,
    "msg": "注册账号已存在，请更新账号",
    "data": {}
    }
    
    {
    "code": 1002,
    "msg": "密码不一致，请确认密码是否一致",
    "data": {}
    }
    
    {
      {
    "code": 1003,
    "msg": "参数校验失败",
    "data": {
        "u_username": [
            "注册账号必填"
        ],
        "u_password": [
            "注册密码必填"
        ],
        "u_password2": [
            "注册确认密码必填"
        ],
        "u_email": [
            "注册邮箱必填"
        ],
        "u_username": [
            "注册账号不能少于3字符"
        ],
        "u_password": [
            "注册密码不能少于5字符"
        ],
        "u_password2": [
            "注册确认密码不能少于5字符"
        ],
        "u_email": [
            "格式错误"
        ],
        "u_username": [
            "注册账号不能超过10字符"
        ],
        "u_password": [
            "注册密码不能超过10字符"
        ],
        "u_password2": [
            "注册确认密码不能超过10字符"
        ],
    }
}
    }
         
#### 响应参数
    
    code 状态码 
    msg 响应信息
    data 响应数据
    user_id 用户id 用于获取用户信息