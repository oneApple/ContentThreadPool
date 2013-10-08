登录过程：
REQLOGINMSG: 发送用户类型，用户名，密码

接受登录过程：
REQLOGINMSG:SendLoginResult :如果验证成功，则发送权限LOGINSUCCESS，否则 LOGINFAIL

审核过程：
REQAUDITMSG ：发送文件名

REQDHPANDPUBKEY:SendDhPAndPubkey:发送迪菲参数p和公钥，及各自的签名  SENDDHPANDPUBKEY

SENDDHPUBKEY:RecvDhPubkeyAndSendDhGenerateSuccess:收到对方发来的公钥及签名，首先验证签名，如果验证失败则发送IDENTITYVERIFYFAILED并关闭线程，否则
生成会话密钥并发送AUDITDHGENERATE 

REQFILEBUFFER:SendFileBuffer,发送文件内容，如果未发送完SENDFILEBUFFER，否则SENDFILEOVER

REQAGROUP:SendAgroupSignAndParam:发送a组参数和hash（签名）SENDAGROUP

RECVMEDIASUCCESS:RecvSendMediaSuccess：接收接收成功，并改变状态


审核返回过程：
REQAUDITRETURN:RecvFilename接收文件名，并打开文件准备写,SendDhPAndPubkey:发送迪菲参数p和公钥，及各自的签名  SENDDHPANDPUBKEY

SENDDHPUBKEY:RecvDhPubkeyAndSendDhResult  收到对方发来的公钥及签名，首先验证签名，如果验证失败则发送IDENTITYVERIFYFAILED并关闭线程，否则
生成会话密钥并发送AUDITRETURNDHGENERATE

SENDFILEBUFFER:RecvFileBuffer：接受文件,REQFILEBUFFER

SENDFILEOVER:RecvAllFile：接受文件，并关闭文件 REQCGROUP

SENDCGROUP:RecvCgroupSignAndParam:收到c组参数和c组签名，利用收到的参数在本地采样，然后利用这个参数与a组签名进行验证 AUDITRETURNSUCCESS


请求分发过程：
REQOBTAINFILE:RecvObtainFile,SendDhPAndPubkey ： 接收文件名并保存，SendDhPAndPubkey:发送迪菲参数p和公钥，及各自的签名  SENDDHPANDPUBKEY

SENDDHPUBKEY:RecvDhPubkeyAndSendDhGenerateSuccess  收到对方发来的公钥及签名，首先验证签名，如果验证失败则发送IDENTITYVERIFYFAILED并关闭线程，否则
生成会话密钥并发送AUDITRETURNDHGENERATE

REQFILEBUFFER:SendFileBuffer :发送文件内容，如果未发送完SENDFILEBUFFER，否则SENDFILEOVER

REQAGROUP:SendAgroupSignAndParam:发送a组参数和hash（签名）SENDAGROUP

RECVMEDIASUCCESS:RecvSendMediaSuccess：接收接收成功，并改变状态






